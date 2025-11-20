from fastapi import APIRouter, HTTPException, Request
from backend.model.model import Model

router = APIRouter(prefix="/estadisticas", tags=["Estadísticas"])
model = Model()

USUARIOS_API = "http://localhost:3000"   # API USUARIOS

# ========================= ARTISTAS =========================

@router.get("/artistas/oyentes/{id_artista}")
async def get_oyentes_artista(id_artista: int, request: Request):
    """
    Obtiene los oyentes de un artista.
    Maneja errores comunes:
    - 400: ID inválido
    - 404: Artista no encontrado
    - 422: Parámetros no válidos
    - 500: Error interno de servidor
    """
    try:
        # 400 - Validación manual del parámetro (ID <= 0 no tiene sentido)
        if id_artista <= 0:
            raise HTTPException(
                status_code=400,
                detail="El ID del artista debe ser un número entero positivo."
            )

        # Llamada al modelo
        data = model.get_artista_oyentes(id_artista)

        # 404 - No existe ese artista
        if not data:
            raise HTTPException(
                status_code=404,
                detail="No hay estadísticas para ese artista."
            )

        return data

    # 422 - (FastAPI los lanza solo, pero puedes capturarlos si quieres)
    except ValueError:
        raise HTTPException(
            status_code=422,
            detail="El parámetro proporcionado no es válido."
        )

    # Error de base de datos (SQLAlchemy)
    except Exception as e:
        # Log del error para depuración
        print(f"❌ Error en get_oyentes_artista: {e}")

        raise HTTPException(
            status_code=500,
            detail=f"Error interno al obtener los oyentes: {str(e)}"
        )


@router.put("/artistas/oyentes")
async def sync_oyentes_artista(request: Request):
    """
    Sincroniza los oyentes de un artista.
    Manejo de errores:
    - 400: Falta idArtista o valor inválido
    - 404: Artista no encontrado
    - 422: Datos mal formados
    - 500: Error interno
    """
    try:
        # Obtener JSON del body
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(
                status_code=422,
                detail="El cuerpo de la solicitud no es un JSON válido."
            )

        id_artista = body.get("idArtista")

        # Validación del parámetro
        if id_artista is None:
            raise HTTPException(
                status_code=400,
                detail="Falta el campo obligatorio 'idArtista'."
            )

        if not isinstance(id_artista, int) or id_artista <= 0:
            raise HTTPException(
                status_code=400,
                detail="'idArtista' debe ser un entero positivo."
            )

        # Llamada al modelo
        data = model.sync_artista_oyentes(id_artista)

        # Si devuelve None → artista no existe
        if data is None:
            raise HTTPException(
                status_code=404,
                detail="No se pudo sincronizar: el artista no existe."
            )

        return data

    except HTTPException:
        raise

    except Exception as e:
        print(f"❌ Error interno en sync_oyentes_artista: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al sincronizar oyentes: {str(e)}"
        )



@router.get("/artistas/ranking/oyentes")
async def ranking_oyentes(request: Request):
    """
    Devuelve el ranking de artistas por oyentes mensuales.
    Manejo de errores:
    - 404: No hay datos de ranking
    - 500: Error interno del servidor
    """
    try:
        ranking = model.get_ranking_artistas_oyentes()

        if ranking is None or len(ranking) == 0:
            raise HTTPException(
                status_code=404,
                detail="No hay datos de ranking disponibles."
            )

        return ranking

    except HTTPException:
        raise

    except Exception as e:
        print(f"❌ Error interno en ranking_oyentes: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al obtener ranking: {str(e)}"
        )



