from __future__ import annotations


from pydantic import BaseModel, EmailStr


class AuthUserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str


class AuthUserCreate(AuthUserBase):
    password: str


class RegisterAuthUserResponse(BaseModel):
    auth_user: AuthUserBase
    access_token: str


class LoginResponse(BaseModel):
    access_token: str
