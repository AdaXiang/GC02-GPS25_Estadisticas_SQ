from sqlalchemy import Column, Integer
from backend.model.dao.postgresql.posgresConnector import Base

class ArtistasMensual(Base):
    __tablename__ = "artistasmensual"

    idartista = Column("idartista", Integer, primary_key=True)
    numoyentes = Column("numoyentes", Integer)
    valoracionmedia = Column("valoracionmedia", Integer)
