from backend.model.dao.postgresql.collection.postgresArtistasMensualesDAO import PostgresArtistasMensualesDAO

class PostgreSQLDAOFactory:

    def get_artistas_mensuales_dao(self):
        return PostgresArtistasMensualesDAO()

