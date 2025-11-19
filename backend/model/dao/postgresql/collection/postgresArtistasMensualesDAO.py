from sqlalchemy import text
from backend.model.dto.artistaMensualDTO import ArtistaMensualDTO
from backend.model.dao.interfaceArtistasMensualesDao import InterfaceArtistasMensualesDao


class PostgresArtistasMensualesDAO(InterfaceArtistasMensualesDao):
    
    def __init__(self, db):
        self.db = db  # Usamos la sesión recibida del Factory, como en el otro DAO

# ...existing code...
    def upsert(self, id_artista: int, num_oyentes: int = 0, valoracion_media: int = 0) -> bool:
        """
        Inserta o actualiza un registro de artista mensual.
        Acepta parámetros individuales en lugar de un DTO.
        """
        try:
            # Comprobar si el artista existe
            sql_select = text("""
                SELECT idartista FROM artistasmensual
                WHERE idartista = :id
            """)
            res = self.db.execute(sql_select, {"id": id_artista}).fetchone()  # Trae una fila o None

            if res:
                # Si el artista existe, actualizar los datos
                sql_update = text("""
                    UPDATE artistasmensual
                    SET numoyentes = :num, valoracionmedia = :val
                    WHERE idartista = :id
                """)
                self.db.execute(sql_update, {"id": id_artista, "num": num_oyentes, "val": valoracion_media})
                print(f"✅ Artista {id_artista} actualizado")
            else:
                # Si el artista no existe, insertar un nuevo registro
                sql_insert = text("""
                    INSERT INTO artistasmensual (idartista, numoyentes, valoracionmedia)
                    VALUES (:id, :num, :val)
                """)
                self.db.execute(sql_insert, {"id": id_artista, "num": num_oyentes, "val": valoracion_media})
                print(f"✅ Artista {id_artista} insertado")

            # Commit de la transacción
            self.db.commit()
            return True  # Se devolvió 'True' indicando que la operación fue exitosa

        except Exception as e:
            # Si hay un error, revertir la transacción
            self.db.rollback()
            print(f"❌ Error al actualizar/insertar artista {id_artista}: {e}")
            return False  # Retornamos False en caso de error


# ...existing code...

    def obtener_por_id(self, id_artista: int) -> ArtistaMensualDTO | None:
        sql = text("""
            SELECT idartista, numoyentes, valoracionmedia
            FROM artistasmensual
            WHERE idartista = :id
        """)
        row = self.db.execute(sql, {"id": id_artista}).fetchone()

        if not row:
            return None

        return ArtistaMensualDTO(
            idartista=row.idartista,
            numOyentes=row.numoyentes,
            valoracionmedia=row.valoracionmedia
        )

    def obtener_ranking_oyentes(self, limite: int = 10):
        sql = text("""
            SELECT idartista, numoyentes, valoracionmedia
            FROM artistasmensual
            ORDER BY numoyentes DESC
            LIMIT :lim
        """)
        rows = self.db.execute(sql, {"lim": limite}).fetchall()

        return [
            ArtistaMensualDTO(
                idartista=r.idartista,
                numOyentes=r.numoyentes,
                valoracionmedia=r.valoracionmedia
            )
            for r in rows
        ]
