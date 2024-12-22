from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    book_id: int
    user_id: int
    review_title: str
    review: str
    story_rating: int
    style_rating: int
    character_rating: int
    overall_rating: float
    recommendation: bool

class ReviewUpdate(BaseModel):
    pass

class ReviewOut(BaseModel):
    id: int
    book_id: int
    user_id: int
    review_title: str
    review: str
    overall_rating: float
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
