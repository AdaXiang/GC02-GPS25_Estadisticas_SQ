from fastapi import APIRouter, HTTPException, Request
from backend.model.model import Model

router = APIRouter(prefix="/estadisticas", tags=["Estadísticas"])
model = Model()

USUARIOS_API = "http://localhost:3000"   # API USUARIOS

# ========================= ARTISTAS =========================

@router.get("/artistas/oyentes/{id_artista}")
async def get_oyentes_artista(id_artista: int, request: Request):
    """
    Obtiene los oyentes de un artista sin necesidad de usar un modelo Pydantic.
    """
    try:
        data = model.get_artista_oyentes(id_artista)
        if not data:
            raise HTTPException(status_code=404, detail="No hay estadísticas para ese artista")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los oyentes: {str(e)}")


@router.put("/artistas/oyentes")
async def sync_oyentes_artista(request: Request):
    """
    Sincroniza los oyentes de un artista. El ID del artista se pasa en el cuerpo de la solicitud.
    """
    try:
        body = await request.json()  # Obtiene el cuerpo de la solicitud en formato JSON
        id_artista = body.get("idArtista")
        if not id_artista:
            raise HTTPException(status_code=400, detail="Falta el 'idArtista' en la solicitud")

        # Llamamos a la función de sincronización
        data = model.sync_artista_oyentes(id_artista)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al sincronizar oyentes: {str(e)}")


@router.get("/artistas/ranking/oyentes")
async def ranking_oyentes(request: Request):
    """
    Devuelve el ranking de artistas por oyentes mensuales.
    """
    try:
        ranking = model.get_ranking_artistas_oyentes()
        return ranking
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ranking de oyentes: {str(e)}")


@router.post("/artistas/busqueda")
async def registrar_busqueda_artista(request: Request):
    """
    Registra una búsqueda de un artista cada vez que un usuario busque o haga clic en el perfil de un artista.
    """
    try:
        # Obtener el cuerpo de la solicitud en formato JSON
        body = await request.json()
        
        # Extraer los datos necesarios del cuerpo de la solicitud
        id_artista = body.get("idArtista")  # id del artista que se busca
        id_usuario = body.get("idUsuario")  # id del usuario que hace la búsqueda (opcional)

        if not id_artista:
            raise HTTPException(status_code=400, detail="Falta el 'idArtista' en la solicitud")

        # Llamamos al modelo para registrar la búsqueda
        model.registrar_o_actualizar_busqueda_artista(id_artista, id_usuario)

        return {"msg": "Búsqueda registrada"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar la búsqueda: {str(e)}")


@router.get("/artistas/top")
async def get_top_artistas(request: Request, limit: int = 10):
    """
    Devuelve el top de artistas más buscados del mes.
    """
    try:
        # Llamamos al método del modelo para obtener el top de artistas
        top = model.get_top_artistas_busquedas(limit=limit)
        return top
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el top de artistas: {str(e)}")