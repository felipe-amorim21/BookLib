from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import UserResponse
from app.models.user import User  # Adjust the import based on your actual model structure
#from app.services.user import UserService  # You might want to create a service for user-related operations
from app.config import settings
from app.schemas.user import UserResponse, UserLogin
from app.core.security import create_access_token, verify_password, decode_token_and_get_user_id, oauth2_scheme
from jose import JWTError, jwt
from app.config import settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@router.get("/users", response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return


@router.post("/token")
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user or not verify_password(user_login.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    # Create JWT token
    access_token = create_access_token(subject=user.id)  # Assuming user.id is the identifier
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=UserResponse)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = decode_token_and_get_user_id(token)  # Get user ID from token

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


async def get_user_from_token(token: str, db: Session):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/{user_id}")
async def get_user(
    user_id: str,
    db: Session = Depends(get_db),
    token: str = Depends(lambda x: x.headers.get("Authorization").split(" ")[1])
):
    """Get user by ID"""
    try:
        # Verify the token and get the requesting user
        requesting_user = await get_user_from_token(token, db)
        
        # Get the requested user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Convert the user object to a dictionary
        user_data = {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "name": user.name if hasattr(user, 'name') else user.username,
            # Add any other fields you want to expose
        }
        
        return user_data
        
    except Exception as e:
        logger.error(f"Error getting user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user data"
        )

# Add this route to get user info from Google OAuth
@router.post("/google-auth")
async def google_auth(
    user_data: dict,
    db: Session = Depends(get_db)
):
    """Create or update user from Google OAuth data"""
    try:
        # Check if user exists
        user = db.query(User).filter(User.email == user_data["email"]).first()
        
        if not user:
            # Create new user
            user = User(
                email=user_data["email"],
                username=user_data["email"].split("@")[0],  # Use email prefix as username
                name=user_data.get("name", ""),
                # Add other fields as needed
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        return {
            "id": str(user.id),
            "email": user.email,
            "username": user.username,
            "name": user.name if hasattr(user, 'name') else user.username,
        }
        
    except Exception as e:
        logger.error(f"Error in google_auth: {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing Google authentication"
        )