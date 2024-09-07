from datetime import date
from typing import ClassVar, Optional
from pydantic import BaseModel, conint


class SearchCategories(BaseModel):
    category: str


class SearchPublisher(BaseModel):
    publisher: str


class BorrowedBookCreate(BaseModel):
    RETURN_DATE: ClassVar[str] = "return_date"

    user_id: int
    book_id: int
    days_to_borrow: conint(ge=1)
    due_date: Optional[date] = None
