"""图书数据模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from app.core.database import Base


class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False, index=True)
    isbn = Column(String(20), unique=True, index=True)
    publisher = Column(String(100), default="")
    publish_date = Column(String(20), default="")
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    description = Column(Text, default="")
    cover_url = Column(String(255), default="")
    location = Column(String(50), default="")
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    embedding = Column(LargeBinary, nullable=True)  # 存储向量
    ai_summary = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    category = relationship("Category", back_populates="books")
    borrows = relationship("Borrow", back_populates="book")


class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    description = Column(String(200), default="")
    
    books = relationship("Book", back_populates="category")
