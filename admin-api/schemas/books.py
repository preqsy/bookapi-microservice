from datetime import date, datetime
from enum import Enum
from typing import ClassVar, Optional

from pydantic import BaseModel, conint


class Categories(str, Enum):
    FICTION = "fiction"
    FANTASY = "fantasy"
    DYSTOPIAN = "dystopian"
    ADVENTURE = "adventure"
    ROMANCE = "Romance"
    MYSTERY = "mystery"
    HORROR = "horror"
    THRILLER = "thriller"
    HISTORICAL = "historical"
    BIOGRAPHY = "biography"
    COOKING = "cooking"
    ART = "art"
    PHOTOGRAPHY = "photography"
    PERSONAL_DEVELOPMENT = "personal development"
    MOTIVATIONAL = "motivational"
    EDUCATION_ = "education"
    TRAVEL = "travel"
    SPIRITUALITY = "spirituality"


class BookCreate(BaseModel):
    title: str
    page_count: int
    description: str
    category: Categories
    author: str


class BookResponse(BaseModel):
    id: int
    title: str
    description: str


class BookOut(BookResponse):
    category: str
    published_date: datetime
    page_count: int
    author: str


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


class BorrowedBookReturn(BookOut):
    is_available: bool
    available_date: Optional[date] = None


class Borrowed(BaseModel):
    borrowed: bool = True
