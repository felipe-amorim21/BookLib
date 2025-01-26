from typing import Optional, Dict
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, get_password_hash
from app.schemas.user import UserCreate

class AuthService:
    """
    Serviço de autenticação e gerenciamento de usuários.

    Métodos disponíveis:
    - authenticate_user: Autentica um usuário com email e senha.
    - create_user: Cria um novo usuário no banco de dados.
    - get_or_create_google_user: Busca ou cria um usuário com base nos dados do Google.
    """

    @staticmethod
    async def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Autentica um usuário verificando email e senha.

        Parâmetros:
        - db (Session): Sessão do banco de dados.
        - email (str): Email do usuário.
        - password (str): Senha do usuário.

        Retorno:
        - Optional[User]: Usuário autenticado ou None se as credenciais forem inválidas.
        """
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        return user

    @staticmethod
    async def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Cria um novo usuário no banco de dados.

        Parâmetros:
        - db (Session): Sessão do banco de dados.
        - user_data (UserCreate): Dados para criação do usuário.

        Retorno:
        - User: Usuário criado.
        """
        hashed_password = get_password_hash(user_data.password)

        db_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hashed_password
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    async def get_or_create_google_user(db: Session, google_data: Dict[str, str]) -> User:
        """
        Busca ou cria um usuário com base nos dados do Google.

        Parâmetros:
        - db (Session): Sessão do banco de dados.
        - google_data (Dict[str, str]): Dados recebidos do Google.

        Retorno:
        - User: Usuário correspondente aos dados fornecidos.
        """
        user = db.query(User).filter(User.google_id == google_data["sub"]).first()
        
        if user is None:
            user = User(
                email=google_data["email"],
                username=google_data["email"].split("@")[0],
                google_id=google_data["sub"],
                profile_picture=google_data.get("picture")
            )

            db.add(user)
            db.commit()
            db.refresh(user)

        return user
