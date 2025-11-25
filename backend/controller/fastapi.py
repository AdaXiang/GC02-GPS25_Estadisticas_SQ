from fastapi import FastAPI, HTTPException, Request, APIRouter
from fastapi.responses import JSONResponse
from apscheduler.schedulers.background import BackgroundScheduler
from backend.controller.config import setup_cors  # Configuración de CORS
from backend.model.model import Model  # Importar el modelo
from backend.model.dao.postgresql.posgresConnector import PostgreSQLConnector  # Conexión a la DB
from contextlib import asynccontextmanager
from backend.controller.endpoints import router as estadisticas_router
from backend.controller.endpoints import model  # Importar el modelo desde endpoints
from fastapi.middleware.cors import CORSMiddleware

# Inicializar la aplicación FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Pon "*" para permitir TODOS los orígenes (lo más fácil para desarrollo)
    # O pon ["http://localhost:3001"] para ser específico
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], # Permitir GET, POST, PUT, DELETE, etc.
    allow_headers=["*"], # Permitir todas las cabeceras
)

# Inicializar el Scheduler (para tareas programadas)
scheduler = BackgroundScheduler()

# Función para actualizar mensualmente los oyentes de los artistas
def actualizar_mensualmente():
    print("🔄 Actualizando oyentes mensuales...")
    try:
        model.sync_todos_los_artistas()
        print("✅ Actualización mensual completada")
    except Exception as e:
        print("❌ Error durante la actualización mensual:", str(e))

# Función para resetear las búsquedas mensuales
def resetear_busquedas_mensuales():
    print("🗑️ Reseteando búsquedas mensuales...")
    try:
        model.registrar_o_actualizar_busqueda_artista()  # Llamar al modelo para resetear las búsquedas
        print("✅ Búsquedas reseteadas")
    except Exception as e: 
        print("❌ Error al resetear búsquedas:", str(e))

def actualizar_contenido_mensualmente():
    print("🔄 Iniciando actualización mensual de CONTENIDOS...")
    try:
        # Llamamos al nuevo método masivo del modelo
        model.sync_todos_los_contenidos()
        print("✅ Actualización mensual de contenidos completada")
    except Exception as e:
        print("❌ Error durante la actualización mensual de contenidos:", str(e))

# Configuración de lifespan (cuando el servidor se inicia y apaga)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    if not scheduler.running:
        # Añadimos los jobs de forma compacta
        scheduler.add_job(actualizar_mensualmente, trigger="cron", day=1, hour=0, minute=0)
        print("🗓️ Scheduler mensual añadido")
        
        scheduler.add_job(resetear_busquedas_mensuales, trigger="cron", day=1, hour=0, minute=1)
        print("🗓️ Scheduler mensual añadido (reset búsquedas)")

        scheduler.add_job(actualizar_contenido_mensualmente, trigger="cron", day=1, hour=0, minute=5)
        print("🗓️ Scheduler mensual añadido (Contenidos)")
        # scheduler.add_job(
        #     actualizar_mensualmente, 
        #     trigger="interval", 
        #     seconds=30,
        #     id="test_sync_contenidos", # ID opcional pero útil
        #     replace_existing=True
        # )
        # Iniciar el scheduler
        scheduler.start()
        print("🗓️ Scheduler iniciado")

    app.state.model = model  # Guardamos el modelo en el estado de la app

    yield  # Aquí corre la aplicación

    # === SHUTDOWN ===
    if scheduler.running:
        scheduler.shutdown()
        print("🛑 Scheduler detenido")

# Creamos la app con lifespan
app = FastAPI(
    title="Microservicio de Estadísticas",
    lifespan=lifespan
)

# CORS: Para permitir acceso desde ciertos orígenes (si lo necesitas)
setup_cors(app)

app.include_router(estadisticas_router)

@app.get("/")
def root():
    return {"message": "Microservicio de Estadísticas activo"}
