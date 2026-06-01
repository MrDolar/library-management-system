"""AI 服务 - 智能推荐、语义搜索、分类、摘要"""
import json
import httpx
import numpy as np
from typing import Optional
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.models.book import Book
from app.models.borrow import Borrow

settings = get_settings()


class AIService:
    """统一 AI 服务层"""
    
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.base_url = settings.AI_BASE_URL
        self.model = settings.AI_MODEL
        self.embedding_model = settings.AI_EMBEDDING_MODEL
        self._client: Optional[httpx.AsyncClient] = None
    
    @property
    def client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=30.0
            )
        return self._client
    
    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None
    
    def _is_configured(self) -> bool:
        """检查 AI 服务是否已配置"""
        return bool(self.api_key and self.api_key != "sk-your-api-key-here")
    
    async def _chat(self, messages: list, temperature: float = 0.7) -> str:
        """通用 LLM 对话接口"""
        if not self._is_configured():
            raise ValueError("AI 服务未配置，请设置 AI_API_KEY 环境变量")
        
        response = await self.client.post(
            "/chat/completions",
            json={
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 1000
            }
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    
    async def _embed(self, text: str) -> list[float]:
        """文本向量化"""
        if not self._is_configured():
            raise ValueError("AI 服务未配置")
        
        response = await self.client.post(
            "/embeddings",
            json={
                "model": self.embedding_model,
                "input": text
            }
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]
    
    async def recommend_books(self, user_id: int, db: Session, limit: int = 5) -> list[dict]:
        """智能推荐图书
        
        基于用户借阅历史，使用 LLM 生成个性化推荐。
        """
        # 获取用户借阅历史
        borrows = db.query(Borrow).filter(
            Borrow.user_id == user_id
        ).order_by(Borrow.created_at.desc()).limit(10).all()
        
        if not borrows:
            # 冷启动：返回热门图书
            books = db.query(Book).order_by(Book.created_at.desc()).limit(limit).all()
            return [{"id": b.id, "title": b.title, "author": b.author, 
                     "reason": "热门新书推荐"} for b in books]
        
        # 构建用户偏好描述
        borrowed_books = []
        for borrow in borrows:
            book = db.query(Book).filter(Book.id == borrow.book_id).first()
            if book:
                borrowed_books.append(f"《{book.title}》- {book.author}")
        
        borrowed_list = "\n".join(borrowed_books)
        
        # 获取所有图书用于推荐
        all_books = db.query(Book).all()
        book_list = "\n".join([
            f"[{b.id}] 《{b.title}》- {b.author} | 分类: {b.category.name if b.category else '未分类'}"
            for b in all_books
        ])
        
        prompt = f"""你是一个图书推荐专家。根据用户的借阅历史，从图书库中推荐{limit}本用户可能喜欢的图书。

用户借阅过的图书：
{borrowed_list}

图书库：
{book_list}

请返回 JSON 数组，每个元素包含：
- id: 图书ID
- reason: 推荐理由（简短）

只返回 JSON，不要其他文字。"""

        try:
            response = await self._chat([
                {"role": "system", "content": "你是图书推荐助手，只返回 JSON。"},
                {"role": "user", "content": prompt}
            ], temperature=0.5)
            
            # 解析响应
            recommendations = json.loads(response)
            
            # 填充图书信息
            result = []
            for rec in recommendations[:limit]:
                book = db.query(Book).filter(Book.id == rec["id"]).first()
                if book:
                    result.append({
                        "id": book.id,
                        "title": book.title,
                        "author": book.author,
                        "cover_url": book.cover_url,
                        "reason": rec.get("reason", "为您推荐")
                    })
            return result
            
        except Exception as e:
            # 降级：返回未借过的图书
            borrowed_ids = [b.book_id for b in borrows]
            books = db.query(Book).filter(
                ~Book.id.in_(borrowed_ids) if borrowed_ids else True
            ).limit(limit).all()
            return [{"id": b.id, "title": b.title, "author": b.author,
                     "reason": "猜您可能感兴趣"} for b in books]
    
    async def semantic_search(self, query: str, db: Session, limit: int = 10) -> list[dict]:
        """语义搜索图书
        
        使用 Embedding 向量相似度搜索。
        """
        if not self._is_configured():
            # 降级到关键词搜索
            return self._keyword_search(query, db, limit)
        
        try:
            # 计算查询的 embedding
            query_embedding = np.array(await self._embed(query))
            
            # 获取所有图书并计算相似度
            books = db.query(Book).all()
            results = []
            
            for book in books:
                if book.embedding:
                    book_embedding = np.frombuffer(book.embedding, dtype=np.float32)
                    # 余弦相似度
                    similarity = np.dot(query_embedding, book_embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(book_embedding)
                    )
                    results.append({
                        "id": book.id,
                        "title": book.title,
                        "author": book.author,
                        "description": book.description[:100],
                        "cover_url": book.cover_url,
                        "score": float(similarity)
                    })
            
            # 按相似度排序
            results.sort(key=lambda x: x["score"], reverse=True)
            return results[:limit]
            
        except Exception:
            return self._keyword_search(query, db, limit)
    
    def _keyword_search(self, query: str, db: Session, limit: int) -> list[dict]:
        """关键词搜索（降级方案）"""
        books = db.query(Book).filter(
            Book.title.contains(query) |
            Book.author.contains(query) |
            Book.description.contains(query)
        ).limit(limit).all()
        
        return [{
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "description": b.description[:100],
            "cover_url": b.cover_url,
            "score": 0.5
        } for b in books]
    
    async def classify_book(self, title: str, description: str) -> dict:
        """智能分类图书"""
        if not self._is_configured():
            return {"categories": ["其他"], "confidence": 0.0}
        
        prompt = f"""根据以下图书信息，推荐分类标签（1-3个），并给出置信度（0-1）。

书名：{title}
简介：{description[:200]}

可选分类：文学、科幻、历史、科技、经济、教育、艺术、哲学、医学、法律、计算机、心理学、少儿、其他

返回 JSON 格式：
{{"categories": ["分类1", "分类2"], "confidence": 0.85}}"""

        try:
            response = await self._chat([
                {"role": "system", "content": "你是图书分类助手，只返回 JSON。"},
                {"role": "user", "content": prompt}
            ], temperature=0.3)
            return json.loads(response)
        except Exception:
            return {"categories": ["其他"], "confidence": 0.0}
    
    async def generate_summary(self, title: str, description: str) -> str:
        """生成图书摘要"""
        if not self._is_configured():
            return description[:200] if description else ""
        
        prompt = f"""请为以下图书生成一段简洁的摘要（100字以内）：

书名：{title}
简介：{description[:500]}

要求：突出核心内容，语言简洁优美。"""

        try:
            return await self._chat([
                {"role": "system", "content": "你是图书摘要生成助手。"},
                {"role": "user", "content": prompt}
            ], temperature=0.5)
        except Exception:
            return description[:200] if description else ""
    
    async def chat(self, user_message: str, context: str = "") -> str:
        """AI 对话助手"""
        if not self._is_configured():
            return "AI 助手暂未配置，请联系管理员。"
        
        system_prompt = """你是图书馆的 AI 助手，可以帮助读者：
1. 查找图书
2. 推荐书籍
3. 回答图书馆相关问题（借阅规则、开馆时间等）
4. 提供阅读建议

请用友好、专业的语气回答。如果不确定，请如实告知。"""
        
        if context:
            system_prompt += f"\n\n当前图书馆信息：{context}"
        
        try:
            return await self._chat([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ])
        except Exception:
            return "抱歉，AI 助手暂时无法回答，请稍后再试。"


# 全局单例
ai_service = AIService()
