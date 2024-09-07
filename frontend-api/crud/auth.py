from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.orm import Session

from core.db import get_db
from models import AuthUser


class CRUDAuthUser:
    def __init__(self, db: Session):
        self._db = db
        self.model = AuthUser

    def get_by_email(self, email: EmailStr):
        email_query = (
            self._db.query(self.model).filter(self.model.email == email.lower()).first()
        )
        return email_query if email_query else None

    def create_user(self, data_obj):
        new_user = self.model(**data_obj.model_dump())
        self._db.add(new_user)
        self._db.commit()
        self._db.refresh(new_user)
        return new_user

    def list_users(self, skip: int = 0, limit=20) -> list[AuthUser] | list:
        users = self._db.query(self.model).offset(skip).limit(limit).all()
        return users if users else []


def get_crud_auth_user(db=Depends(get_db)):
    return CRUDAuthUser(db=db)
