from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException, Form, Response, Request, Header
from sqlalchemy.orm import Session
from starlette import status
from cruds import auth as auth_cruds
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from schemas import UserCreate, UserResponse, Msg, Token, DecodedToken
from database import get_db
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["auth"])
DbDependency = Annotated[Session, Depends(get_db)]

FormDependency = Annotated[OAuth2PasswordRequestForm, Depends()]

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(db: DbDependency, user_create: UserCreate):
    return auth_cruds.create_user(db, user_create)

@router.post("/login", response_model=Union[Msg, Token], status_code=status.HTTP_200_OK)
async def login(response: Response, db: DbDependency, form_data: FormDependency):
    user = auth_cruds.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = auth_cruds.create_access_token(
        user.username, user.email, user.id, timedelta(minutes=20)
    )
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: Annotated[DecodedToken, Depends(auth_cruds.get_current_user)], db: DbDependency):
    user = auth_cruds.get_user_by_id(db, user_id=current_user.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user