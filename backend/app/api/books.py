"""图书 API"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.deps import get_current_user, get_admin_user
from app.models.book import Book, Category
from app.models.user import User

router = APIRouter(prefix="/api/books", tags=["图书"])


class BookCreate(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    publisher: Optional[str] = ""
    publish_date: Optional[str] = ""
    category_id: Optional[int] = None
    description: Optional[str] = ""
    cover_url: Optional[str] = ""
    location: Optional[str] = ""
    total_copies: int = 1


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    publish_date: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    location: Optional[str] = None
    total_copies: Optional[int] = None


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: Optional[str]
    publisher: str
    publish_date: str
    category_id: Optional[int]
    description: str
    cover_url: str
    location: str
    total_copies: int
    available_copies: int
    ai_summary: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class CategoryResponse(BaseModel):
    id: int
    name: str
    parent_id: Optional[int]
    description: str
    
    class Config:
        from_attributes = True


@router.get("", response_model=dict)
async def list_books(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取图书列表"""
    query = db.query(Book)
    
    if category_id:
        query = query.filter(Book.category_id == category_id)
    
    if keyword:
        query = query.filter(
            Book.title.contains(keyword) |
            Book.author.contains(keyword) |
            Book.isbn.contains(keyword)
        )
    
    total = query.count()
    books = query.offset((page - 1) * size).limit(size).all()
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "items": [BookResponse.from_orm(b) for b in books]
    }


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(db: Session = Depends(get_db)):
    """获取分类列表"""
    return db.query(Category).all()


@router.get("/{book_id}", response_model=BookResponse)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """获取图书详情"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")
    return book


@router.post("", response_model=BookResponse, status_code=201)
async def create_book(
    req: BookCreate,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """新增图书（管理员）"""
    # 检查 ISBN 唯一性
    if req.isbn and db.query(Book).filter(Book.isbn == req.isbn).first():
        raise HTTPException(status_code=409, detail="ISBN 已存在")
    
    book = Book(
        title=req.title,
        author=req.author,
        isbn=req.isbn,
        publisher=req.publisher,
        publish_date=req.publish_date,
        category_id=req.category_id,
        description=req.description,
        cover_url=req.cover_url,
        location=req.location,
        total_copies=req.total_copies,
        available_copies=req.total_copies
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}", response_model=BookResponse)
async def update_book(
    book_id: int,
    req: BookUpdate,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """更新图书（管理员）"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")
    
    update_data = req.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)
    
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """删除图书（管理员）"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="图书不存在")
    
    # 检查是否有在借记录
    from app.models.borrow import Borrow
    active_borrows = db.query(Borrow).filter(
        Borrow.book_id == book_id,
        Borrow.status == "borrowed"
    ).count()
    
    if active_borrows > 0:
        raise HTTPException(status_code=400, detail="该图书有在借记录，无法删除")
    
    db.delete(book)
    db.commit()
    return {"message": "删除成功"}


@router.get("/search", response_model=dict)
async def search_books(
    keyword: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """搜索图书"""
    query = db.query(Book).filter(
        Book.title.contains(keyword) |
        Book.author.contains(keyword) |
        Book.description.contains(keyword)
    )
    
    total = query.count()
    books = query.offset((page - 1) * size).limit(size).all()
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "items": [BookResponse.from_orm(b) for b in books]
    }
