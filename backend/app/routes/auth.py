from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.models.user import User
from app.database.session import get_db
from app.services.auth import AuthService
from app.core.security import create_access_token
from app.schemas.user import UserCreate, UserResponse, Token
from app.config import settings
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# OAuth setup with complete configuration
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile',
        'prompt': 'select_account'
    },
    authorize_params={
        'access_type': 'offline',
        'include_granted_scopes': 'true'
    }
)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    existing_user = db.query(User).filter(
        (User.email == user_data.email) |
        (User.username == user_data.username)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    user = await AuthService.create_user(db, user_data)
    return user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    user = await AuthService.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(user.id)
    return Token(access_token=access_token)

@router.get('/auth/google/init')
async def google_init(request: Request):
    """Initialize the OAuth flow by setting up the session"""
    try:
        # Generate and store state
        state = os.urandom(16).hex()
        request.session['oauth_state'] = state
        return JSONResponse({"status": "success", "state": state})
    except Exception as e:
        logger.error(f"Error in google_init: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get('/auth/google/login')
async def google_login(request: Request):
    """Start the Google OAuth flow"""
    try:
        redirect_uri = request.url_for('google_callback')
        return await oauth.google.authorize_redirect(
            request, 
            redirect_uri,
            access_type='offline'  # Request refresh token
        )
    except Exception as e:
        logger.error(f"Error in google_login: {str(e)}")
        return RedirectResponse(url="http://localhost:5173/login?error=oauth_init_failed")

@router.get('/auth/google/callback')
async def google_callback(request: Request, db: Session = Depends(get_db)):
    """Handle the OAuth callback"""
    try:
        logger.info(f"Callback received with query params: {dict(request.query_params)}")

        # Get the token
        token = await oauth.google.authorize_access_token(request)
        if not token:
            logger.error("No token received from Google")
            raise HTTPException(status_code=400, detail="No token received from Google")

        logger.info("Successfully received token from Google")

        # Get user info using the access token
        resp = await oauth.google.get('https://www.googleapis.com/oauth2/v3/userinfo', token=token)
        user_data = resp.json()
        logger.info(f"Successfully retrieved user info: {user_data}")

        # Extract user information
        google_user_id = user_data.get('sub')
        email = user_data.get('email')

        if not google_user_id or not email:
            logger.error("Missing required user information from Google response")
            raise HTTPException(status_code=400, detail="Incomplete user information")

        # Check if the user exists using google_id first
        existing_user = db.query(User).filter(User.google_id == google_user_id).first()

        if existing_user:
            logger.info(f"User found in database: {existing_user}")
            user_id = existing_user.id
        else:
            # If not found, check by email
            existing_user_by_email = db.query(User).filter(User.email == email).first()

            if existing_user_by_email:
                logger.info(f"User found in database by email: {existing_user_by_email}")
                existing_user_by_email.google_id = google_user_id  # Update google_id
                db.commit()
                user_id = existing_user_by_email.id
                logger.info(f"Updated user with google_id: {existing_user_by_email}")
            else:
                # If not, create a new user without a name
                new_user = User(email=email, username=email.split('@')[0], google_id=google_user_id)
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                user_id = new_user.id
                logger.info(f"New user created: {new_user}")

        # Generate your application's access token
        access_token = create_access_token(user_id)
        
        # Create and configure the response
        response = RedirectResponse(url="http://localhost:5173/home")
        response.set_cookie(
            key="session",
            value=access_token,
            httponly=True,
            secure=False,  # Set to True in production
            samesite="lax",
            max_age=3600
        )
        
        return response
        
    except Exception as e:
        logger.error(f"OAuth callback error: {str(e)}")
        error_details = str(e)
        return RedirectResponse(
            url=f"http://localhost:5173/login?error=oauth_callback_failed&details={error_details}"
        )