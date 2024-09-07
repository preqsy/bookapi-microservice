from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer

from core import settings
from core.db import get_db
from core.errors import CredentialException, InvalidRequest
from models import AuthUser

from pydantic import BaseModel


class TokenData(BaseModel):
    auth_id: int


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def encode_jwt(payload: dict, expiry_time: timedelta):
    data_to_encode = payload.copy()
    expiration_time = datetime.utcnow() + expiry_time
    data_to_encode.update({"exp": expiration_time})
    token = jwt.encode(data_to_encode, settings.JWT_SECRET_KEY, settings.ALGORITHM)
    return token


def generate_access_token(user_id):
    payload = {
        "user_id": user_id,
        "type": "access",
    }
    access_token = encode_jwt(
        payload=payload,
        expiry_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY_TIME),
    )
    return access_token


def verify_access_token(token):

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.ALGORITHM)
        user_id = payload.get("user_id")
        if not user_id:
            CredentialException("invalid token")
        token_data = TokenData(auth_id=user_id)
    except InvalidTokenError:
        raise CredentialException("Invalid token")
    return token_data


def get_current_auth_user(
    token=Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> AuthUser:

    token = verify_access_token(token)
    auth_user = db.query(AuthUser).filter(AuthUser.id == token.auth_id).first()
    if not auth_user:
        raise CredentialException("User not found")
    if not auth_user.email_verified:
        raise InvalidRequest("Complete your registration")
    return auth_user
