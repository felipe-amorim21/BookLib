from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookOut
from app.database.session import get_db

router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book.
    This endpoint creates a new book in the database.
    """
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    """
    List all books.
    This endpoint retrieves all books from the database.
    """
    return db.query(Book).all()

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """
    Get a book by its ID.
    This endpoint retrieves a book from the database by its ID.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/google/{google_id}", response_model=BookOut)
def get_book_by_google_id(google_id: str, db: Session = Depends(get_db)):
    """
    Get a book by its Google ID.
    This endpoint retrieves a book from the database by its Google ID.
    """
    book = db.query(Book).filter(Book.google_id == google_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book  # Simplified: directly return the Book object as response

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    """
    Update an existing book by its ID.
    This endpoint updates the fields of an existing book based on the provided input.
    Only the fields specified in the request are updated.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """
    Delete a book by its ID.
    This endpoint deletes a book from the database.
    """
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}
