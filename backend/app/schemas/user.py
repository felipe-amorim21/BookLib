from typing import Optional
from pydantic import BaseModel, EmailStr

# Base de modelos para usuários
class UserBase(BaseModel):
    """
    Modelo base para informações comuns entre os modelos de usuário.

    Atributos:
        email (EmailStr): Endereço de e-mail do usuário, validado automaticamente.
        username (str): Nome de usuário exclusivo.
    """
    email: EmailStr
    username: str


class UserCreate(UserBase):
    """
    Modelo para criação de novos usuários.

    Atributos:
        password (str): Senha do usuário.
    """
    password: str


class UserLogin(BaseModel):
    """
    Modelo para dados de autenticação de usuários.

    Atributos:
        email (EmailStr): Endereço de e-mail do usuário.
        password (str): Senha do usuário.
    """
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """
    Modelo para respostas de usuários na API.

    Atributos:
        id (int): Identificador único do usuário.
        is_active (bool): Indica se o usuário está ativo.
        profile_picture (Optional[str]): URL opcional para a imagem de perfil do usuário.
    """
    id: int
    is_active: bool
    profile_picture: Optional[str] = None

    class Config:
        """
        Configuração para o modelo Pydantic.

        Configurações:
            from_attributes (bool): Permite inicializar o modelo a partir de objetos do ORM.
        """
        from_attributes = True


class Token(BaseModel):
    """
    Modelo para tokens de autenticação.

    Atributos:
        access_token (str): Token de acesso gerado para o usuário.
        token_type (str): Tipo do token, padrão é 'bearer'.
    """
    access_token: str
    token_type: str = "bearer"
