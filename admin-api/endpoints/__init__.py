from fastapi import APIRouter
from .books import router as book_router

router = APIRouter()
router.include_router(book_router)
