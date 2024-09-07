from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime
from models import Book, BorrowedBook
from core.errors import MissingResources
from core.db import get_db


class CRUDBorrowBook:
    def __init__(self, db: Session):
        self._db = db
        self.model = BorrowedBook

    def borrow_book(self, data_dict: dict):
        borrowed_book = self.model(**data_dict)
        self._db.add(borrowed_book)
        self._db.commit()

        return borrowed_book

    def return_book(db: Session, borrowed_book_id: int):
        borrowed_book = (
            db.query(BorrowedBook).filter(BorrowedBook.id == borrowed_book_id).first()
        )
        if not borrowed_book:
            raise MissingResources()

        borrowed_book.days_to_borrow = datetime.utcnow()
        borrowed_book.is_returned = True

        # Update the book's availability
        book = db.query(Book).filter(Book.id == borrowed_book.book_id).first()
        if book:
            book.available = True
            db.commit()

        return borrowed_book

    def get_user_borrowed_books(db: Session, user_id: int):
        return db.query(BorrowedBook).filter(BorrowedBook.user_id == user_id).all()

    def get_books_not_available(db: Session):
        return (
            db.query(Book)
            .join(BorrowedBook, Book.id == BorrowedBook.book_id)
            .filter(Book.available == False)
            .all()
        )


def get_crud_borrowed_book(db: Session = Depends(get_db)) -> CRUDBorrowBook:
    return CRUDBorrowBook(db=db)
