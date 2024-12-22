from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.sql import func
from app.database.session import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    review_title = Column(String, nullable=False) 
    review = Column(String, nullable=False)
    story_rating = Column(Integer, nullable=False)
    style_rating = Column(Integer, nullable=False)
    character_rating = Column(Integer, nullable=False) 
    overall_rating = Column(Float, nullable=False) 
    recommendation = Column(Boolean, default=False)  
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
