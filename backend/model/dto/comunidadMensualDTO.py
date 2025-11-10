from backend.model.base import Base
from sqlalchemy import Column, Integer

class ComunidadMensual(Base):
    __tablename__ = "comunidadesMensual"

    idComunidad = Column(Integer, primary_key=True, autoincrement=False)
    numPublicaciones = Column(Integer, nullable=False)
    numMiembros = Column(Integer, nullable=False)