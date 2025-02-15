from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from app.database.session import get_db
from app.models.review import Review

router = APIRouter()

@router.get("/books/{book_id}/ai-summary")
async def generate_local_summary(book_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()

    if not reviews:
        return {"message": "Nenhuma review encontrada para este livro."}

    reviews_text = " ".join([r.review for r in reviews])

    parser = PlaintextParser.from_string(reviews_text, Tokenizer("portuguese"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 3)

    return {"ai_review": " ".join(str(sentence) for sentence in summary)}
