from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.routes import auth, api, book, review, ia, favorites
from app.config import settings
from dotenv import load_dotenv
import os
from starlette.requests import Request
from typing import List

def load_environment_variables() -> None:
    """Carrega variáveis de ambiente do arquivo .env e valida seu carregamento."""
    if not load_dotenv():
        raise RuntimeError("Falha ao carregar variáveis de ambiente do arquivo .env")

def validate_environment_variables(required_vars: List[str]) -> None:
    """Valida a presença de variáveis de ambiente essenciais."""
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"{var} não está configurada nas variáveis de ambiente")

# Carregar e validar variáveis de ambiente
load_environment_variables()
validate_environment_variables(["DATABASE_URL", "SECRET_KEY"])

# Obter URL do banco de dados e chave secreta
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")


ALLOWED_ORIGINS = ["http://localhost:5173"]
SESSION_COOKIE_NAME = "session"
SESSION_MAX_AGE = 60 * 60 * 24


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

def configure_cors(app: FastAPI) -> None:
    """Configura o middleware de CORS."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def configure_session(app: FastAPI, secret_key: str) -> None:
    """Configura o middleware de sessão."""
    app.add_middleware(
        SessionMiddleware,
        secret_key=secret_key,
        session_cookie=SESSION_COOKIE_NAME,
        max_age=SESSION_MAX_AGE,
        same_site="lax",
        https_only=False,
    )

# Configurar middlewares
configure_cors(app)
configure_session(app, SECRET_KEY)

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    """Middleware para adicionar cabeçalhos CORS extras."""
    response = await call_next(request)
    response.headers.update({
        "Access-Control-Allow-Origin": ALLOWED_ORIGINS[0],
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, Authorization",
    })
    return response


@app.get("/")
async def read_root():
    """Endpoint raiz da aplicação."""
    return {"message": "Welcome to the BookReview API"}


app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["auth"])
app.include_router(api.router, prefix=settings.API_V1_PREFIX)
app.include_router(book.router, prefix=settings.API_V1_PREFIX)
app.include_router(review.router, prefix=settings.API_V1_PREFIX)
app.include_router(ia.router, prefix=settings.API_V1_PREFIX)
app.include_router(favorites.router, prefix=settings.API_V1_PREFIX)
