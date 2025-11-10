from fastapi import FastAPI, HTTPException
from backend.controller.config import setup_cors
from view.view import router as estadisticas_router
from backend.model.model import Model

# Inicializamos la app FastAPI
app = FastAPI(title="Microservicio de Estadísticas")

# Activamos CORS
setup_cors(app)

# Registramos las rutas de view
app.include_router(estadisticas_router)

# Inicializamos el modelo (por ejemplo, conexión a la BD)
model = Model()

# Ruta básica de estado (para pruebas)
@app.get("/")
def root():
    return {"message": "✅ Microservicio de Estadísticas activo"}


