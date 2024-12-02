from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    title: str
    author: str
    google_id: str
    description: Optional[str]
    genre: Optional[str]
    published_year: Optional[int]

class BookUpdate(BaseModel):
    title: Optional[str]
    author: Optional[str]
    google_id: Optional[str]
    description: Optional[str]
    genre: Optional[str]
    published_year: Optional[int]

class BookOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    author: str
    google_id: str
    genre: Optional[str]
    published_year: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
        from_attributes=True
