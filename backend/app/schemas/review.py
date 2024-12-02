from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    book_id: int
    user_id: int
    review: str
    rating: int = Field(..., ge=1, le=5)

class ReviewUpdate(BaseModel):
    review: Optional[str]
    rating: Optional[int] = Field(None, ge=1, le=5)

class ReviewOut(BaseModel):
    id: int
    book_id: int
    user_id: int
    review: str
    rating: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
