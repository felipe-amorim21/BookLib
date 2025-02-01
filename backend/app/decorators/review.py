from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.review import Review
from functools import wraps

def moderate_review(func):
    """Decorator para filtrar palavras ofensivas em um review"""
    def wrapper( db: Session, review_data, *args, **kwargs):
        review_text = review_data.review  
        banned_words = ["porra", "merda", "caralho"]
        for word in banned_words:
            review_text = review_text.replace(word, "***")
        review_data.review = review_text 
        return func(db, review_data, *args, **kwargs)
    return wrapper


def check_review_owner(func):
    """Decorator para garantir que o usuário só pode modificar seus próprios reviews"""
    @wraps(func)
    def wrapper(review_id: int, user_id: int, db: Session, *args, **kwargs):
        review = db.query(Review).filter(Review.id == review_id).first()
        if not review:
            raise HTTPException(status_code=404, detail="Review não encontrado")
        if review.user_id != user_id:
            raise HTTPException(status_code=403, detail="Ação não permitida. Você não é o dono desse review.")
        return func(review_id, user_id, db, *args, **kwargs)

    return wrapper