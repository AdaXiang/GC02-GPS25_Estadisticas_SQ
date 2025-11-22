from sqlalchemy import text
from backend.model.dto.busquedaArtistaDTO import BusquedaArtistaDTO
from backend.model.dao.interfaceBusquedasArtistasDao import InterfaceBusquedasArtistasDao
from sqlalchemy.orm import Session

class BusquedasArtistasDAO(InterfaceBusquedasArtistasDao):
    def __init__(self, db: Session):
        self.db = db  # Usamos la sesión recibida del Factory

    def insertar_o_actualizar_busqueda(self, id_artista: int, id_usuario: int | None = None):
        """
        Inserta o actualiza la búsqueda de un artista por parte de un usuario.
        """
        try:
            # Verificar si ya existe el registro
            sql_check = text("""
                SELECT COUNT(*) FROM busquedasartistas 
                WHERE idartista = :idartista AND idusuario = :idusuario
            """)
            result = self.db.execute(sql_check, {"idartista": id_artista, "idusuario": id_usuario}).fetchone()

            if result[0] > 0:  # Si el registro ya existe, actualizamos
                sql_update = text("""
                    UPDATE busquedasartistas
                    SET numbusquedas = numbusquedas + 1
                    WHERE idartista = :idartista AND idusuario = :idusuario
                """)
                self.db.execute(sql_update, {"idartista": id_artista, "idusuario": id_usuario})
            else:  # Si no existe, insertamos
                sql_insert = text("""
                    INSERT INTO busquedasartistas (idartista, idusuario)
                    VALUES (:idartista, :idusuario)
                """)
                self.db.execute(sql_insert, {"idartista": id_artista, "idusuario": id_usuario})

            self.db.commit()
        except Exception as e:
            print(f"Error al insertar o actualizar búsqueda: {e}")
            self.db.rollback()

    def get_top_artistas_busquedas(self, limit: int = 10):
        """
        Devuelve el top de artistas más buscados del mes (según la tabla `busquedasartistas`).
        """
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
                numBusquedas=r.num_busquedas
            )
            for r in rows
        ]

    def eliminar_busquedas_por_artista(self, id_artista: int) -> int:
        """Elimina todas las búsquedas relacionadas con un artista específico."""
        sql = text("DELETE FROM busquedasartistas WHERE idartista = :id")
        result = self.db.execute(sql, {"id": id_artista})
        return result.rowcount

    def eliminar_busquedas_por_usuario(self, id_usuario: int) -> int:
        """Elimina todas las búsquedas realizadas por un usuario específico."""
        sql = text("DELETE FROM busquedasartistas WHERE idusuario = :id")
        result = self.db.execute(sql, {"id": id_usuario})
        return result.rowcount