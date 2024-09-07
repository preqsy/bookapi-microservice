from fastapi import Depends
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from models import Book, BorrowedBook
from core.errors import MissingResources
from core.db import get_db
from datetime import datetime, timedelta


class CRUDBook:
    def __init__(self, db: Session):
        self._db = db
        self.model = Book

    def get_books(self, search: str, limit: int):
        query = (
            self._db.query(self.model)
            .filter(
                (self.model.title.contains(search.upper()))
                | (self.model.author.contains(search.lower()))
            )
            .filter(self.model.available == True)
            .limit(limit)
            .all()
        )
        return query if query else []

    def get_borrowed_books(self, limit: int = 100):
        query = (
            self._db.query(self.model)
            .filter(self.model.is_available == False)
            .limit(limit)
            .all()
        )
        return query if query else []

    def get_book_by_id_or_raise_exception(self, book_id: int):
        book = (
            self._db.query(self.model)
            .filter(self.model.id == book_id)
            .filter(self.model.is_available == True)
            .first()
        )
        if not book:
            raise MissingResources(
                f"Book with ISBN: {book_id} does not exist or has been borrowed"
            )
        return book

    def create_book(self, data: dict):
        new_book = self.model(**data)
        self._db.add(new_book)
        self._db.commit()
        self._db.refresh(new_book)
        return new_book

    def update_book(self, book_id: int, data: dict):
        book_query = self._db.query(self.model).filter(self.model.id == book_id)
        book = book_query.first()

        if not book:
            raise MissingResources(f"Book with ISBN: {book_id} does not exist")

        book_query.update(data, synchronize_session=False)
        self._db.commit()
        return book_query.first()

    def delete_book(self, book_id: int):
        book_query = self._db.query(self.model).filter(self.model.id == book_id)
        book = book_query.first()

        if not book:
            raise MissingResources(f"Book with ISBN: {book_id} does not exist")

        book_query.delete(synchronize_session=False)
        self._db.commit()
        return True

    def get_books_by_category(self, category: str, limit: int):
        query = (
            self._db.query(self.model)
            .filter(self.model.category == category)
            .limit(limit)
            .all()
        )
        return query if query else []

    def get_books_by_publisher(self, publisher: str, limit: int):
        query = (
            self._db.query(self.model)
            .filter(self.model.author == publisher)
            .limit(limit)
            .all()
        )
        return query if query else []


def get_crud_book(db: Session = Depends(get_db)) -> CRUDBook:
    return CRUDBook(db=db)
