from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ReviewCreate(BaseModel):
    """
    Schema for creating a new review. All fields are mandatory.
    """
    book_id: int = Field(..., description="ID of the book being reviewed")
    user_id: int = Field(..., description="ID of the user creating the review")
    review_title: str = Field(..., description="Title of the review")
    review: str = Field(..., description="Content of the review")
    story_rating: int = Field(..., ge=1, le=5, description="Rating for the story (1 to 5)")
    style_rating: int = Field(..., ge=1, le=5, description="Rating for the style (1 to 5)")
    character_rating: int = Field(..., ge=1, le=5, description="Rating for the characters (1 to 5)")
    overall_rating: float = Field(..., ge=1, le=5, description="Overall rating (1.0 to 5.0)")
    recommendation: bool = Field(..., description="Indicates if the user recommends the book")

class ReviewUpdate(BaseModel):
    """
    Schema for updating an existing review. All fields are optional.
    """
    book_id: Optional[int] = Field(None, description="ID of the book being reviewed")
    user_id: Optional[int] = Field(None, description="ID of the user updating the review")
    review_title: Optional[str] = Field(None, description="Title of the review")
    review: Optional[str] = Field(None, description="Content of the review")
    story_rating: Optional[int] = Field(None, ge=1, le=5, description="Rating for the story (1 to 5)")
    style_rating: Optional[int] = Field(None, ge=1, le=5, description="Rating for the style (1 to 5)")
    character_rating: Optional[int] = Field(None, ge=1, le=5, description="Rating for the characters (1 to 5)")
    overall_rating: Optional[float] = Field(None, ge=1, le=5, description="Overall rating (1.0 to 5.0)")
    recommendation: Optional[bool] = Field(None, description="Indicates if the user recommends the book")

class ReviewOut(BaseModel):
    """
    Schema for API responses. Includes timestamps and IDs.
    """
    id: int = Field(..., description="Unique identifier for the review")
    book_id: int = Field(..., description="ID of the book being reviewed")
    user_id: int = Field(..., description="ID of the user who created the review")
    review_title: str = Field(..., description="Title of the review")
    review: str = Field(..., description="Content of the review")
    story_rating: Optional[int] = Field(None, ge=1, le=5, description="Rating for the story (1 to 5)")
    style_rating: Optional[int] = Field(None, ge=1, le=5, description="Rating for the style (1 to 5)")
    character_rating: Optional[int] = Field(None, ge=1, le=5, description="Rating for the characters (1 to 5)")
    overall_rating: float = Field(..., ge=1, le=5, description="Overall rating (1.0 to 5.0)")
    recommendation: bool = Field(..., description="Whether the reviewer recommends the book or not")
    created_at: datetime = Field(..., description="Timestamp when the review was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the review was last updated")

    class Config:
        orm_mode = True
