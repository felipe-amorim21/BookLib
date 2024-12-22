from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.models.review import Review
from app.models.book import Book
from app.models.user import User
from app.schemas.review import ReviewCreate, ReviewUpdate, ReviewOut
from app.database.session import get_db

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewOut)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == review.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book não encontrado")

    user = db.query(User).filter(User.id == review.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User não encontrado")

    overall_rating = (
        review.story_rating + review.style_rating + review.character_rating
    ) / 3.0

    new_review = Review(
        **review.dict(exclude={"overall_rating"}),
        overall_rating=overall_rating, 
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review


@router.get("/", response_model=list[ReviewOut])
def list_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()


@router.get("/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrado")
    return review


@router.put("/{review_id}", response_model=ReviewOut)
def update_review(review_id: int, review_update: ReviewUpdate, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrado")

    for key, value in review_update.dict(exclude_unset=True).items():
        setattr(review, key, value)

    if any(
        key in {"story_rating", "style_rating", "character_rating"}
        for key in review_update.dict(exclude_unset=True)
    ):
        review.overall_rating = (
            review.story_rating + review.style_rating + review.character_rating
        ) / 3.0

    db.commit()
    db.refresh(review)
    return review


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review não encontrado")
    db.delete(review)
    db.commit()
    return {"message": "Review deletado com sucesso"}


@router.get("/books/{book_id}")
async def get_reviews_by_book_id(book_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    if not reviews:
        return []

    return [
        {
            "id": review.id,
            "review_title": review.review_title,
            "review": review.review,
            "story_rating": review.story_rating,
            "style_rating": review.style_rating,
            "character_rating": review.character_rating,
            "overall_rating": review.overall_rating,
            "recommendation": review.recommendation,
        }
        for review in reviews
    ]
