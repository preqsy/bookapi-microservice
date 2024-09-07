from fastapi import APIRouter
from .auth import router as auth_router
from .books import router as book_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(book_router)
