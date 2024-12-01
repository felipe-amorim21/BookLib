from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate, BookOut
from app.database.session import get_db



router = APIRouter(prefix="/books", tags=["Books"])

@router.post("/", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.get("/", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book não encontrado")
    return book

@router.get("/google/{google_id}", response_model=BookOut)
def get_book_by_google_id(google_id: str, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.google_id == google_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book não encontrado")
    return BookOut.from_orm(book)

@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, book_update: BookUpdate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book não encontrado")
    for key, value in book_update.dict(exclude_unset=True).items():
        setattr(book, key, value)
    db.commit()
    db.refresh(book)
    return book

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book não encontrado")
    db.delete(book)
    db.commit()
    return {"message": "Book deletado com sucesso"}
