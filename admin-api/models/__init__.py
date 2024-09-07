from .book import Book, BorrowedBook
from core.db import engine

book.Base.metadata.create_all(bind=engine)
