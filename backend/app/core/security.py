from datetime import datetime, timedelta
import logging
from typing import Any, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request
import google.auth
from google.oauth2 import id_token
from google.auth.transport import requests

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(subject: Union[str, Any]) -> str:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def decode_token_and_get_user_id(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")  
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,  settings.ALGORITHM)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def verify_google_token(token: str):
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request())
        return id_info
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid token: {e}")
    

def create_jwt_for_google_user(google_user_data):
    # Criar um token JWT para sua aplicação
    return create_access_token(subject=google_user_data['sub'])