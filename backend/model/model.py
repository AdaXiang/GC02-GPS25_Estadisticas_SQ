from fastapi import HTTPException
import requests
from backend.model.dao.postgresql.postgresDAOFactory import PostgreSQLDAOFactory
from backend.controller.config import MS_COMUNIDAD_BASE_URL, MS_CONTENIDO_BASE_URL, MS_USUARIOS_BASE_URL


class Model:
    def __init__(self):
        # Crear fábrica de DAOs de PostgreSQL
        self.factory = PostgreSQLDAOFactory()
        # Instancias de los DAOs que se usan en este microservicio
        self.artistasMensualesDAO = self.factory.get_artistas_mensuales_dao()

    def get_artista_oyentes(self, id_artista: int):
        fila = self.artistasMensualesDAO.obtener_por_id(id_artista)
        if not fila:
            return None
        return {
            "idArtista": fila.idartista,
            "numOyentes": int(fila.numoyentes or 0),
            "valoracionMedia": int(fila.valoracionmedia or 0),
        }

    def get_ranking_artistas_oyentes(self):
        filas = self.artistasMensualesDAO.obtener_ranking_oyentes()
        return [
            {
                "idArtista": f.idartista,
                "numOyentes": int(f.numoyentes or 0),
                "valoracionMedia": int(f.valoracionmedia or 0),
            }
            for f in filas
        ]

    # ================== ARTISTAS (PUT: sincronización mensual) ==============

    def sync_artista_oyentes(self, id_artista: int):
        url = f"{MS_USUARIOS_BASE_URL}/api/usuarios/artistas/{id_artista}"

        resp = requests.get(url, timeout=20)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="Artista no encontrado en MS Usuarios")

        resp.raise_for_status()
        data = resp.json()

        # Accedemos directamente a los campos del JSON
        oyentes = data.get("oyentes", 0)
        valoracion = data.get("valoracion", 0)  # 'valoracion' de la API de tu compañero

        # Actualizamos en la base de datos
        # Cambié 'valoracionmedia' a 'valoracion_media' para coincidir con el parámetro esperado
        self.artistasMensualesDAO.upsert(
            id_artista=id_artista,
            num_oyentes=oyentes,
            valoracion_media=valoracion  # Aquí pasamos 'valoracion_media' para que coincida con el DAO
        )

        return {
            "idArtista": id_artista,
            "numOyentes": oyentes,
            "valoracionMedia": valoracion
        }
    
    def obtener_artistas_desde_api(self):
        url = f"{MS_USUARIOS_BASE_URL}/api/usuarios/artistas"  # endpoint de lista de artistas

        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            return resp.json()  # lista completa con todos los artistas
        except Exception as e:
            print("❌ Error obteniendo artistas desde MS Usuarios:", e)
            return []
        
    def sync_todos_los_artistas(self):
        artistas = self.obtener_artistas_desde_api()

        if not artistas:
            print("⚠️ No se pudo obtener la lista de artistas")
            return

        print(f"🔄 Sincronizando {len(artistas)} artistas...")

        resultados = []
        for artista in artistas:
            id_artista = artista["id"]  
            try:
                resultado = self.sync_artista_oyentes(id_artista)
                resultados.append(resultado)
            except Exception as e:
                print(f"❌ Error sincronizando artista {id_artista}:", e)

        print("✅ Sincronización completa")
        return resultados










 