from datetime import datetime, timedelta
import hashlib
import base64
import os
from typing import Annotated
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from schemas import UserCreate, DecodedToken
from models import User
from config import get_settings

ALGORITHM = "HS256"
# openssl rand -hex 32 で作成
SECRET_KEY = get_settings().secret_key
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_user(db: Session, user_create: UserCreate):
    username = user_create.username
    email = user_create.email
    password = user_create.password
    overlap_email = db.query(User).filter(User.email == email).first()
    overlap_username = db.query(User).filter(User.username == username).first()
    if overlap_username:
        raise HTTPException(status_code=400, detail='Username is already taken')
    if overlap_email:
        raise HTTPException(status_code=400, detail='Email is already taken')
    if not password or len(password) < 6:
        raise HTTPException(status_code=400, detail="Password too short")
    salt = base64.b64encode(os.urandom(32))
    hashed_password = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt, 1000
    ).hex()
    new_user = User(
        username=username,
        email=email,
        password=hashed_password,
        salt=salt.decode(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    hashed_password = hashlib.pbkdf2_hmac("sha256", password.encode(), user.salt.encode(), 1000).hex()
    if user.password != hashed_password:
        return None
    return user

def create_access_token(username: str, email: str, user_id: int, expires_delta: timedelta):
    expires = datetime.now() + expires_delta
    payload = {"sub": username, "id": user_id, "email": email, "exp": expires}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        email = payload.get('email')
        user_id = payload.get('id')
        print(username)
        if username is None or user_id is None:
            return None
        return DecodedToken(username=username, email=email, user_id=user_id)
    except JWTError:
        raise JWTError

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()