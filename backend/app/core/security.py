from datetime import datetime, timedelta
from typing import Any, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.config import settings
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from google.oauth2 import id_token
from google.auth.transport import requests
import logging

# Configuração do contexto de criptografia e esquema OAuth2
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuração de log para monitoramento de erros
logger = logging.getLogger(__name__)

def create_access_token(subject: Union[str, Any]) -> str:
    """
    Cria um token de acesso JWT com o sujeito especificado e uma expiração configurada.

    Args:
        subject (Union[str, Any]): O sujeito do token, geralmente o ID do usuário.

    Returns:
        str: O token JWT gerado.
    """
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha fornecida corresponde à senha criptografada.

    Args:
        plain_password (str): A senha fornecida pelo usuário.
        hashed_password (str): A senha armazenada no banco de dados.

    Returns:
        bool: Verdadeiro se as senhas corresponderem, caso contrário, falso.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Gera o hash da senha fornecida.

    Args:
        password (str): A senha a ser criptografada.

    Returns:
        str: O hash da senha.
    """
    return pwd_context.hash(password)


def decode_token_and_get_user_id(token: str) -> int:
    """
    Decodifica o token JWT e retorna o ID do usuário contido nele.

    Args:
        token (str): O token JWT a ser decodificado.

    Returns:
        int: O ID do usuário extraído do token.

    Raises:
        HTTPException: Se o token for inválido ou o ID do usuário não puder ser encontrado.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            logger.error("Token não contém o campo 'sub' com o ID do usuário.")
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_id
    except JWTError:
        logger.error("Erro ao decodificar o token JWT.")
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_access_token(token: str):
    """
    Verifica a validade de um token JWT.

    Args:
        token (str): O token JWT a ser verificado.

    Returns:
        dict: O payload do token decodificado.

    Raises:
        HTTPException: Se o token for inválido.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("sub") is None:
            logger.error("Token inválido: campo 'sub' ausente.")
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return payload
    except JWTError:
        logger.error("Erro ao verificar o token JWT.")
        raise HTTPException(status_code=401, detail="Invalid token")


def verify_google_token(token: str):
    """
    Verifica a validade de um token do Google OAuth2.

    Args:
        token (str): O token do Google a ser verificado.

    Returns:
        dict: As informações do usuário do Google extraídas do token.

    Raises:
        HTTPException: Se o token for inválido.
    """
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request())
        if "sub" not in id_info:
            logger.error("Token do Google inválido: campo 'sub' ausente.")
            raise HTTPException(status_code=400, detail="Invalid Google token")
        return id_info
    except ValueError as e:
        logger.error(f"Erro ao verificar o token do Google: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid Google token: {e}")


def create_jwt_for_google_user(google_user_data: dict) -> str:
    """
    Cria um token JWT para um usuário autenticado via Google OAuth2.

    Args:
        google_user_data (dict): Os dados do usuário retornados pelo Google após a autenticação.

    Returns:
        str: O token JWT gerado para o usuário do Google.
    """
    return create_access_token(subject=google_user_data['sub'])
