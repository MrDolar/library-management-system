"""借阅数据模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base


class Borrow(Base):
    __tablename__ = "borrows"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False, index=True)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(Enum("borrowed", "returned", "overdue", name="borrow_status"), default="borrowed")
    renew_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", backref="borrows")
    book = relationship("Book", back_populates="borrows")


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    comment = Column(String(500), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
