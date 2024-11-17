from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from app.models.user import User
from app.database.session import get_db
from app.services.auth import AuthService
from app.core.security import create_access_token, verify_access_token, verify_google_token, decode_token_and_get_user_id
from app.schemas.user import UserCreate, UserResponse, Token
import os
import logging
from fastapi import Response

# Configuração de logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Configuração do Google OAuth
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
    authorize_params={"access_type": "offline", "include_granted_scopes": "true"},
    redirect_uri='http://localhost:8000/api/v1/auth/google/callback',
)

# Registro de novo usuário
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email ou usuário já registrado"
        )
    user = await AuthService.create_user(db, user_data)
    return user

# Login com autenticação local
@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    # Tentar autenticar o usuário
    user = await AuthService.authenticate_user(
        db, form_data.username, form_data.password
    )
    
    if not user:
        # Se o usuário não for encontrado, lança uma exceção
        logger.warning(f"Falha de login para o usuário {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Geração do token de acesso
    access_token = create_access_token(user.id)
    
    # Log de sucesso no login
    logger.info(f"Usuário {form_data.username} autenticado com sucesso.")
    
    # Criar o cookie com o token (httpOnly, secure, SameSite)
    response.set_cookie(
        key="access_token", 
        value=access_token,
        httponly=True,  # Garantir que o cookie não seja acessado via JavaScript
        secure=True,  # Garantir que o cookie seja enviado apenas em conexões HTTPS
        samesite="Strict",  # A restrição para que o cookie não seja enviado em requisições cross-site
        max_age=3600  # Tempo de expiração do cookie (1 hora)
    )

    # Retornar o token como resposta
    return Token(access_token=access_token)

@router.get("/auth/google/login")
async def google_login(request: Request):
    try:
        # Gerar um nonce único para o usuário
        nonce = os.urandom(16).hex()  # Pode ser qualquer valor único
        request.session['oauth_nonce'] = nonce  # Armazenar o nonce na sessão

        # Definir o URI de redirecionamento após login
        redirect_uri = request.url_for("google_callback")

        # Redirecionar para o Google OAuth, passando o nonce
        return await oauth.google.authorize_redirect(request, redirect_uri, access_type="offline", state=nonce)
    except Exception as e:
        logging.error(f"Erro no login com Google: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro no login com Google")

@router.get('/auth/google/callback')
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Handle the OAuth callback"""
    try:
        # Recuperar o nonce armazenado na sessão
        stored_nonce = request.session.get('oauth_nonce')
        received_nonce = request.query_params.get('state')  # O estado que o Google nos envia

        # Verificar se o nonce corresponde
        if stored_nonce != received_nonce:
            raise HTTPException(status_code=400, detail="Nonce mismatch: CSRF protection")

        # Obter o token de acesso do Google
        token = await oauth.google.authorize_access_token(request)
        if not token:
            raise HTTPException(status_code=400, detail="No token received from Google")

        # Obter informações do usuário do Google usando o token
        resp = await oauth.google.get('https://www.googleapis.com/oauth2/v3/userinfo', token=token)
        user_data = resp.json()

        google_user_id = user_data.get('sub')
        email = user_data.get('email')

        if not google_user_id or not email:
            raise HTTPException(status_code=400, detail="Invalid user information received from Google")

        # Verificar ou criar usuário no banco de dados
        existing_user = db.query(User).filter(User.google_id == google_user_id).first()

        if not existing_user:
            new_user = User(email=email, username=email.split('@')[0], google_id=google_user_id)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            existing_user = new_user

        # Criar o token de acesso
        access_token = create_access_token(existing_user.id)

        # Redirecionar para a página inicial com o cookie de autenticação
        response = RedirectResponse(url="http://localhost:5173/home")
        response.set_cookie(
            key="session",
            value=access_token,
            httponly=True,
            secure=False,  # Em produção, configure para True
            samesite="lax",
            max_age=3600
        )

        return response

    except Exception as e:
        logging.error(f"Erro ao processar o callback do Google: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/user/me")
def get_user_data(authorization: str = Depends(oauth2_scheme)):
    # Verifica se o token é um token válido do Google
    try:
        user = verify_google_token(authorization)
        if user:
            return user
    except Exception as e:
        # Se for um erro relacionado ao token do Google, ignora e continua
        pass  # O erro é ignorado aqui porque o fluxo continua tentando o JWT depois

    # Agora, tenta verificar o token JWT
    try:
        user = verify_access_token(authorization)
        if user:
            return user
    except Exception as e:
        # Em caso de erro ao verificar o JWT, lança um erro genérico de token inválido
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado.")

    # Caso ambos os tokens sejam inválidos, retorna um erro 401
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado.")