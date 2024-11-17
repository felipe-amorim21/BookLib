from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import UserResponse
from app.models.user import User 
from app.config import settings
from app.schemas.user import UserResponse, UserLogin
from app.core.security import create_access_token, verify_password, decode_token_and_get_user_id, oauth2_scheme, verify_access_token
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
    
    access_token = create_access_token(subject=user.id) 
    return {"access_token": access_token, "token_type": "bearer"}



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


# Rota para obter informações do usuário autenticado
@router.get("/user/me")
async def get_user_info(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Verificar se o token é válido e obter os dados do usuário
        user_id = verify_access_token(token)  # Função que decodifica o token e retorna o ID do usuário
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        return {
            "username": user.username,
            "email": user.email,
            # Adicione outras informações que você queira retornar
        }

    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


@router.post("/google-auth")
async def google_auth(
    user_data: dict,
    db: Session = Depends(get_db)
):
    """Create or update user from Google OAuth data"""
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