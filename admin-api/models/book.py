from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text

from core.db import Base

from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean
from datetime import datetime


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    page_count = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    published_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    author = Column(String, nullable=False)
    is_available = Column(Boolean, nullable=False, server_default="TRUE")
    available_date = Column(DateTime)
    category = Column(String, nullable=False)


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    user_id = Column(Integer, nullable=False)
    days_to_borrow = Column(Integer, nullable=False)
    due_date = Column(DateTime, nullable=False)
    borrowed_date = Column(DateTime, default=datetime.utcnow)
