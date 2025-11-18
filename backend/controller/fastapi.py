from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.controller.config import setup_cors
from view.view import router as estadisticas_router
from backend.model.model import Model
from apscheduler.schedulers.background import BackgroundScheduler

model = Model()
scheduler = BackgroundScheduler()

def actualizar_mensualmente():
    print("🔄 Actualizando oyentes mensuales...")
    try:
        model.sync_todos_los_artistas()
        print("✅ Actualización mensual completada")
    except Exception as e:
        print("❌ Error durante la actualización mensual:", str(e))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    if not scheduler.running:
        # Job mensual real
        scheduler.add_job(
            actualizar_mensualmente,
            trigger="cron",
            day=1,
            hour=0,
            minute=0
        )
        print("🗓️ Scheduler mensual añadido")

        # 🔧 TEST: ejecutar cada 30 segundos (descomenta para probar)
        # scheduler.add_job(
        #     actualizar_mensualmente,
        #     trigger="interval",
        #     seconds=30
        # )
        # print("⏱️ Scheduler de prueba (30s) iniciado")

        # scheduler.start()
        # print("🗓️ Scheduler iniciado")

    app.state.model = model

    yield  # Aquí corre la aplicación

    # === SHUTDOWN ===
    scheduler.shutdown()
    print("🛑 Scheduler detenido")


# Creamos la app con lifespan
app = FastAPI(
    title="Microservicio de Estadísticas",
    lifespan=lifespan
)

# CORS
setup_cors(app)

# Rutas
app.include_router(estadisticas_router)


@app.get("/")
def root():
    return {"message": "✅ Microservicio de Estadísticas activo"}
