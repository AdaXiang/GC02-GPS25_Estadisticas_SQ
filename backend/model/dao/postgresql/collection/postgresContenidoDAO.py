from sqlalchemy import text
from backend.model.dto.contenidoDTO import ContenidoDTO
from backend.model.dao.interfaceContenidoDao import InterfaceContenidoDao

class PostgresContenidoDAO(InterfaceContenidoDao):
    def __init__(self, db):
        self.db = db
        
    def obtener_todos(self) -> list[ContenidoDTO]:
        sql = text("""
            SELECT idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios, genero, esnovedad
            FROM contenidosmensual
        """)
        result = self.db.execute(sql)
        contenidos = []
        for row in result:
            contenidos.append(ContenidoDTO(
                idcontenido=row.idcontenido,
                numventas=int(row.numventas or 0),
                esalbum=row.esalbum,
                sumavaloraciones=int(row.sumavaloraciones or 0),
                numcomentarios=int(row.numcomentarios or 0),
                genero=row.genero,
                esnovedad=row.esnovedad # <--- Mapeo
            ))
        return contenidos

    def actualizar_o_insertar(self, dto: ContenidoDTO) -> bool:
        try:
            sql_check = text("SELECT idcontenido FROM contenidosmensual WHERE idcontenido = :id")
            existe = self.db.execute(sql_check, {"id": dto.idContenido}).fetchone()

            if existe:
                # UPDATE completo
                sql_update = text("""
                    UPDATE contenidosmensual
                    SET numventas = :nr,
                        esalbum = :ea,
                        sumavaloraciones = :sv,
                        numcomentarios = :nc,
                        genero = :gen,
                        esnovedad = :nov  -- <--- Campo nuevo
                    WHERE idcontenido = :id
                """)
                self.db.execute(sql_update, {
                    "id": dto.idContenido,
                    "nr": dto.numVentas,
                    "ea": dto.esAlbum,
                    "sv": dto.sumaValoraciones,
                    "nc": dto.numComentarios,
                    "gen": dto.genero,
                    "nov": dto.esNovedad # <--- Valor
                })
            else:
                # INSERT completo
                sql_insert = text("""
                    INSERT INTO contenidosmensual (idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios, genero, esnovedad)
                    VALUES (:id, :nr, :ea, :sv, :nc, :gen, :nov)
                """)
                self.db.execute(sql_insert, {
                    "id": dto.idContenido,
                    "nr": dto.numVentas,
                    "ea": dto.esAlbum,
                    "sv": dto.sumaValoraciones,
                    "nc": dto.numComentarios,
                    "gen": dto.genero,
                    "nov": dto.esNovedad
                })
            
            return True

        except Exception as e:
            print(f"❌ Error DB DAO: {e}")
            raise e

    def obtener_por_id(self, id_contenido: int) -> ContenidoDTO | None:
        sql = text("""
            SELECT idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios, genero, esnovedad
            FROM contenidosmensual
            WHERE idcontenido = :id
        """)
        row = self.db.execute(sql, {"id": id_contenido}).fetchone()

        if not row:
            return None

        return ContenidoDTO(
            idcontenido=row.idcontenido,
            numventas=int(row.numventas or 0),
            esalbum=row.esalbum,
            sumavaloraciones=float(row.sumavaloraciones or 0),
            numcomentarios=int(row.numcomentarios or 0),
            genero=row.genero,
            esnovedad=row.esnovedad
        )

    def eliminar(self, id_contenido: int) -> bool:
        sql = text("DELETE FROM contenidosmensual WHERE idcontenido = :id")
        result = self.db.execute(sql, {"id": id_contenido})
        return result.rowcount > 0
    
    def get_top_valorados(self, limit: int):
        """ Top por sumaValoraciones DESC """
        sql = text("""
            SELECT idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios
            FROM contenidosmensual
            ORDER BY sumavaloraciones DESC
            LIMIT :lim
        """)
        return self.db.execute(sql, {"lim": limit}).fetchall()

    def get_top_comentados(self, limit: int):
        """ Top por numComentarios DESC """
        sql = text("""
            SELECT idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios
            FROM contenidosmensual
            ORDER BY numcomentarios DESC
            LIMIT :lim
        """)
        return self.db.execute(sql, {"lim": limit}).fetchall()

    def get_top_vendidos(self, limit: int):
        """ Top por numVentas DESC """
        sql = text("""
            SELECT idcontenido, numventas, esalbum, sumavaloraciones, numcomentarios
            FROM contenidosmensual
            ORDER BY numventas DESC
            LIMIT :lim
        """)
        return self.db.execute(sql, {"lim": limit}).fetchall()
    
    def get_top_generos_por_ventas(self, limit: int):
        """
        Agrupa por género y suma las ventas totales de cada uno.
        Devuelve: [(genero, total_ventas), ...]
        """
        sql = text("""
            SELECT genero, SUM(numventas) as total_ventas
            FROM contenidosmensual
            WHERE genero IS NOT NULL AND genero != 'Desconocido'
            GROUP BY genero
            ORDER BY total_ventas DESC
            LIMIT :lim
        """)
        result = self.db.execute(sql, {"lim": limit}).fetchall()
        
        # Convertimos a una lista de diccionarios simple
        ranking = []
        for row in result:
            ranking.append({
                "genero": row.genero,
                "totalVentas": int(row.total_ventas or 0)
            })
        return ranking