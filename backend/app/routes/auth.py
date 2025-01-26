from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from app.models.user import User
from app.database.session import get_db
from app.services.auth import AuthService
from app.core.security import create_access_token, verify_access_token, verify_google_token
from app.schemas.user import UserCreate, UserResponse, Token
import os
import logging
from fastapi import Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

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


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    """
    Register a new user.
    Checks if the user already exists using the email or username.
    If a user already exists, raises a 400 error.
    """
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email or username already registered"
        )
    user = await AuthService.create_user(db, user_data)
    logger.info(f"User {user_data.username} registered successfully.")
    return user


@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    """
    Login with username and password.
    Authenticates the user and returns a token. If credentials are incorrect, raises a 401 error.
    """
    user = await AuthService.authenticate_user(
        db, form_data.username, form_data.password
    )

    if not user:
        logger.warning(f"Failed login attempt for user {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(user.id)

    logger.info(f"User {form_data.username} authenticated successfully.")
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Strict",
        max_age=3600
    )

    return Token(access_token=access_token)


@router.get("/auth/google/login")
async def google_login(request: Request):
    """
    Redirects to the Google OAuth login page.
    Initializes the OAuth flow and sets a nonce for CSRF protection.
    """
    try:
        nonce = os.urandom(16).hex()
        request.session['oauth_nonce'] = nonce

        redirect_uri = request.url_for("google_callback")

        return await oauth.google.authorize_redirect(request, redirect_uri, access_type="offline", state=nonce)
    except Exception as e:
        logging.error(f"Error during Google login: {str(e)}")
        raise HTTPException(status_code=500, detail="Error during Google login")


@router.get('/auth/google/callback')
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """
    Handle the callback after Google OAuth authentication.
    Verifies the nonce to prevent CSRF attacks, retrieves user data, and creates or logs in the user.
    """
    try:
        stored_nonce = request.session.get('oauth_nonce')
        received_nonce = request.query_params.get('state')

        if stored_nonce != received_nonce:
            raise HTTPException(status_code=400, detail="Nonce mismatch: CSRF protection")

        token = await oauth.google.authorize_access_token(request)
        if not token:
            raise HTTPException(status_code=400, detail="No token received from Google")

        resp = await oauth.google.get('https://www.googleapis.com/oauth2/v3/userinfo', token=token)
        user_data = resp.json()

        google_user_id = user_data.get('sub')
        email = user_data.get('email')

        if not google_user_id or not email:
            raise HTTPException(status_code=400, detail="Invalid user information received from Google")

        existing_user = db.query(User).filter(User.google_id == google_user_id).first()

        if not existing_user:
            new_user = User(email=email, username=email.split('@')[0], google_id=google_user_id)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            existing_user = new_user

        access_token = create_access_token(existing_user.id)

        response = RedirectResponse(url="http://localhost:5173/home")
        response.set_cookie(
            key="session",
            value=access_token,
            httponly=True,
            secure=True,  # Set to True in production for added security
            samesite="Lax",
            max_age=3600
        )

        logger.info(f"User {existing_user.username} logged in via Google OAuth.")
        return response

    except Exception as e:
        logging.error(f"Error during Google callback: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/user/me")
def get_user_data(authorization: str = Depends(oauth2_scheme)):
    """
    Retrieve the currently authenticated user's data using either a Google or regular access token.
    If token is invalid or expired, raises a 401 error.
    """
    try:
        user = verify_google_token(authorization)
        if user:
            return user
    except Exception as e:
        logger.error(f"Google token verification failed: {e}")
        pass 

    try:
        user = verify_access_token(authorization)
        if user:
            return user
    except Exception as e:
        logger.error(f"Access token verification failed: {e}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")
