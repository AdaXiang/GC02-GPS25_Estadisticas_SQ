from sqlalchemy import text
from backend.model.dto.reproduccionDTO import ReproduccionDTO # Corrige el nombre del archivo si es necesario
from backend.model.dao.interfaceReproduccionesDao import InterfaceReproduccionesDao

class ReproduccionesDAO(InterfaceReproduccionesDao):
    def __init__(self, db):
        self.db = db

    def insertar_reproduccion(self, id_usuario: int, id_contenido: int, segundos: int):
        """
        Registra una nueva reproducción usando NOW() de PostgreSQL.
        """
        try:
            sql_insert = text("""
                INSERT INTO historialreproducciones (id_usuario, id_contenido, segundos_reproducidos, fecha_reproduccion)
                VALUES (:id_usuario, :id_contenido, :segundos, NOW())
            """)
            
            self.db.execute(sql_insert, {
                "id_usuario": id_usuario,
                "id_contenido": id_contenido,
                "segundos": segundos
            })
            
            # Siguiendo tu patrón en BusquedasDAO, hacemos commit aquí
            self.db.commit()
            
        except Exception as e:
            print(f"❌ Error DAO Reproducciones Insert: {e}")
            self.db.rollback()
            raise e

    def obtener_historial_por_usuario(self, id_usuario: int, limit: int = 50) -> list[ReproduccionDTO]:
        """
        Recupera el historial para mostrarlo en las estadísticas personales.
        Aquí es donde usamos el DTO para mapear la respuesta.
        """
        try:
            sql = text("""
                SELECT id, id_usuario, id_contenido, segundos_reproducidos, fecha_reproduccion
                FROM historialreproducciones
                WHERE id_usuario = :id_usuario
                ORDER BY fecha_reproduccion DESC
                LIMIT :limit
            """)
            
            rows = self.db.execute(sql, {"id_usuario": id_usuario, "limit": limit}).fetchall()

            # Mapeo a DTO, igual que en tu BusquedasArtistasDAO
            return [
                ReproduccionDTO(
                    id_reproduccion=r.id,
                    id_usuario=r.id_usuario,
                    id_contenido=r.id_contenido,
                    segundos=r.segundos_reproducidos,
                    fecha=r.fecha_reproduccion
                )
                for r in rows
            ]
        except Exception as e:
            print(f"❌ Error DAO Obtener Historial: {e}")
            raise e
        
    def eliminar_todo_el_historial(self):
        """
        Vacia completamente la tabla de historial de reproducciones.
        Reinicia la secuencia de IDs a 1.
        """
        try:
            # TRUNCATE es instantáneo y perfecto para reseteos mensuales
            sql = text("TRUNCATE TABLE historialreproducciones RESTART IDENTITY")
            self.db.execute(sql)
            
            # Nota: Al igual que en busquedas, el commit lo hacemos en el modelo
            # pero si tu DAO gestiona transacciones, descomenta:
            # self.db.commit()
            return True
        except Exception as e:
            print(f"❌ Error DAO vaciando historial reproducciones: {e}")
            self.db.rollback() # Por si acaso
            raise e

    def get_top_reproducciones_usuario(self, id_usuario: int, limit: int = 10) -> list[ReproduccionDTO]:
        try:
            # Seleccionamos el contenido y CONTAMOS las veces que aparece.
            sql = text("""
                SELECT id_contenido, COUNT(*) as total_veces
                FROM historialreproducciones
                WHERE id_usuario = :uid
                GROUP BY id_contenido
                ORDER BY total_veces DESC
                LIMIT :lim
            """)
            
            rows = self.db.execute(sql, {"uid": id_usuario, "lim": limit}).fetchall()

            # REUTILIZACIÓN DEL DTO:
            # Usamos 'segundos' para guardar el 'total_veces'.
            # Ponemos fecha en None porque es un acumulado, no una fecha concreta.
            return [
                ReproduccionDTO(
                    id_reproduccion=None,        # No hay ID único de fila, es un grupo
                    id_usuario=id_usuario,
                    id_contenido=r.id_contenido,
                    segundos=r.total_veces,      # <--- AQUÍ GUARDAMOS EL CONTEO
                    fecha=None                   # No aplica fecha
                )
                for r in rows
            ]
        except Exception as e:
            print(f"❌ Error DAO Top Reproducciones Usuario: {e}")
            raise e