@router.put("/artistas/busqueda")
async def registrar_busqueda_artista(request: Request):
    """
    Registra una búsqueda de un artista cada vez que un usuario busque o haga clic en el perfil de un artista.
    Manejo de errores:
    - 400: Falta idArtista o es inválido
    - 422: Cuerpo no es JSON válido
    - 500: Error interno
    """
    try:
        # Intentamos leer el JSON del body
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(
                status_code=422,
                detail="El cuerpo de la solicitud no es un JSON válido."
            )

        id_artista = body.get("idArtista")
        id_usuario = body.get("idUsuario")  # opcional

        # Validación de idArtista (obligatorio)
        if id_artista is None:
            raise HTTPException(
                status_code=400,
                detail="Falta el campo obligatorio 'idArtista'."
            )

        if not isinstance(id_artista, int) or id_artista <= 0:
            raise HTTPException(
                status_code=400,
                detail="'idArtista' debe ser un entero positivo."
            )

        # Validación opcional de idUsuario (si viene)
        if id_usuario is not None:
            if not isinstance(id_usuario, int) or id_usuario <= 0:
                raise HTTPException(
                    status_code=400,
                    detail="'idUsuario', si se proporciona, debe ser un entero positivo."
                )

        # Registrar/actualizar la búsqueda
        model.registrar_o_actualizar_busqueda_artista(id_artista, id_usuario)

        return {"msg": "Búsqueda registrada correctamente."}

    except HTTPException:
        # Re-lanzamos las que ya están controladas
        raise

    except Exception as e:
        print(f"❌ Error interno en registrar_busqueda_artista: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al registrar la búsqueda."
        )

@router.get("/artistas/top")
async def get_top_artistas(request: Request, limit: int = 10):
    """
    Devuelve el top de artistas más buscados del mes.
    Manejo de errores:
    - 400: 'limit' inválido
    - 404: No hay datos
    - 500: Error interno
    """
    try:
        # Validación de 'limit'
        if limit <= 0:
            raise HTTPException(
                status_code=400,
                detail="'limit' debe ser un entero positivo."
            )

        # (Opcional) límite máximo razonable para no reventar la API
        if limit > 100:
            raise HTTPException(
                status_code=400,
                detail="'limit' no puede ser mayor que 100."
            )

        top = model.get_top_artistas_busquedas(limit=limit)

        if not top or len(top) == 0:
            raise HTTPException(
                status_code=404,
                detail="No hay datos de artistas más buscados para este periodo."
            )

        return top

    except HTTPException:
        raise

    except Exception as e:
        print(f"❌ Error interno en get_top_artistas: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al obtener el top de artistas."
        )

@router.get("/contenido")
async def get_todos_los_contenidos(request: Request):
    """
    Obtiene todos los contenidos con sus estadísticas.

    Posibles errores:
    - 404: No se encontraron contenidos
    - 500: Error interno del servidor o de la base de datos
    """
    try:
        # Llamada al modelo
        contenidos = model.get_todos_los_contenidos()

        # Si el modelo devuelve None o una lista vacía
        if contenidos is None:
            print("⚠️ El modelo devolvió None en get_todos_los_contenidos()")
            raise HTTPException(
                status_code=500,
                detail="El servicio no devolvió datos válidos."
            )

        if isinstance(contenidos, list) and len(contenidos) == 0:
            print("ℹ️ No hay contenidos registrados en la base de datos.")
            raise HTTPException(
                status_code=404,
                detail="No se encontraron contenidos."
            )

        # Todo OK
        return {
            "status": "success",
            "count": len(contenidos) if isinstance(contenidos, list) else None,
            "data": contenidos
        }

    except HTTPException as http_error:
        # Errores lanzados manualmente
        print(f"⚠️ Error controlado: {http_error.detail}")
        raise http_error

    except ConnectionError as ce:
        # Error típico de DB o API externa
        print(f"❌ Error de conexión con la base de datos: {ce}")
        raise HTTPException(
            status_code=500,
            detail="Error de conexión con la base de datos."
        )

    except Exception as e:
        # Error inesperado
        print(f"❌ Error interno no controlado en get_todos_los_contenidos: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error interno al obtener los contenidos."
        )

@router.put("/contenido")
async def sincronizar_contenido(request: Request):
    """
    Sincroniza un contenido específico trayendo datos frescos de las APIs externas.
    Body: { "idContenido": 123 }
    """
    try:
        body = await request.json()
        id_contenido = body.get("idContenido")

        if not id_contenido or not isinstance(id_contenido, int):
            raise HTTPException(status_code=400, detail="JSON inválido: Falta 'idContenido' (int).")

        # Llamada al modelo
        resultado = model.sincronizar_desde_api_externa(id_contenido)

        return {
            "status": "success",
            "message": "Sincronización completada",
            "data": resultado
        }
    
    except Exception as e:
        print(f"❌ Error interno: {e}")
        raise HTTPException(status_code=500, detail="Error interno del servidor.")