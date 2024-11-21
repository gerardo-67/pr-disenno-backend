from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from app.exceptions.already_in_db_error import AlreadyInDatabaseError
from app.exceptions.not_found_error import NotFoundError

from app.schemas import UserOut, UserIn, UserUpdate
from app.schemas.user_schema import UserLogin, UserPassword
from app.services import UserService

user_router = APIRouter(prefix="/users")

@user_router.get("", status_code=status.HTTP_200_OK)
def get_users(user_service: UserService = Depends(UserService)):
    try:
        return user_service.get_users()
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@user_router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, user_service: UserService = Depends(UserService)):
    try:
        return user_service.get_user(user_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@user_router.get("/by-email/{email}", status_code=status.HTTP_200_OK)
def get_user(email: str, user_service: UserService = Depends(UserService)):
    try:
        return user_service.get_user_by_email(email)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@user_router.post("", status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn, user_service: UserService = Depends(UserService)):
    try:
        return user_service.create_user(user)
    except AlreadyInDatabaseError as e:
        raise HTTPException(status_code=409, detail=str(e))

@user_router.post("/login", status_code=status.HTTP_200_OK)
def login_user(user_login: UserLogin, user_service: UserService = Depends(UserService)):
    try:
        return user_service.validate_user(user_login.email, user_login.password)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@user_router.put("/password", status_code=status.HTTP_200_OK)
def change_password(user_password: UserPassword, user_service: UserService = Depends(UserService)):
    try:
        return user_service.change_password(user_password.user_id, user_password.password)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
