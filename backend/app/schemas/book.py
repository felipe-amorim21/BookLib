from pydantic import BaseModel, Field, conint
from typing import Optional
from datetime import datetime

class BookCreate(BaseModel):
    """
    Classe para criar um novo livro. Todos os campos são obrigatórios.
    """
    title: str = Field(..., description="Título do livro.")
    author: str = Field(..., description="Autor do livro.")
    google_id: str = Field(..., description="ID do livro no Google Books.")
    description: Optional[str] = Field(None, description="Descrição do livro.")
    genre: Optional[str] = Field(None, description="Gênero do livro.")
    published_year: Optional[int] = Field(None, 
                                           ge=0, 
                                           le=datetime.now().year, 
                                           description="Ano de publicação do livro (não pode ser negativo ou maior que o ano atual).")
    thumbnail: Optional[str] = Field(None, description="URL da imagem da capa do livro.")                                       

class BookUpdate(BaseModel):
    """
    Classe para atualizar um livro existente. Todos os campos são opcionais.
    """
    title: Optional[str] = Field(None, description="Título do livro.")
    author: Optional[str] = Field(None, description="Autor do livro.")
    google_id: Optional[str] = Field(None, description="ID do livro no Google Books.")
    description: Optional[str] = Field(None, description="Descrição do livro.")
    genre: Optional[str] = Field(None, description="Gênero do livro.")
    published_year: Optional[int] = Field(None, 
                                           ge=0, 
                                           le=datetime.now().year, 
                                           description="Ano de publicação do livro (não pode ser negativo ou maior que o ano atual).")
    thumbnail: Optional[str] = Field(None, description="URL da imagem da capa do livro.")

class BookOut(BaseModel):
    """
    Classe de saída para retornar as informações do livro. Usada na resposta da API.
    """
    id: int = Field(..., description="ID do livro.")
    title: str = Field(..., description="Título do livro.")
    description: Optional[str] = Field(None, description="Descrição do livro.")
    author: str = Field(..., description="Autor do livro.")
    google_id: str = Field(..., description="ID do livro no Google Books.")
    genre: Optional[str] = Field(None, description="Gênero do livro.")
    published_year: Optional[int] = Field(None, 
                                           ge=0, 
                                           le=datetime.now().year, 
                                           description="Ano de publicação do livro (não pode ser negativo ou maior que o ano atual).")
    created_at: datetime = Field(..., description="Data de criação do registro.")
    updated_at: Optional[datetime] = Field(None, description="Data de última atualização do registro.")
    thumbnail: Optional[str] = Field(None, description="URL da imagem da capa do livro.")

    class Config:
        orm_mode = True
        from_attributes = True
