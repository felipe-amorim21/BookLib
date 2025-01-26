from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.config import settings
from app.schemas.user import UserResponse, UserLogin
from app.core.security import create_access_token, verify_password, oauth2_scheme, verify_access_token
from jose import JWTError, jwt
import logging

#router = APIRouter(prefix="/api")
router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.
    
    - user_id: ID of the user to retrieve.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User with id {user_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    logger.info(f"User with id {user_id} retrieved successfully.")
    return user


@router.get("/users", response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    """
    Retrieve a list of all users.
    """
    users = db.query(User).all()
    logger.info(f"Retrieved {len(users)} users.")
    return users


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by their ID.
    
    - user_id: ID of the user to delete.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User with id {user_id} not found for deletion.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    logger.info(f"User with id {user_id} deleted successfully.")
    return


@router.post("/token")
async def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password.
    
    - user_login: The login credentials (email and password).
    """
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user or not verify_password(user_login.password, user.password):
        logger.error(f"Incorrect email or password for {user_login.email}.")
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(subject=user.id)
    logger.info(f"User {user.email} logged in successfully.")
    return {"access_token": access_token, "token_type": "bearer"}


async def get_user_from_token(token: str, db: Session):
    """
    Retrieve user from the token.
    
    - token: The JWT token used to retrieve user data.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            logger.error("Invalid token, missing user ID.")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except JWTError as e:
        logger.error(f"JWT decode error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        logger.error(f"User with id {user_id} not found.")
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Rota para obter informações do usuário autenticado
@router.get("/user/me")
async def get_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieve information about the currently authenticated user.
    
    - token: The JWT token used to authenticate the user.
    """
    try:
        user_id = verify_access_token(token)
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            logger.error("Authenticated user not found.")
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        logger.info(f"Authenticated user info retrieved: {user.email}.")
        return {
            "username": user.username,
            "email": user.email,
            # Adicione outras informações que você queira retornar
        }

    except Exception as e:
        logger.error(f"Error retrieving user info: {str(e)}")
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


@router.post("/google-auth")
async def google_auth(user_data: dict, db: Session = Depends(get_db)):
    """
    Create or update user from Google OAuth data.
    
    - user_data: The user information retrieved from Google OAuth.
    """
    try:
        user = db.query(User).filter(User.email == user_data["email"]).first()
        if not user:
            user = User(
                email=user_data["email"],
                username=user_data["email"].split("@")[0],
                name=user_data.get("name", ""),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"User {user.email} created via Google OAuth.")
        else:
            logger.info(f"User {user.email} already exists, logged in via Google OAuth.")

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
