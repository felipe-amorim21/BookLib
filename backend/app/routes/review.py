from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.review import Review
from app.models.book import Book
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewOut
from app.database.session import get_db
from app.factory.factories import ReviewFactory
from app.decorators.review import check_review_owner
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/reviews", tags=["Reviews"])

def calculate_overall_rating(story_rating: int, style_rating: int, character_rating: int) -> float:
    """
    Calculate the overall rating for a review based on story, style, and character ratings.
    """
    return (story_rating + style_rating + character_rating) / 3.0

@router.post("/", response_model=ReviewOut)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """
    Create a new review for a book. This route checks if the book and user exist,
    calculates the overall rating, and saves the new review to the database.
    """
    new_review = ReviewFactory.create_review(db, review)
    return new_review

@router.get("/", response_model=list[ReviewOut])
def list_reviews(db: Session = Depends(get_db)):
    """
    List all reviews from the database.
    """
    return db.query(Review).all()

@router.get("/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    """
    Get a specific review by its ID.
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review

@router.put("/{review_id}", response_model=ReviewOut)
def update_review(review_id: int, review_update: ReviewUpdate, db: Session = Depends(get_db)):
    """
    Update an existing review. The overall rating is recalculated if any of the rating fields change.
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    for key, value in review_update.dict(exclude_unset=True).items():
        setattr(review, key, value)

    if any(
        key in {"story_rating", "style_rating", "character_rating"}
        for key in review_update.dict(exclude_unset=True)
    ):
        review.overall_rating = calculate_overall_rating(
            review.story_rating, review.style_rating, review.character_rating
        )

    db.commit()
    db.refresh(review)
    return review

@router.delete("/{review_id}", response_model=None)
@check_review_owner
def delete_review(review_id: int, db: Session = Depends(get_db)):
    """
    Delete a review by its ID.
    """
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    db.delete(review)
    db.commit()
    return JSONResponse(status_code=204, content={"message": "Review deleted successfully"})

@router.get("/books/{book_id}", response_model=list[ReviewOut])
async def get_reviews_by_book_id(book_id: int, db: Session = Depends(get_db)):
    """
    Get all reviews for a specific book by its ID.
    This route returns a list of reviews using the ReviewOut model.
    """
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    if not reviews:
        return []

    return reviews