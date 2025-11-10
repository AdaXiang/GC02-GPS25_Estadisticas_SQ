from backend.model.base import Base
from sqlalchemy import Column, Integer

class GeneroMensual(Base):
    __tablename__ = "generosMensual"

    idGenero = Column(Integer, primary_key=True, autoincrement=False)
    numReproducciones = Column(Integer, nullable=False)
    numFavoritos = Column(Integer, nullable=False)