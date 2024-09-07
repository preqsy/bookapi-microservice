from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from schemas import (
    AuthUserCreate,
    RegisterAuthUserResponse,
    LoginResponse,
)

from crud import CRUDAuthUser, get_crud_auth_user
from core.errors import ResourcesExist, InvalidRequest
from core.tokens import generate_access_token

from utils.password_utils import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=RegisterAuthUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    data_obj: AuthUserCreate,
    crud_auth_user: CRUDAuthUser = Depends(get_crud_auth_user),
):

    data_obj.email = data_obj.email.lower()
    email = crud_auth_user.get_by_email(data_obj.email)
    if email:
        raise ResourcesExist("Email Exists")
    data_obj.password = hash_password(data_obj.password)
    new_user = crud_auth_user.create_user(data_obj)

    access_token = generate_access_token(user_id=new_user.id)

    new_user_dict = data_obj.model_dump()
    new_user_dict["id"] = new_user.id
    return RegisterAuthUserResponse(auth_user=new_user_dict, access_token=access_token)


@router.post(
    "/login", status_code=status.HTTP_201_CREATED, response_model=LoginResponse
)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    crud_auth_user: CRUDAuthUser = Depends(get_crud_auth_user),
):
    user_query = crud_auth_user.get_by_email(email=form_data.username)
    if not user_query:
        raise InvalidRequest("Incorrect Credentials")

    if not verify_password(
        plain_password=form_data.password, hashed_password=user_query.password
    ):
        raise InvalidRequest("Incorrect Credentials")
    access_token = generate_access_token(user_id=user_query.id)
    return {"access_token": access_token}


@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(
    skip: int,
    limit: int,
    crud_auth_user: CRUDAuthUser = Depends(get_crud_auth_user),
):
    return crud_auth_user.list_users()
