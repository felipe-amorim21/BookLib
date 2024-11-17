from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.routes import auth, api
from app.config import settings
from dotenv import load_dotenv
import os
from starlette.requests import Request

load_dotenv()


database_url = os.getenv("DATABASE_URL")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="Oe_Ef1Y38o1KSWM2R-s-Kg",
    session_cookie="session",
    max_age=60 * 60 * 24,
    same_site="lax",
    https_only=False
)


@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"  # Ou "*" durante testes
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@app.get("/")
async def read_root():
    return {"message": "Welcome to the BookReview API"}


app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["auth"])
app.include_router(api.router, prefix=settings.API_V1_PREFIX)
