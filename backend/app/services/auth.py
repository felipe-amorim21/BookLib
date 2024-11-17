from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, get_password_hash
from app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    async def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    async def create_user(db: Session, user_data: UserCreate) -> User:
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
    async def get_or_create_google_user(
        db: Session,
        google_data: dict
    ) -> User:
        user = db.query(User).filter(User.google_id == google_data["sub"]).first()
        if not user:
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
