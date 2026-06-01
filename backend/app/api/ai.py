"""AI 功能 API"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api/ai", tags=["AI 功能"])


class RecommendResponse(BaseModel):
    id: int
    title: str
    author: str
    cover_url: str
    reason: str


class SearchRequest(BaseModel):
    query: str
    limit: int = 10


class ClassifyRequest(BaseModel):
    title: str
    description: str


class SummarizeRequest(BaseModel):
    title: str
    description: str


class ChatRequest(BaseModel):
    message: str
    context: str = ""


@router.post("/recommend")
async def get_recommendations(
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """智能推荐图书
    
    基于用户的借阅历史，AI 分析偏好并推荐图书。
    """
    try:
        recommendations = await ai_service.recommend_books(
            user_id=current_user.id,
            db=db,
            limit=limit
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"推荐服务异常: {str(e)}")


@router.post("/search")
async def semantic_search(
    req: SearchRequest,
    db: Session = Depends(get_db)
):
    """语义搜索图书
    
    使用自然语言描述来搜索图书，例如：
    - "关于太空探索的科幻小说"
    - "适合初学者的 Python 教程"
    - "讲述二战历史的书"
    """
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="搜索内容不能为空")
    
    try:
        results = await ai_service.semantic_search(
            query=req.query,
            db=db,
            limit=req.limit
        )
        return {"results": results, "query": req.query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"搜索服务异常: {str(e)}")


@router.post("/classify")
async def classify_book(
    req: ClassifyRequest,
    current_user: User = Depends(get_current_user)
):
    """智能分类图书
    
    AI 自动分析图书内容并推荐分类标签。
    """
    try:
        result = await ai_service.classify_book(
            title=req.title,
            description=req.description
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分类服务异常: {str(e)}")


@router.post("/summarize")
async def generate_summary(
    req: SummarizeRequest,
    current_user: User = Depends(get_current_user)
):
    """生成图书摘要
    
    AI 自动生成简洁的图书摘要。
    """
    try:
        summary = await ai_service.generate_summary(
            title=req.title,
            description=req.description
        )
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"摘要服务异常: {str(e)}")


@router.post("/chat")
async def ai_chat(
    req: ChatRequest,
    db: Session = Depends(get_db)
):
    """AI 对话助手
    
    回答图书馆相关问题，提供阅读建议。
    """
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空")
    
    try:
        response = await ai_service.chat(
            user_message=req.message,
            context=req.context
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"对话服务异常: {str(e)}")
