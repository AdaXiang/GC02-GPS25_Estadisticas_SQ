from sqlalchemy import text
from backend.model.dto.contenidoDTO import ContenidoDTO
from backend.model.dao.interfaceContenidoDao import InterfaceContenidoDao

class PostgresContenidoDAO(InterfaceContenidoDao):
    def __init__(self, db):
        self.db = db
        
    def _map_row_to_dto(self, row) -> ContenidoDTO:
        """Helper para mapear fila a DTO"""
        return ContenidoDTO(
            idcontenido=row.idcontenido,
            numventas=int(row.numventas or 0),
            esalbum=row.esalbum,
            sumavaloraciones=float(row.sumavaloraciones or 0),
            numcomentarios=int(row.numcomentarios or 0),
            genero=row.genero,
            esnovedad=row.esnovedad
        )

    def obtener_todos(self) -> list[ContenidoDTO]:
        try:
            sql = text("""
                SELECT idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios, genero, esnovedad
                FROM contenidosmensual
            """)
            result = self.db.execute(sql).fetchall()
            return [self._map_row_to_dto(row) for row in result]
        except Exception as e:
            print(f"❌ Error DAO Contenido obtener_todos: {e}")
            raise e

    def actualizar_o_insertar(self, dto: ContenidoDTO) -> bool:
        try:
            sql_check = text("SELECT idcontenido FROM contenidosmensual WHERE idcontenido = :id")
            existe = self.db.execute(sql_check, {"id": dto.idContenido}).fetchone()

            if existe:
                sql_update = text("""
                    UPDATE contenidosmensual
                    SET numventas = :nr, esalbum = :ea, sumavaloraciones = :sv,
                        numcomentarios = :nc, genero = :gen, esnovedad = :nov
                    WHERE idcontenido = :id
                """)
                self.db.execute(sql_update, {
                    "id": dto.idContenido, "nr": dto.numVentas, "ea": dto.esAlbum,
                    "sv": dto.sumaValoraciones, "nc": dto.numComentarios,
                    "gen": dto.genero, "nov": dto.esNovedad
                })
            else:
                sql_insert = text("""
                    INSERT INTO contenidosmensual (idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios, genero, esnovedad)
                    VALUES (:id, :nr, :ea, :sv, :nc, :gen, :nov)
                """)
                self.db.execute(sql_insert, {
                    "id": dto.idContenido, "nr": dto.numVentas, "ea": dto.esAlbum,
                    "sv": dto.sumaValoraciones, "nc": dto.numComentarios,
                    "gen": dto.genero, "nov": dto.esNovedad
                })
            
            return True
        except Exception as e:
            print(f"❌ Error DAO Contenido Upsert: {e}")
            raise e

    def obtener_por_id(self, id_contenido: int) -> ContenidoDTO | None:
        try:
            sql = text("""
                SELECT idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios, genero, esnovedad
                FROM contenidosmensual
                WHERE idcontenido = :id
            """)
            row = self.db.execute(sql, {"id": id_contenido}).fetchone()
            return self._map_row_to_dto(row) if row else None
        except Exception as e:
            print(f"❌ Error DAO Contenido obtener_id: {e}")
            raise e

    def eliminar(self, id_contenido: int) -> bool:
        try:
            sql = text("DELETE FROM contenidosmensual WHERE idcontenido = :id")
            result = self.db.execute(sql, {"id": id_contenido})
            return result.rowcount > 0
        except Exception as e:
            print(f"❌ Error DAO Contenido eliminar: {e}")
            raise e
    
    def get_top_valorados(self, limit: int) -> list[ContenidoDTO]:
        try:
            sql = text("""
                SELECT idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios, genero, esnovedad
                FROM contenidosmensual
                ORDER BY sumavaloraciones DESC
                LIMIT :lim
            """)
            result = self.db.execute(sql, {"lim": limit}).fetchall()
            return [self._map_row_to_dto(row) for row in result]
        except Exception as e:
            print(f"❌ Error DAO Contenido Top Valorados: {e}")
            raise e

    def get_top_comentados(self, limit: int) -> list[ContenidoDTO]:
        try:
            sql = text("""
                SELECT idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios, genero, esnovedad
                FROM contenidosmensual
                ORDER BY numcomentarios DESC
                LIMIT :lim
            """)
            result = self.db.execute(sql, {"lim": limit}).fetchall()
            return [self._map_row_to_dto(row) for row in result]
        except Exception as e:
            print(f"❌ Error DAO Contenido Top Comentados: {e}")
            raise e

    def get_top_vendidos(self, limit: int) -> list[ContenidoDTO]:
        try:
            sql = text("""
                SELECT idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios, genero, esnovedad
                FROM contenidosmensual
                ORDER BY numventas DESC
                LIMIT :lim
            """)
            result = self.db.execute(sql, {"lim": limit}).fetchall()
            return [self._map_row_to_dto(row) for row in result]
        except Exception as e:
            print(f"❌ Error DAO Contenido Top Vendidos: {e}")
            raise e
    
    def get_top_generos_por_ventas(self, limit: int):
        """
        Este devuelve una lista de diccionarios personalizada (no DTO de contenido)
        porque agrega datos por género.
        """
        try:
            sql = text("""
                SELECT genero, SUM(numventas) as total_ventas
                FROM contenidosmensual
                WHERE genero IS NOT NULL AND genero != 'Desconocido'
                GROUP BY genero
                ORDER BY total_ventas DESC
                LIMIT :lim
            """)
            result = self.db.execute(sql, {"lim": limit}).fetchall()
            
            return [
                {"genero": row.genero, "totalVentas": int(row.total_ventas or 0)}
                for row in result
            ]
        except Exception as e:
            print(f"❌ Error DAO Contenido Top Generos: {e}")
            raise e