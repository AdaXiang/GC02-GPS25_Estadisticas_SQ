from fastapi import APIRouter, HTTPException, Request
from backend.model.model import Model
from pydantic import BaseModel

router = APIRouter(prefix="/estadisticas", tags=["Estadísticas"])
model = Model()

USUARIOS_API = "http://localhost:3000"   # API USUARIOS

# ================== ARTISTAS ==================

@router.get("/artistas/oyentes/{id_artista}")
async def get_oyentes_artista(id_artista: int, request: Request):
    model: Model = request.app.state.model
    data = model.get_artista_oyentes(id_artista)
    if not data:
        raise HTTPException(status_code=404, detail="No hay estadísticas para ese artista")
    return data


# Pydantic model to parse incoming JSON body
class ArtistaRequest(BaseModel):
    idArtista: int

@router.put("/artistas/oyentes")
async def sync_oyentes_artista(request: Request, artista: ArtistaRequest):
    # Aquí obtenemos el modelo desde el app state usando 'request'
    model: Model = request.app.state.model
    id_artista = artista.idArtista  # Usamos el id del body
    
    # Llamamos a tu función de sincronización
    data = model.sync_artista_oyentes(id_artista)  
    return data


@router.get("/artistas/ranking/oyentes")
async def ranking_oyentes(request: Request):
    """
    Devuelve el ranking de artistas por oyentes mensuales (de tu BD estadísticas).
    """
    model: Model = request.app.state.model
    ranking = model.get_ranking_artistas_oyentes()
    return ranking