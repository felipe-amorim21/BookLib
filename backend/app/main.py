from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from app.routes import auth, api
from app.config import settings
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the database URL from environment variable
database_url = os.getenv("DATABASE_URL")



app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key= "Oe_Ef1Y38o1KSWM2R-s-Kg",
    session_cookie="session",
    max_age=60 * 60 * 24,  # 1 day in seconds
    same_site="lax",  # Important for security
    https_only=False  # Set to True in production
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the BookReview API"}

# Routes
app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["auth"])
app.include_router(api.router, prefix=settings.API_V1_PREFIX)