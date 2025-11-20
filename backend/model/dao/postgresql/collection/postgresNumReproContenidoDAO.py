from sqlalchemy import text
from backend.model.dto.numReproContenidoDTO import NumReproContenidoDTO
from backend.model.dao.interfaceNumReproContenidoDao import InterfaceNumReproContenidoDao

class PostgresNumReproContenidoDAO(InterfaceNumReproContenidoDao):
    def __init__(self, db):
        self.db = db
        
    def obtener_todos(self) -> list[NumReproContenidoDTO]:
        # Consulta a tu tabla 'contenidosmensual' (ver imagen 1)
        sql = text("""
            SELECT idcontenido, numreproducciones, esalbum, numvaloraciones, sumavaloraciones, numcomentarios
            FROM contenidosmensual
        """)
        result = self.db.execute(sql)
        contenidos = []
        for row in result:
            contenidos.append(NumReproContenidoDTO(
                idcontenido=row.idcontenido,
                numreproducciones=int(row.numreproducciones or 0),
                esalbum=row.esalbum,
                numvaloraciones=int(row.numvaloraciones or 0),
                sumavaloraciones=int(row.sumavaloraciones or 0),
                numcomentarios=int(row.numcomentarios or 0)
            ))
        return contenidos
    
    def actualizar_o_insertar(self, dto: NumReproContenidoDTO) -> bool:
            try:
                # 1. Buscar si ya existe
                sql_check = text("SELECT idcontenido FROM contenidosmensual WHERE idcontenido = :id")
                existe = self.db.execute(sql_check, {"id": dto.idContenido}).fetchone()

                if existe:
                    # UPDATE: Solo actualizamos lo que cambia (Repros, esAlbum, Valoracion)
                    sql_update = text("""
                        UPDATE contenidosmensual
                        SET numreproducciones = :nr,
                            esalbum = :ea,
                            sumavaloraciones = :sv
                            -- Nota: No tocamos numcomentarios ni numvaloraciones si no tenemos datos nuevos reales
                        WHERE idcontenido = :id
                    """)
                    self.db.execute(sql_update, {
                        "id": dto.idContenido,
                        "nr": dto.numReproducciones,
                        "ea": dto.esAlbum,
                        "sv": dto.sumaValoraciones
                    })
                else:
                    # INSERT: Creamos el registro de cero
                    sql_insert = text("""
                        INSERT INTO contenidosmensual (idcontenido, numreproducciones, esalbum, sumavaloraciones, numvaloraciones, numcomentarios)
                        VALUES (:id, :nr, :ea, :sv, 1, 0)
                    """)
                    self.db.execute(sql_insert, {
                        "id": dto.idContenido,
                        "nr": dto.numReproducciones,
                        "ea": dto.esAlbum,
                        "sv": dto.sumaValoraciones
                    })
                
                self.db.commit()
                return True

            except Exception as e:
                self.db.rollback()
                print(f"❌ Error DB: {e}")
                raise e

    def obtener_por_id(self, id_contenido: int) -> NumReproContenidoDTO | None:
        # Consulta a tu tabla 'contenidosmensual' (ver imagen 1)
        sql = text("""
            SELECT idcontenido, numreproducciones, esalbum
            FROM contenidosmensual
            WHERE idcontenido = :id
        """)
        row = self.db.execute(sql, {"id": id_contenido}).fetchone()

        if not row:
            return None

        return NumReproContenidoDTO(
            idcontenido=row.idcontenido,
            numreproducciones=int(row.numreproducciones or 0),
            esalbum=row.esalbum
        )

    def actualizar_reproducciones(self, id_contenido: int, nuevas_reproducciones: int):
        # Actualizamos el contador en Postgres
        sql = text("""
            UPDATE contenidosmensual
            SET numreproducciones = :num
            WHERE idcontenido = :id
        """)
        result = self.db.execute(sql, {"num": nuevas_reproducciones, "id": id_contenido})
        self.db.commit()
        return result.rowcount > 0