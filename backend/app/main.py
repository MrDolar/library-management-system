"""图书管理系统 - FastAPI 应用入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.core.config import get_settings
from app.services.ai_service import ai_service

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    init_db()
    print("✅ 数据库初始化完成")
    
    # 初始化默认分类
    from app.models.book import Category
    from app.core.database import SessionLocal
    db = SessionLocal()
    default_categories = [
        ("文学", "文学作品"),
        ("科幻", "科幻小说"),
        ("历史", "历史著作"),
        ("科技", "科学技术"),
        ("经济", "经济管理"),
        ("教育", "教育学习"),
        ("艺术", "艺术设计"),
        ("哲学", "哲学思想"),
        ("医学", "医学健康"),
        ("法律", "法律法规"),
        ("计算机", "计算机技术"),
        ("心理学", "心理学"),
        ("少儿", "少儿读物"),
        ("其他", "其他类别"),
    ]
    for name, desc in default_categories:
        if not db.query(Category).filter(Category.name == name).first():
            db.add(Category(name=name, description=desc))
    db.commit()
    db.close()
    print("✅ 默认分类初始化完成")
    
    yield
    
    # 关闭时清理
    await ai_service.close()
    print("👋 应用已关闭")


app = FastAPI(
    title="图书管理系统",
    description="AI 驱动的智能图书管理系统",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
from app.api import auth, books, borrows, ai

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(borrows.router)
app.include_router(ai.router)


@app.get("/")
async def root():
    return {
        "name": "图书管理系统 API",
        "version": "1.0.0",
        "docs": "/docs",
        "ai_enabled": settings.AI_API_KEY != "" and settings.AI_API_KEY != "sk-your-api-key-here"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}
