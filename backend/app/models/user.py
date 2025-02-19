from sqlalchemy import Boolean, Column, Integer, String
from app.database.session import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    google_id = Column(String, unique=True, nullable=True)
    favorites = relationship("Favorito", back_populates="user")
