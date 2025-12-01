from sqlalchemy import text
from backend.model.dto.artistaMensualDTO import ArtistaMensualDTO
from backend.model.dao.interfaceArtistasMensualesDao import InterfaceArtistasMensualesDao

class PostgresArtistasMensualesDAO(InterfaceArtistasMensualesDao):
    
    def __init__(self, db):
        self.db = db

    def actualizar_o_insertar(self, dto: ArtistaMensualDTO) -> bool:
        """
        Inserta o actualiza un registro usando el DTO estandarizado.
        """
        try:
            # Comprobar si existe
            sql_check = text("SELECT idartista FROM artistasmensual WHERE idartista = :id")
            existe = self.db.execute(sql_check, {"id": dto.idArtista}).fetchone()

            if existe:
                # UPDATE
                sql_update = text("""
                    UPDATE artistasmensual
                    SET numoyentes = :no, valoracionmedia = :vm
                    WHERE idartista = :id
                """)
                self.db.execute(sql_update, {
                    "id": dto.idArtista, 
                    "no": dto.numOyentes, 
                    "vm": dto.valoracionMedia
                })
            else:
                # INSERT
                sql_insert = text("""
                    INSERT INTO artistasmensual (idartista, numoyentes, valoracionmedia)
                    VALUES (:id, :no, :vm)
                """)
                self.db.execute(sql_insert, {
                    "id": dto.idArtista, 
                    "no": dto.numOyentes, 
                    "vm": dto.valoracionMedia
                })

            return True

        except Exception as e:
            print(f"❌ Error DAO Artistas Upsert: {e}")
            raise e

    def obtener_todos(self) -> list[ArtistaMensualDTO]:
        try:
            sql = text("SELECT idartista, numoyentes, valoracionmedia FROM artistasmensual")
            result = self.db.execute(sql).fetchall()

            return [
                ArtistaMensualDTO(
                    idartista=row.idartista,
                    numOyentes=row.numoyentes,
                    valoracionmedia=row.valoracionmedia
                ) for row in result
            ]

        except Exception as e:
            print(f"❌ Error DAO Artistas Obtener Todos: {e}")
            raise e
        
    def obtener_por_id(self, id_artista: int) -> ArtistaMensualDTO | None:
        try:
            sql = text("SELECT idartista, numoyentes, valoracionmedia FROM artistasmensual WHERE idartista = :id")
            row = self.db.execute(sql, {"id": id_artista}).fetchone()

            if not row:
                return None

            return ArtistaMensualDTO(
                idartista=row.idartista,
                numOyentes=row.numoyentes,
                valoracionmedia=row.valoracionmedia
            )
        except Exception as e:
            print(f"❌ Error DAO Artistas Obtener ID: {e}")
            raise e

    def obtener_ranking_oyentes(self, limite: int = 10) -> list[ArtistaMensualDTO]:
        try:
            sql = text("""
                SELECT idartista, numoyentes, valoracionmedia
                FROM artistasmensual
                ORDER BY numoyentes DESC
                LIMIT :lim
            """)
            result = self.db.execute(sql, {"lim": limite}).fetchall()

            return [
                ArtistaMensualDTO(
                    idartista=row.idartista,
                    numOyentes=row.numoyentes,
                    valoracionmedia=row.valoracionmedia
                ) for row in result
            ]
        except Exception as e:
            print(f"❌ Error DAO Artistas Ranking: {e}")
            raise e