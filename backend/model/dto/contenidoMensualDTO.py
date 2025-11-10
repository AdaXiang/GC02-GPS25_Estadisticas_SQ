from backend.model.base import Base
from sqlalchemy import Column, Integer, Float, Boolean

class ContenidoMensual(Base):
    __tablename__ = "contenidosMensual"

    idContenido = Column(Integer, primary_key=True, autoincrement=False)
    esAlbum = Column(Boolean, nullable=False)
    sumaValoraciones = Column(Float, nullable=False)
    numValoraciones = Column(Integer, nullable=False)
    numComentarios = Column(Integer, nullable=False)
    numReproducciones = Column(Integer, nullable=False)