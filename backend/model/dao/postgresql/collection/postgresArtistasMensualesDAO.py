from backend.model.dao.postgresql.posgresConnector import SessionLocal
from backend.model.dao.postgresql.models import ArtistasMensual

class PostgresArtistasMensualesDAO:

    def upsert(self, id_artista: int, num_oyentes: int, valoracion_media: float):
        session = SessionLocal()
        try:
            fila = session.query(ArtistasMensual).filter_by(idartista=id_artista).first()

            if fila:
                fila.numoyentes = num_oyentes
                fila.valoracionmedia = valoracion_media
            else:
                fila = ArtistasMensual(
                    idartista=id_artista,
                    numoyentes=num_oyentes,
                    valoracionmedia=valoracion_media
                )
                session.add(fila)

            session.commit()
            session.refresh(fila)
            return fila

        except Exception as e:
            session.rollback()
            raise e

        finally:
            session.close()

    def obtener_por_id(self, id_artista: int):
        session = SessionLocal()
        try:
            return session.query(ArtistasMensual).filter_by(idartista=id_artista).first()
        finally:
            session.close()

    def obtener_ranking_oyentes(self, limite: int = 10):
        session = SessionLocal()
        try:
            return (
                session.query(ArtistasMensual)
                .order_by(ArtistasMensual.numoyentes.desc())
                .limit(limite)
                .all()
            )
        finally:
            session.close()
        


