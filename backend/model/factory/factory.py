from sqlalchemy.orm import Session
from backend.model.dao.postgresql.collection.busquedasArtistasDAO import BusquedasArtistasDAO
from backend.model.dao.postgresql.collection.postgresArtistasMensualesDAO import PostgresArtistasMensualesDAO
from backend.model.dao.postgresql.collection.postgresNumReproContenido import PostgresNumReproContenidoDAO

class DAOFactory:

    def __init__(self, db: Session):
        self.connector = db  # Usamos la sesión de base de datos de PostgreSQL
        self.busquedas_artistas_dao = BusquedasArtistasDAO(self.connector)
        self.artistas_mensuales_dao = PostgresArtistasMensualesDAO(self.connector)
        self.num_repro_contenido_dao = PostgresNumReproContenidoDAO(self.connector)

    def get_artistas_mensuales_dao(self):
        return self.artistas_mensuales_dao

    def get_busquedas_artistas_dao(self):
        return self.busquedas_artistas_dao
    
    def get_num_repro_contenido_dao(self):
        return self.num_repro_contenido_dao

    def close(self):
        """Cierra la conexión a la base de datos."""
        self.connector.close()  
