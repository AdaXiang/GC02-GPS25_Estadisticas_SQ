import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

class PostgreSQLConnector:
    # --- VARIABLES DE CLASE (Compartidas por todas las instancias) ---
    db_initialized = False
    engine = None
    SessionLocal = None
    Base = declarative_base()

    def __init__(self):
        try:
            # Solo inicializamos si la CLASE no ha sido inicializada aún
            if not PostgreSQLConnector.db_initialized:
                
                # 1. PRIMERO: Intentamos leer la variable de entorno (DOCKER)
                # Si estamos en Docker, esto tendrá valor. Si estamos en local, será None.
                database_url = os.getenv("DATABASE_URL")

                # 2. SEGUNDO: Si NO hay variable de entorno, usamos el JSON (FALLBACK LOCAL)
                if not database_url:
                    print("⚠️ No se detectó DATABASE_URL, buscando credentials.json...")
                    credentials_path = os.path.join(
                        "backend", "model", "dao", "postgresql", "credentials.json"
                    )

                    with open(credentials_path) as f:
                        credentials = json.load(f)

                    user = credentials["user"]
                    password = credentials["password"]
                    port = credentials["port"]
                    dbname = credentials["dbname"]

                    # En local sí usamos localhost
                    database_url = f"postgresql://{user}:{password}@localhost:{port}/{dbname}"

                print(f"🔌 Conectando a BD: {database_url}") # Debug para ver qué está usando

                # Guardamos en las variables de CLASE
                PostgreSQLConnector.engine = create_engine(
                    database_url,
                    echo=True,
                    pool_pre_ping=True
                )

                PostgreSQLConnector.SessionLocal = sessionmaker(
                    autocommit=False,
                    autoflush=False,
                    bind=PostgreSQLConnector.engine
                )

                PostgreSQLConnector.db_initialized = True
                print("✅ Connection to PostgreSQL database initialized successfully.")

        except Exception as e:
            print("❌ Error in connecting to the PostgreSQL database.")
            print(e)
            PostgreSQLConnector.engine = None
            PostgreSQLConnector.SessionLocal = None

    def get_db(self) -> Session:
        """Devuelve una nueva sesión de base de datos."""
        if PostgreSQLConnector.engine is None or PostgreSQLConnector.SessionLocal is None:
            print("Database connection is not initialized.")
            return None

        return PostgreSQLConnector.SessionLocal()