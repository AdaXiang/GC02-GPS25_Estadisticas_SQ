from backend.model.dao.postgresql.posgresConnector import PostgreSQLConnector
from backend.model.dao.postgresql.collection.postgresArtistasMensualesDAO import PostgresArtistasMensualesDAO
from backend.model.dao.postgresql.collection.busquedasArtistasDAO import BusquedasArtistasDAO
from backend.model.dao.postgresql.collection.postgresContenidoDAO import PostgresContenidoDAO

class PostgreSQLDAOFactory:

    def __init__(self):
        """Inicializa el conector a la base de datos PostgreSQL"""
        self.connector = PostgreSQLConnector()  # Usamos el conector para crear una conexión con la base de datos
        self.db = self.connector.get_db()  # SOLO UNA CONEXIÓN, que se reutiliza
        
    def get_artistas_mensuales_dao(self):
        return PostgresArtistasMensualesDAO(self.db)
    
    def get_busquedas_artistas_dao(self):
        return BusquedasArtistasDAO(self.db)
    
    def get_contenido_dao(self):
        return PostgresContenidoDAO(self.db)


