from sqlalchemy import text
from backend.model.dto.busquedaArtistaDTO import BusquedaArtistaDTO

class BusquedasArtistasDAO:
    def __init__(self, db):
        self.db = db

    def insertar_o_actualizar_busqueda(self, id_artista: int, id_usuario: int | None = None):
        try:
            sql_check = text("""
                SELECT COUNT(*) FROM busquedasartistas 
                WHERE idartista = :idartista AND idusuario = :idusuario
            """)
            # Nota: .scalar() es mejor que fetchone()[0] para conteos
            count = self.db.execute(sql_check, {"idartista": id_artista, "idusuario": id_usuario}).scalar()

            if count > 0:
                sql_update = text("""
                    UPDATE busquedasartistas
                    SET numbusquedas = numbusquedas + 1
                    WHERE idartista = :idartista AND idusuario = :idusuario
                """)
                self.db.execute(sql_update, {"idartista": id_artista, "idusuario": id_usuario})
            else:
                sql_insert = text("""
                    INSERT INTO busquedasartistas (idartista, idusuario)
                    VALUES (:idartista, :idusuario)
                """)
                self.db.execute(sql_insert, {"idartista": id_artista, "idusuario": id_usuario})

            self.db.commit()
        except Exception as e:
            print(f"❌ Error DAO Busquedas Insert/Update: {e}")
            self.db.rollback()
            raise e

    def get_top_artistas_busquedas(self, limit: int = 10) -> list[BusquedaArtistaDTO]:
        try:
            sql = text("""
                SELECT idartista, COUNT(*) AS num_busquedas
                FROM busquedasartistas
                GROUP BY idartista
                ORDER BY num_busquedas DESC
                LIMIT :limit
            """)
            rows = self.db.execute(sql, {"limit": limit}).fetchall()

            return [
                BusquedaArtistaDTO(
                    idartista=r.idartista,
                    numBusquedas=r.num_busquedas # Verifica si tu SQL devuelve esto o count(*)
                )
                for r in rows
            ]
        except Exception as e:
             print(f"❌ Error DAO Top Busquedas: {e}")
             raise e

    def eliminar_busquedas_por_artista(self, id_artista: int) -> int:
        sql = text("DELETE FROM busquedasartistas WHERE idartista = :id")
        result = self.db.execute(sql, {"id": id_artista})
        return result.rowcount

    def eliminar_busquedas_por_usuario(self, id_usuario: int) -> int:
        sql = text("DELETE FROM busquedasartistas WHERE idusuario = :id")
        result = self.db.execute(sql, {"id": id_usuario})
        return result.rowcount