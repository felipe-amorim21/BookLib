from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class Favorito(Base):
    __tablename__ = 'favoritos'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id')) 
    livro_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="favorites")
    livro = relationship("Book", back_populates="favorites")
