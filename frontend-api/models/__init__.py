from .auth_user import AuthUser
from .book import Book
from core.db import engine

auth_user.Base.metadata.create_all(bind=engine)
