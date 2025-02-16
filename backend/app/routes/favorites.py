from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.favorite import Favorito
from app.database.session import get_db
from app.factory.factories import BookFactory
from app.decorators.book import cache_response
from app.models.user import User
from app.routes.api import get_current_user

router = APIRouter()

# Função para favoritar livro
@router.post("/favoritar/{livro_id}")
def favoritar(livro_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Adiciona um livro aos favoritos de um usuário.
    
    - livro_id: ID do livro a ser favoritado.
    - user_id: ID do usuário que está favoritando o livro.
    """
    favorito = db.query(Favorito).filter(Favorito.user_id == user_id, Favorito.livro_id == livro_id).first()
    if favorito:
        raise HTTPException(status_code=400, detail="Você já favoritou este livro")
    
    # Adiciona o livro aos favoritos
    novo_favorito = Favorito(user_id=user_id, livro_id=livro_id)
    db.add(novo_favorito)
    db.commit()
    db.refresh(novo_favorito)
    
    return {"message": "Livro favoritado com sucesso!"}


# Função para desfavoritar livro
@router.delete("/desfavoritar/{livro_id}")
def desfavoritar(livro_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Remove um livro dos favoritos de um usuário.
    
    - livro_id: ID do livro a ser desfavoritado.
    - user_id: ID do usuário que está desfavoritando o livro.
    """
    favorito = db.query(Favorito).filter(Favorito.user_id == user_id, Favorito.livro_id == livro_id).first()
    
    if not favorito:
        raise HTTPException(status_code=404, detail="Favorito não encontrado")
    
    db.delete(favorito)
    db.commit()
    
    return {"message": "Livro desfavoritado com sucesso!"}


# Função para listar os favoritos do usuário
@router.get("/favoritos")
def get_favoritos(user_id: int, db: Session = Depends(get_db)):
    """
    Lista os livros favoritos de um usuário.
    
    - user_id: ID do usuário cujos favoritos serão listados.
    """
    favoritos = db.query(Book).join(Favorito).filter(Favorito.user_id == user_id).all()
    
    if not favoritos:
        raise HTTPException(status_code=404, detail="Nenhum livro favorito encontrado")
    
    return favoritos


@router.get("/favoritos/{livro_id}")
def check_favorito(livro_id: int, user_id: int, db: Session = Depends(get_db)):
    """
    Verifica se o livro já foi favoritado pelo usuário.
    
    - livro_id: ID do livro a ser verificado.
    """
    favorito = db.query(Favorito).filter(Favorito.user_id == user_id, Favorito.livro_id == livro_id).first()
    
    if favorito:
        return {"isFavorito": True}
    return {"isFavorito": False}
