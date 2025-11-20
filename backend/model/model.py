from fastapi import HTTPException
import requests
from backend.model.dao.postgresql.postgresDAOFactory import PostgreSQLDAOFactory
from backend.controller.config import MS_USUARIOS_BASE_URL, CONTENIDO_API_BASE_URL
from backend.model.dto.numReproContenidoDTO import NumReproContenidoDTO


class Model:
    def __init__(self):
        # Crear fábrica de DAOs de PostgreSQL
        self.factory = PostgreSQLDAOFactory()
        # Instancias de los DAOs que se usan en este microservicio
        self.artistasMensualesDAO = self.factory.get_artistas_mensuales_dao()
        self.busquedasArtistasDAO = self.factory.get_busquedas_artistas_dao()
        self.num_repro_contenido_dao = self.factory.get_num_repro_contenido_dao()      
        self.URL_CONTENIDOS = f"{CONTENIDO_API_BASE_URL}/elementos" 
        self.URL_CANCIONES = f"{CONTENIDO_API_BASE_URL}/canciones"

    def get_artista_oyentes(self, id_artista: int):
        fila = self.artistasMensualesDAO.obtener_por_id(id_artista)
        if not fila:
            return None
        return {
            "idArtista": fila.idArtista,
            "numOyentes": int(fila.numOyentes or 0),
            "valoracionMedia": int(fila.valoracionMedia or 0),
        }

    def get_ranking_artistas_oyentes(self):
            filas = self.artistasMensualesDAO.obtener_ranking_oyentes()
            return [
                {
                    # CAMBIOS AQUÍ: Usa los nombres exactos definidos en tu DTO
                    "idArtista": f.idArtista,         # Antes tenías f.idartista
                    "numOyentes": int(f.numOyentes or 0),     # Antes tenías f.numoyentes
                    "valoracionMedia": int(f.valoracionMedia or 0), # Antes tenías f.valoracionmedia
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

        # Llamamos a 'upsert' pasando los parámetros individuales
        self.artistasMensualesDAO.upsert(
            id_artista=id_artista,
            num_oyentes=oyentes,
            valoracion_media=valoracion
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

    # ================== BUSQUEDAS ARTISTAS ==================
    def registrar_o_actualizar_busqueda_artista(self, id_artista: int, id_usuario: int | None = None):
        print(f"✅ Registrando o actualizando búsqueda para el artista {id_artista} y el usuario {id_usuario}")
        self.busquedasArtistasDAO.insertar_o_actualizar_busqueda(id_artista, id_usuario)


    def get_top_artistas_busquedas(self, limit: int = 10):
        """
        Devuelve el top de artistas más buscados del mes.

        Como machacas las estadísticas cada mes con el scheduler
        (borrando la tabla), esta consulta siempre refleja el
        mes actual.
        """
        filas = self.busquedasArtistasDAO.get_top_artistas_busquedas(limit)
        return [
            {
                "idArtista": f.idArtista,
                "numBusquedas": int(f.numBusquedas or 0)
            }
            for f in filas
        ]
        
    # ================== CONTENIDO ==================    
    def get_todos_los_contenidos(self):
        filas = self.num_repro_contenido_dao.obtener_todos()
        return [
            {
                "idContenido": f.idContenido,
                "numReproducciones": int(f.numReproducciones or 0),
                "esAlbum": f.esAlbum,
                "numValoraciones": int(f.numValoraciones or 0),
                "sumaValoraciones": int(f.sumaValoraciones or 0),
                "numComentarios": int(f.numComentarios or 0)
            }
            for f in filas
        ]

    def sincronizar_desde_api_externa(self, id_contenido: int):
            """
            Recupera datos de la API de Contenidos y, si es canción, 
            busca el numRep en la API de Canciones.
            """
            print(f"🔄 Sincronizando contenido ID: {id_contenido}...")

            # -----------------------------------------------------
            # PASO 1: Obtener información base (Valoración y Tipo)
            # -----------------------------------------------------
            try:
                # Asumimos que existe un endpoint por ID: /api/contenidos/{id}
                # Si no existe y solo tienes el de "todos", avísame, pero lo ideal es por ID.
                resp_general = requests.get(f"{self.URL_CONTENIDOS}/{id_contenido}")
                resp_general.raise_for_status()
                data_general = resp_general.json()
            except Exception as e:
                print(f"❌ Error conectando con API Contenidos: {e}")
                raise e

            # Mapeo según tu JSON de ejemplo:
            # tipo: 1 = Álbum (Electric Dreams)
            # tipo: 2 = Canción (Electric, Wave)
            tipo_contenido = data_general.get("tipo")
            valoracion = data_general.get("valoracion", 0)
            
            # Determinar si es álbum
            es_album = (tipo_contenido == 1) 

            # -----------------------------------------------------
            # PASO 2: Obtener reproducciones (numRep)
            # -----------------------------------------------------
            num_reproducciones = 0

            if tipo_contenido == 2: # Si es CANCIÓN
                try:
                    # Llamamos a la API específica de canciones para sacar el numRep
                    # Endpoint: /api/canciones/{id} (Suponiendo que existe para 1 canción)
                    resp_cancion = requests.get(f"{self.URL_CANCIONES}/{id_contenido}")
                    
                    if resp_cancion.status_code == 200:
                        data_cancion = resp_cancion.json()
                        # En tu segundo JSON, el campo es "numRep"
                        num_reproducciones = data_cancion.get("numRep", 0)
                    else:
                        print(f"⚠️ No se pudo obtener detalles de canción {id_contenido}. Status: {resp_cancion.status_code}")

                except Exception as e:
                    print(f"⚠️ Error conectando con API Canciones (se usará 0 repros): {e}")
            
            # Si es ÁLBUM (tipo 1), normalmente las reproducciones son la suma de sus canciones
            # o 0 si no se trakean a nivel de álbum. Lo dejamos en 0 o lo que venga si la API cambia.
            
            # -----------------------------------------------------
            # PASO 3: Crear DTO y Guardar
            # -----------------------------------------------------
            dto = NumReproContenidoDTO(
                idcontenido=id_contenido,
                numreproducciones=int(num_reproducciones),
                esalbum=bool(es_album),
                sumavaloraciones=float(valoracion), # Guardamos la valoración actual
                numvaloraciones=1, # Placeholder ya que la API externa no devuelve 'cantidad' de votos, solo el promedio
                numcomentarios=0
            )

            self.num_repro_contenido_dao.actualizar_o_insertar(dto)

            return {
                "id": id_contenido,
                "tipo_detectado": "Album" if es_album else "Cancion",
                "reproducciones_guardadas": num_reproducciones,
                "valoracion_guardada": valoracion
            }

    def get_contenido_reproducciones(self, id_contenido: int):
        fila = self.num_repro_contenido_dao.obtener_por_id(id_contenido)
        if not fila:
            return None
        
        # Devolvemos un diccionario simple o el objeto, según prefieras en tu controller
        return {
            "idContenido": fila.idContenido,
            "numReproducciones": fila.numReproducciones
        }

    def update_contenido_reproducciones(self, id_contenido: int, nuevas_reproducciones: int):
        # Intentamos actualizar
        actualizado = self.num_repro_contenido_dao.actualizar_reproducciones(id_contenido, nuevas_reproducciones)
        
        if not actualizado:
            # AQUI PODRIAMOS LLAMAR AL MICROSERVICIO JAVA PARA VERIFICAR SI EXISTE

            return None
            
        return {
            "idContenido": id_contenido,
            "numReproducciones": nuevas_reproducciones,
            "mensaje": "Actualizado correctamente"
        }
    









 