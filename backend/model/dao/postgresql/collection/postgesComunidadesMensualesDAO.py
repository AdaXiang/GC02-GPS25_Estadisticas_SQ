from sqlalchemy import text
from backend.model.dto.comunidadMensualDTO import ComunidadDTO
from backend.model.dao.interfaceComunidadesMensualesDao import InterfaceComunidadesMensualesDAO

class PostgresComunidadesMensualesDAO(InterfaceComunidadesMensualesDAO):
    def __init__(self, db):
        self.db = db

    def actualizar_o_insertar_comunidad(self, dto: ComunidadDTO) -> bool:
        try:
            sql_check = text("SELECT idcomunidad FROM comunidadesmensual WHERE idcomunidad = :id")
            existe = self.db.execute(sql_check, {"id": dto.idComunidad}).fetchone()

            if existe:
                sql_update = text("""
                    UPDATE comunidadesmensual
                    SET numpublicaciones = :np, nummiembros = :nm
                    WHERE idcomunidad = :id
                """)
                self.db.execute(sql_update, {
                    "id": dto.idComunidad,
                    "np": dto.numPublicaciones,
                    "nm": dto.numMiembros
                })
            else:
                sql_insert = text("""
                    INSERT INTO comunidadesmensual (idcomunidad, numpublicaciones, nummiembros)
                    VALUES (:id, :np, :nm)
                """)
                self.db.execute(sql_insert, {
                    "id": dto.idComunidad,
                    "np": dto.numPublicaciones,
                    "nm": dto.numMiembros
                })
            
            return True

        except Exception as e:
            print(f"❌ Error DB DAO Comunidad: {e}")
            raise e
        
    def obtener_todas(self) -> list[ComunidadDTO]:
        try:
            sql = text("SELECT idcomunidad, numpublicaciones, nummiembros FROM comunidadesmensual")
            result = self.db.execute(sql).fetchall()
            
            # Devolvemos objetos DTO
            return [
                ComunidadDTO(
                    idcomunidad=row.idcomunidad,
                    numpublicaciones=row.numpublicaciones,
                    nummiembros=row.nummiembros
                ) for row in result
            ]
        except Exception as e:
            print(f"❌ Error DB DAO Comunidad (Get All): {e}")
            raise e

    def obtener_ranking_miembros(self, limite=10) -> list[ComunidadDTO]:
        try:
            sql = text("""
                SELECT idcomunidad, numpublicaciones, nummiembros 
                FROM comunidadesmensual 
                ORDER BY nummiembros DESC 
                LIMIT :lim
            """)
            result = self.db.execute(sql, {"lim": limite}).fetchall()
            
            return [
                ComunidadDTO(
                    idcomunidad=row.idcomunidad,
                    numpublicaciones=row.numpublicaciones,
                    nummiembros=row.nummiembros
                ) for row in result
            ]
        except Exception as e:
            print(f"❌ Error DAO Ranking Miembros: {e}")
            raise e

    def obtener_ranking_publicaciones(self, limite=10) -> list[ComunidadDTO]:
        try:
            sql = text("""
                SELECT idcomunidad, numpublicaciones, nummiembros 
                FROM comunidadesmensual 
                ORDER BY numpublicaciones DESC 
                LIMIT :lim
            """)
            result = self.db.execute(sql, {"lim": limite}).fetchall()
            
            return [
                ComunidadDTO(
                    idcomunidad=row.idcomunidad,
                    numpublicaciones=row.numpublicaciones,
                    nummiembros=row.nummiembros
                ) for row in result
            ]
        except Exception as e:
            print(f"❌ Error DAO Ranking Publicaciones: {e}")
            raise e

    def obtener_por_id(self, id_comunidad) -> ComunidadDTO | None:
        try:
            sql = text("SELECT idcomunidad, numpublicaciones, nummiembros FROM comunidadesmensual WHERE idcomunidad = :id")
            row = self.db.execute(sql, {"id": id_comunidad}).fetchone()
            
            if row:
                return ComunidadDTO(
                    idcomunidad=row.idcomunidad,
                    numpublicaciones=row.numpublicaciones,
                    nummiembros=row.nummiembros
                )
            return None
        except Exception as e:
            print(f"❌ Error DAO Obtener por ID Comunidad: {e}")
            raise e

    def eliminar(self, id_comunidad):
        try:
            sql = text("DELETE FROM comunidadesmensual WHERE idcomunidad = :id")
            result = self.db.execute(sql, {"id": id_comunidad})
            return result.rowcount > 0
        except Exception as e:
            print(f"❌ Error DB DAO Comunidad (Delete): {e}")
            raise e