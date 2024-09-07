from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime
from models import Book
from core.errors import MissingResources
from core.db import get_db


class CRUDBook:
    def __init__(self, db: Session):
        self._db = db
        self.model = Book

    def get_books(self, search: str, limit: int):
        query = (
            self._db.query(self.model)
            .filter(
                (self.model.title.contains(search.upper()))
                | (self.model.authors.contains(search.lower()))
            )
            .filter(self.model.is_deleted == False)
            .limit(limit)
            .all()
        )
        return query

    def get_book_by_id(self, book_id: int):
        book = self._db.query(self.model).filter(self.model.id == book_id).first()
        if not book:
            raise MissingResources(f"Book with ISBN: {book_id} does not exist")
        return book

    def create_book(self, data: dict, authors: str):
        new_book = self.model(authors=authors, **data)
        self._db.add(new_book)
        self._db.commit()
        self._db.refresh(new_book)
        return new_book

    def update_book(self, book_id: int, data: dict, current_user: str):
        book_query = self._db.query(self.model).filter(self.model.id == book_id)
        book = book_query.first()

        if not book:
            raise MissingResources(f"Book with ISBN: {book_id} does not exist")

        if book.authors != current_user:
            raise MissingResources("You do not have permission to update this book")

        book_query.update(data, synchronize_session=False)
        self._db.commit()
        return book_query.first()

    def delete_book(self, book_id: int, current_user: str):
        book_query = self._db.query(self.model).filter(self.model.id == book_id)
        book = book_query.first()

        if not book:
            raise MissingResources(f"Book with ISBN: {book_id} does not exist")

        if book.authors != current_user:
            raise MissingResources("You do not have permission to delete this book")

        book_query.delete(synchronize_session=False)
        self._db.commit()
        return True

    def get_books_by_category(self, category: str, limit: int):
        return (
            self._db.query(self.model)
            .filter(self.model.categories == category)
            .limit(limit)
            .all()
        )


def get_crud_book(db: Session = Depends(get_db)) -> CRUDBook:
    return CRUDBook(db=db)
