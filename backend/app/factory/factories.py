from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.review import Review
from app.models.user import User
from app.schemas.book import BookCreate
from app.schemas.review import ReviewCreate
from fastapi import HTTPException

class BookFactory:
    @staticmethod
    def create_book(db: Session, book_data: BookCreate) -> Book:
        """Cria um novo livro e salva no banco de dados."""
        book = Book(**book_data.model_dump())  # Converte Pydantic para dict
        db.add(book)
        db.commit()
        db.refresh(book)
        return book

class ReviewFactory:
    @staticmethod
    def calculate_overall_rating(story_rating: int, style_rating: int, character_rating: int) -> float:
        """Calcula a média das avaliações."""
        return (story_rating + style_rating + character_rating) / 3.0

    @staticmethod
    def create_review(db: Session, review_data: ReviewCreate) -> Review:
        """Cria um novo review, verificando se o livro e o usuário existem."""
        book = db.query(Book).filter(Book.id == review_data.book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")

        user = db.query(User).filter(User.id == review_data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        overall_rating = ReviewFactory.calculate_overall_rating(
            review_data.story_rating, review_data.style_rating, review_data.character_rating
        )

        review = Review(**review_data.model_dump(exclude={"overall_rating"}), overall_rating=overall_rating)
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
