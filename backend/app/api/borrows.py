"""借阅 API"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.deps import get_current_user, get_admin_user
from app.models.book import Book
from app.models.borrow import Borrow
from app.models.user import User

router = APIRouter(prefix="/api/borrows", tags=["借阅"])

MAX_BORROWS = 5  # 最大借阅数量
MAX_RENEWALS = 2  # 最大续借次数
BORROW_DAYS = 30  # 默认借阅天数


class BorrowRequest(BaseModel):
    book_id: int


class BorrowResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    book_title: str
    borrow_date: datetime
    due_date: datetime
    return_date: datetime | None
    status: str
    renew_count: int
    
    class Config:
        from_attributes = True


@router.post("", status_code=201)
async def borrow_book(
    req: BorrowRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """借书"""
    # 检查图书是否存在
    book = db.query(Book).filter(Book.id == req.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")
    
    # 检查库存
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="该图书暂无可借库存")
    
    # 检查是否已借阅该书
    existing = db.query(Borrow).filter(
        Borrow.user_id == current_user.id,
        Borrow.book_id == req.book_id,
        Borrow.status == "borrowed"
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="您已借阅该图书，请先归还")
    
    # 检查借阅数量上限
    active_borrows = db.query(Borrow).filter(
        Borrow.user_id == current_user.id,
        Borrow.status == "borrowed"
    ).count()
    if active_borrows >= MAX_BORROWS:
        raise HTTPException(status_code=400, detail=f"已达最大借阅数量({MAX_BORROWS}本)")
    
    # 检查是否有逾期
    overdue = db.query(Borrow).filter(
        Borrow.user_id == current_user.id,
        Borrow.status == "borrowed",
        Borrow.due_date < datetime.utcnow()
    ).first()
    if overdue:
        raise HTTPException(status_code=400, detail="您有逾期未还的图书，请先归还")
    
    # 创建借阅记录
    borrow = Borrow(
        user_id=current_user.id,
        book_id=req.book_id,
        borrow_date=datetime.utcnow(),
        due_date=datetime.utcnow() + timedelta(days=BORROW_DAYS),
        status="borrowed"
    )
    db.add(borrow)
    
    # 更新库存
    book.available_copies -= 1
    
    db.commit()
    db.refresh(borrow)
    
    return {
        "id": borrow.id,
        "book_title": book.title,
        "borrow_date": borrow.borrow_date,
        "due_date": borrow.due_date,
        "message": "借阅成功"
    }


@router.put("/{borrow_id}/return")
async def return_book(
    borrow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """还书"""
    borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="借阅记录不存在")
    
    # 权限检查：只能还自己的书
    if borrow.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="无权操作")
    
    if borrow.status == "returned":
        raise HTTPException(status_code=400, detail="该图书已归还")
    
    # 更新借阅记录
    borrow.return_date = datetime.utcnow()
    borrow.status = "returned"
    
    # 检查是否逾期
    if borrow.return_date > borrow.due_date:
        borrow.status = "overdue"
    
    # 更新库存
    book = db.query(Book).filter(Book.id == borrow.book_id).first()
    if book:
        book.available_copies += 1
    
    db.commit()
    
    return {"message": "归还成功", "status": borrow.status}


@router.put("/{borrow_id}/renew")
async def renew_book(
    borrow_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """续借"""
    borrow = db.query(Borrow).filter(Borrow.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="借阅记录不存在")
    
    if borrow.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权操作")
    
    if borrow.status != "borrowed":
        raise HTTPException(status_code=400, detail="只能续借在借的图书")
    
    if borrow.renew_count >= MAX_RENEWALS:
        raise HTTPException(status_code=400, detail=f"已达最大续借次数({MAX_RENEWALS}次)")
    
    if borrow.due_date < datetime.utcnow():
        raise HTTPException(status_code=400, detail="已逾期的图书无法续借")
    
    # 续借：延长30天
    borrow.due_date += timedelta(days=BORROW_DAYS)
    borrow.renew_count += 1
    
    db.commit()
    
    return {
        "message": "续借成功",
        "new_due_date": borrow.due_date,
        "renew_count": borrow.renew_count
    }


@router.get("/my")
async def my_borrows(
    status: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """我的借阅记录"""
    query = db.query(Borrow).filter(Borrow.user_id == current_user.id)
    
    if status:
        query = query.filter(Borrow.status == status)
    
    borrows = query.order_by(Borrow.created_at.desc()).all()
    
    result = []
    for borrow in borrows:
        book = db.query(Book).filter(Book.id == borrow.book_id).first()
        result.append({
            "id": borrow.id,
            "book_id": borrow.book_id,
            "book_title": book.title if book else "未知",
            "book_cover": book.cover_url if book else "",
            "borrow_date": borrow.borrow_date,
            "due_date": borrow.due_date,
            "return_date": borrow.return_date,
            "status": borrow.status,
            "renew_count": borrow.renew_count
        })
    
    return {"items": result}


@router.get("")
async def list_borrows(
    page: int = 1,
    size: int = 10,
    status: str = None,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """所有借阅记录（管理员）"""
    query = db.query(Borrow)
    
    if status:
        query = query.filter(Borrow.status == status)
    
    total = query.count()
    borrows = query.order_by(Borrow.created_at.desc()).offset((page - 1) * size).limit(size).all()
    
    result = []
    for borrow in borrows:
        user = db.query(User).filter(User.id == borrow.user_id).first()
        book = db.query(Book).filter(Book.id == borrow.book_id).first()
        result.append({
            "id": borrow.id,
            "user": user.username if user else "未知",
            "book_title": book.title if book else "未知",
            "borrow_date": borrow.borrow_date,
            "due_date": borrow.due_date,
            "return_date": borrow.return_date,
            "status": borrow.status,
            "renew_count": borrow.renew_count
        })
    
    return {"total": total, "page": page, "size": size, "items": result}
