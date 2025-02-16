from pydantic import BaseModel
from typing import Optional

class FavoritoBase(BaseModel):
    user_id: int
    livro_id: int

    class Config:
        orm_mode = True

class FavoritoCreate(FavoritoBase):
    pass

class Favorito(FavoritoBase):
    id: int
    user_id: int
    livro_id: int

    class Config:
        orm_mode = True
