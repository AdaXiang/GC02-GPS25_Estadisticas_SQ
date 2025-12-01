import requests
from fastapi import HTTPException
from backend.model.dao.postgresql.postgresDAOFactory import PostgreSQLDAOFactory
from backend.controller.config import MS_USUARIOS_BASE_URL, CONTENIDO_API_BASE_URL, COMUNIDAD_API_BASE_URL

# IMPORTS DE LOS DTOs ESTANDARIZADOS
from backend.model.dto.contenidoDTO import ContenidoDTO
from backend.model.dto.artistaMensualDTO import ArtistaMensualDTO
from backend.model.dto.busquedaArtistaDTO import BusquedaArtistaDTO
from backend.model.dto.comunidadMensualDTO import ComunidadDTO
from backend.model.dto.reproduccionDTO import ReproduccionDTO

class Model:
    def __init__(self):
        # Crear fábrica de DAOs de PostgreSQL
        self.factory = PostgreSQLDAOFactory()
        
        # Instancias de los DAOs
        self.artistasMensualesDAO = self.factory.get_artistas_mensuales_dao()
        self.busquedasArtistasDAO = self.factory.get_busquedas_artistas_dao()
        self.contenidoDAO = self.factory.get_contenido_dao()      
        self.comunidadDAO = self.factory.get_comunidad_dao()
        self.reproduccionesDAO = self.factory.get_reproducciones_dao()
        
        # URLs
        self.URL_CONTENIDOS = f"{CONTENIDO_API_BASE_URL}/elementos" 
        self.URL_VALORACIONES = f"{CONTENIDO_API_BASE_URL}/usuarioValoraElem"
        self.URL_COMUNIDAD = f"{COMUNIDAD_API_BASE_URL}/comunidad"
        
        # Sesión DB
        self.db = self.factory.db 

    # ================== ARTISTAS (GET) ==================

    def get_todos_los_artistas(self):
        """Obtiene la lista completa de artistas."""
        self.db.rollback()
        try:
            # DAO devuelve lista de objetos ArtistaMensualDTO
            lista_dtos = self.artistasMensualesDAO.obtener_todos()
            
            # Convertimos a diccionarios para el JSON
            return [dto.to_dict() for dto in lista_dtos]

        except Exception as e:
            print(f"❌ Error DB en get_todos_los_artistas: {e}")
            self.db.rollback()
            raise e

    def get_artista_oyentes(self, id_artista: int):
        self.db.rollback()
        try:
            # DAO devuelve un objeto ArtistaMensualDTO o None
            dto = self.artistasMensualesDAO.obtener_por_id(id_artista)
            
            if not dto:
                return None
            
            return dto.to_dict()
        except Exception as e:
            print(f"❌ Error DB en get_artista_oyentes: {e}")
            self.db.rollback()
            raise e
        
    def get_ranking_artistas_oyentes(self):
        self.db.rollback()
        try:
            lista_dtos = self.artistasMensualesDAO.obtener_ranking_oyentes()
            return [dto.to_dict() for dto in lista_dtos]
        except Exception as e:
            print(f"❌ Error DB en get_ranking_artistas_oyentes: {e}")
            self.db.rollback()
            raise e

    # ================== ARTISTAS (SYNC) ==================

    def sync_artista_oyentes(self, id_artista: int):
        self.db.rollback()
        try:
            url = f"{MS_USUARIOS_BASE_URL}/api/usuarios/artistas/{id_artista}"

            # 1. Petición API Externa
            resp = requests.get(url, timeout=20)
            if resp.status_code == 404:
                raise HTTPException(status_code=404, detail="Artista no encontrado en MS Usuarios")
            resp.raise_for_status()
            data = resp.json()

            # 2. Crear DTO con los datos recibidos
            # A veces el ID viene como 'id' o 'idUsuario' dependiendo de la API
            raw_id = data.get("id") or data.get("idUsuario") or id_artista
            
            dto = ArtistaMensualDTO(
                idartista=raw_id,
                numOyentes=int(data.get("oyentes", 0)),
                valoracionmedia=int(data.get("valoracion", 0))
            )

            # 3. Llamar al DAO pasando el DTO (método actualizado)
            self.artistasMensualesDAO.actualizar_o_insertar(dto)
            self.db.commit()

            return dto.to_dict()
            
        except Exception as e:
            print(f"❌ Error en sync_artista_oyentes: {e}")
            self.db.rollback()
            raise e

    def obtener_artistas_desde_api(self):
        url = f"{MS_USUARIOS_BASE_URL}/api/usuarios/artistas" 
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            return resp.json() 
        except Exception as e:
            print("❌ Error obteniendo artistas desde MS Usuarios:", e)
            return []
        
    def sync_todos_los_artistas(self):
        self.db.rollback()
        artistas = self.obtener_artistas_desde_api()

        if not artistas:
            print("⚠️ No se pudo obtener la lista de artistas")
            return

        print(f"🔄 Sincronizando {len(artistas)} artistas...")
        resultados = []
        for artista in artistas:
            id_artista = artista.get("id")
            try:
                # Reutilizamos el método individual
                resultado = self.sync_artista_oyentes(id_artista)
                resultados.append(resultado)
            except Exception as e:
                print(f"❌ Error sincronizando artista {id_artista}:", e)
                self.db.rollback() 

        print("✅ Sincronización completa")
        return resultados
    
    def delete_artista_estadisticas(self, id_artista: int):
        self.db.rollback()
        try:
            eliminado = self.artistasMensualesDAO.eliminar(id_artista)
            self.db.commit()
            
            if not eliminado:
                return None
            
            return {"idArtista": id_artista, "mensaje": "Eliminado correctamente"}
        except Exception as e:
            print(f"❌ Error DB en delete_artista_estadisticas: {e}")
            self.db.rollback()
            raise e

    # ================== BUSQUEDAS ARTISTAS ==================

    def registrar_o_actualizar_busqueda_artista(self, id_artista: int, id_usuario: int | None = None):
        self.db.rollback()
        print(f"✅ Registrando búsqueda: Artista {id_artista}, Usuario {id_usuario}")
        try:
            # Este DAO sigue usando params sueltos según tu código anterior, 
            # pero el retorno de get_top sí usa DTOs.
            self.busquedasArtistasDAO.insertar_o_actualizar_busqueda(id_artista, id_usuario)
            self.db.commit()
        except Exception as e:
            print(f"❌ Error en registrar busqueda: {e}")
            self.db.rollback()
            raise e

    def get_top_artistas_busquedas(self, limit: int = 10):
        self.db.rollback()
        try:
            # DAO devuelve lista de BusquedaArtistaDTO
            lista_dtos = self.busquedasArtistasDAO.get_top_artistas_busquedas(limit)
            return [dto.to_dict() for dto in lista_dtos]
        except Exception as e:
            self.db.rollback()
            raise e
        
    def delete_busquedas_artista(self, id_artista: int):
        self.db.rollback()
        try:
            filas = self.busquedasArtistasDAO.eliminar_busquedas_por_artista(id_artista)
            self.db.commit()
            return {"idArtista": id_artista, "filasEliminadas": filas}
        except Exception as e:
            self.db.rollback()
            raise e

    def delete_busquedas_usuario(self, id_usuario: int):
        self.db.rollback()
        try:
            filas = self.busquedasArtistasDAO.eliminar_busquedas_por_usuario(id_usuario)
            self.db.commit()
            return {"idUsuario": id_usuario, "filasEliminadas": filas}
        except Exception as e:
            self.db.rollback()
            raise e
        
    def resetear_busquedas_mensuales(self):
        print("🗑️ Reseteando búsquedas mensuales...")
        try:
            # ❌ MAL: Antes tenías esto, que pide un ID que no tienes
            # self.registrar_o_actualizar_busqueda_artista() 

            # ✅ BIEN: Llama al nuevo método del DAO que no pide argumentos
            self.busquedasArtistasDAO.eliminar_todas_las_busquedas()
            
            print("✅ Búsquedas mensuales reseteadas correctamente.")
        except Exception as e:
            print(f"❌ Error reseteo búsquedas: {e}")
            # No hagas raise aquí si es una tarea en segundo plano (cron), 
            # o parará todo el servidor. Solo loguealo.
        
    # ================== CONTENIDO ==================    

    def get_todos_los_contenidos(self):
        self.db.rollback()
        try:
            # DAO devuelve lista de ContenidoDTO
            lista_dtos = self.contenidoDAO.obtener_todos()
            return [dto.to_dict() for dto in lista_dtos]
        except Exception as e:
            self.db.rollback()
            raise e

    def sincronizar_desde_api_externa(self, id_contenido: int):
        self.db.rollback()
        print(f"🔄 Sincronizando contenido ID: {id_contenido}...")

        try:
            # 1. Calls APIs
            resp_elem = requests.get(f"{self.URL_CONTENIDOS}/{id_contenido}", timeout=10)
            resp_elem.raise_for_status()
            data_elem = resp_elem.json()

            num_comentarios = 0
            try:
                resp_com = requests.get(f"{self.URL_VALORACIONES}/{id_contenido}", timeout=10)
                if resp_com.status_code == 200:
                    lista = resp_com.json()
                    reales = [c for c in lista if c.get("comentario") and str(c.get("comentario")).strip() != ""]
                    num_comentarios = len(reales)
            except:
                num_comentarios = 0

            # 2. Extracción segura
            obj_genero = data_elem.get("genero")
            nombre_genero = "Desconocido"
            if isinstance(obj_genero, dict):
                nombre_genero = obj_genero.get("nombre") or "Desconocido"

            # 3. Crear DTO
            dto = ContenidoDTO(
                idcontenido=id_contenido,
                numventas=int(data_elem.get("numventas", 0)),
                esalbum=bool(data_elem.get("esalbum", False)),
                sumavaloraciones=float(data_elem.get("valoracion", 0.0)),
                numcomentarios=int(num_comentarios),
                genero=str(nombre_genero),
                esnovedad=bool(data_elem.get("esnovedad", False))
            )

            # 4. Guardar usando DTO
            self.contenidoDAO.actualizar_o_insertar(dto)
            self.db.commit()
            
            print(f"✅ Contenido {id_contenido} sincronizado")
            return dto.to_dict()

        except Exception as e:
            print(f"❌ Error procesando contenido: {e}")
            self.db.rollback()
            raise e
    
    def obtener_lista_contenidos_api(self):
        try:
            resp = requests.get(self.URL_CONTENIDOS, timeout=20)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print("❌ Error API externa contenidos:", e)
            return []

    def sync_todos_los_contenidos(self):
        self.db.rollback()
        contenidos = self.obtener_lista_contenidos_api()
        if not contenidos: return

        print(f"🔄 Sync masiva: {len(contenidos)} contenidos...")
        resultados = []
        for item in contenidos:
            id_cont = item.get("id")
            if not id_cont: continue
            try:
                res = self.sincronizar_desde_api_externa(id_cont)
                resultados.append(res)
            except Exception as e:
                print(f"❌ Error contenido {id_cont}:", e)
                self.db.rollback()
        return resultados    

    def get_contenido_detalle(self, id_contenido: int):
        self.db.rollback()
        try:
            dto = self.contenidoDAO.obtener_por_id(id_contenido)
            return dto.to_dict() if dto else None
        except Exception as e:
            print(f"❌ Error en get_contenido: {e}")
            self.db.rollback()
            raise e

    def delete_contenido(self, id_contenido: int):
        self.db.rollback()
        try:
            ok = self.contenidoDAO.eliminar(id_contenido)
            self.db.commit()
            if not ok: return None
            return {"idContenido": id_contenido, "mensaje": "Eliminado"}
        except Exception as e:
            self.db.rollback()
            raise e

    # ================== TOPS CONTENIDO ==================

    def get_top_contenidos_valoracion(self, limit: int = 10):
        self.db.rollback()
        try:
            lista = self.contenidoDAO.get_top_valorados(limit)
            return [dto.to_dict() for dto in lista]
        except Exception as e:
            self.db.rollback()
            raise e

    def get_top_contenidos_comentarios(self, limit: int = 10):
        self.db.rollback()
        try:
            lista = self.contenidoDAO.get_top_comentados(limit)
            return [dto.to_dict() for dto in lista]
        except Exception as e:
            self.db.rollback()
            raise e

    def get_top_contenidos_ventas(self, limit: int = 10):
        self.db.rollback()
        try:
            lista = self.contenidoDAO.get_top_vendidos(limit)
            return [dto.to_dict() for dto in lista]
        except Exception as e:
            self.db.rollback()
            raise e
        
    def get_top_generos(self, limit: int = 5):
        self.db.rollback()
        try:
            # Este DAO ya devuelve diccionarios, no DTOs (porque es agrupación)
            return self.contenidoDAO.get_top_generos_por_ventas(limit)
        except Exception as e:
            self.db.rollback()
            raise e
        
    # ================== COMUNIDAD ==================
    def sync_todas_las_comunidades(self):
        """
        Orquestador principal: Obtiene la lista y procesa cada comunidad.
        """
        self.db.rollback() # Limpieza inicial
        
        # 1. Obtener datos crudos de la API
        comunidades_data = self.obtener_comunidades_desde_api()

        if not comunidades_data:
            print("⚠️ No se pudo obtener la lista de comunidades")
            return

        print(f"🔄 Sincronizando {len(comunidades_data)} comunidades...")
        resultados = []

        # 2. Iterar y procesar
        for datos_comunidad in comunidades_data:
            # Protegemos la lectura del ID por si viene como 'id' o 'idComunidad'
            id_comunidad = datos_comunidad.get("idComunidad") or datos_comunidad.get("id")
            
            try:
                # Llamamos al método que procesa una sola comunidad
                # Pasamos 'datos_comunidad' directamente para evitar otra petición API
                resultado = self.sync_comunidad_metricas(id_comunidad, datos_comunidad)
                resultados.append(resultado)
                
            except Exception as e:
                print(f"❌ Error sincronizando comunidad {id_comunidad}:", e)
                self.db.rollback() # Rollback solo de esta iteración fallida

        print("✅ Sincronización de comunidades completa")
        return resultados

    def sync_comunidad_metricas(self, id_comunidad, datos=None):
        """
        Procesa una única comunidad: Crea el DTO y lo guarda en BD.
        Si 'datos' es None, podría intentar buscarla individualmente (opcional).
        """
        self.db.rollback()
        try:
            # Si no pasamos datos (flujo individual), habría que pedirlos.
            # Aquí asumimos que el flujo batch ya nos da los datos.
            if not datos:
                 # Lógica opcional si quisieras buscar por ID individualmente
                 raise Exception("Datos no proporcionados para sincronización individual")

            # 1. Crear DTO con los datos recibidos
            # Mapeamos los campos del JSON externo a tu DTO
            dto = ComunidadDTO(
                idcomunidad=id_comunidad,
                numpublicaciones=int(datos.get("numPublicaciones", 0)),
                # Ojo: Tu API parece devolver 'numUsuarios', pero tu DTO usa 'numMiembros'
                nummiembros=int(datos.get("numUsuarios", 0)) 
            )

            # 2. Llamar al DAO (Upsert)
            self.comunidadDAO.actualizar_o_insertar_comunidad(dto)
            self.db.commit()

            return dto.to_dict()
            
        except Exception as e:
            print(f"❌ Error en sync_comunidad_metricas para ID {id_comunidad}: {e}")
            self.db.rollback()
            raise e

    def obtener_comunidades_desde_api(self):
        """
        Consulta el microservicio externo para obtener todas las comunidades.
        """
        # Usamos la URL base que tenías definida en tu otro método
        url = f"{self.URL_COMUNIDAD}/" 
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            return resp.json() 
        except Exception as e:
            print("❌ Error obteniendo comunidades desde API Externa:", e)
            return []
        
    def sincronizar_comunidad_desde_api(self, id_comunidad):
        try: self.db.rollback() 
        except: pass
        print(f"🔄 Sincronizando comunidad ID: {id_comunidad}...")
        try:
            url = f"{self.URL_COMUNIDAD}/"
            resp = requests.get(url, timeout=10)
            if resp.status_code >= 400:
                print(f"⚠️ Error servidor externo: {resp.text}")
            resp.raise_for_status()
            
            lista = resp.json()
            datos = None
            target = str(id_comunidad)
            
            if isinstance(lista, list):
                for item in lista:
                    if str(item.get("idComunidad")) == target:
                        datos = item
                        break
            
            if not datos:
                print(f"⚠️ Comunidad {id_comunidad} no encontrada.")
                return None

            # Crear DTO
            dto = ComunidadDTO(
                idcomunidad=datos.get("idComunidad"),
                numpublicaciones=int(datos.get("numPublicaciones", 0)),
                nummiembros=int(datos.get("numUsuarios", 0))
            )

            # Guardar DTO
            self.comunidadDAO.actualizar_o_insertar_comunidad(dto)
            self.db.commit()
            
            print(f"✅ Comunidad {id_comunidad} sincronizada.")
            return dto.to_dict()

        except Exception as e:
            print(f"❌ Error comunidad: {e}")
            try: self.db.rollback()
            except: pass
            raise e
        
    def obtener_todas_las_comunidades(self):
        try:
            try: self.db.rollback()
            except: pass
            
            # DAO devuelve DTOs
            lista = self.comunidadDAO.obtener_todas()
            return [dto.to_dict() for dto in lista]
        except Exception as e:
            raise e

    def eliminar_comunidad(self, id_comunidad):
        try:
            self.db.rollback()
            ok = self.comunidadDAO.eliminar(id_comunidad)
            self.db.commit()
            return ok
        except Exception as e:
            self.db.rollback()
            raise e
        
    def obtener_ranking_comunidades_miembros(self):
        try:
            try: self.db.rollback() 
            except: pass
            
            lista = self.comunidadDAO.obtener_ranking_miembros(limite=10)
            return [dto.to_dict() for dto in lista]
        except Exception as e:
            raise e

    def obtener_ranking_comunidades_publicaciones(self):
        try:
            try: self.db.rollback() 
            except: pass
            
            lista = self.comunidadDAO.obtener_ranking_publicaciones(limite=10)
            return [dto.to_dict() for dto in lista]
        except Exception as e:
            raise e
        
    def obtener_comunidad_por_id(self, id_comunidad):
        try:
            try: self.db.rollback() 
            except: pass
            
            dto = self.comunidadDAO.obtener_por_id(id_comunidad)
            return dto.to_dict() if dto else None
        except Exception as e:
            raise e
        
    # ================== REPRODUCCIONES ==================
    def registrar_reproduccion(self, id_usuario: int, id_contenido: int, segundos: int):
        # El DAO ya gestiona el commit/rollback, así que aquí solo llamamos
        print(f"🎵 Registrando reproducción: Usuario {id_usuario}, Contenido {id_contenido}")
        try:
            self.reproduccionesDAO.insertar_reproduccion(id_usuario, id_contenido, segundos)
        except Exception as e:
            raise e

    def obtener_historial_personal(self, id_usuario: int) -> list[dict]:
        """ Devuelve la lista de diccionarios lista para enviar al frontend """
        try:
            dtos = self.reproduccionesDAO.obtener_historial_por_usuario(id_usuario)
            return [dto.to_dict() for dto in dtos]
        except Exception as e:
            print(f"❌ Error obteniendo historial en modelo: {e}")
            return []

    def resetear_reproducciones_mensuales(self):
        """
        Se ejecuta mensualmente (después de procesar las estadísticas).
        Borra todo el historial de escucha para empezar el mes limpio.
        """
        self.db.rollback()
        print("🗑️ Iniciando reseteo mensual de historial de reproducciones...")
        
        try:
            # Llamamos al DAO
            self.reproduccionesDAO.eliminar_todo_el_historial()
            
            self.db.commit()
            print("✅ Historial de reproducciones eliminado. Tabla vacía.")
            return True
            
        except Exception as e:
            print(f"❌ Error CRITICO reseteando reproducciones: {e}")
            self.db.rollback()
            return False
    
    def obtener_top_canciones_usuario(self, id_usuario: int, limit: int = 5):
        """
        Devuelve las canciones más escuchadas reutilizando ReproduccionDTO.
        NOTA: En el JSON devuelto, 'segundosReproducidos' indicará el NÚMERO DE VECES escuchado.
        """
        self.db.rollback()
        try:
            # 1. Obtenemos la lista de DTOs reutilizados
            top_dtos = self.reproduccionesDAO.get_top_reproducciones_usuario(id_usuario, limit)
            
            # 2. Convertimos a diccionario usando el método existente del DTO
            return [dto.to_dict() for dto in top_dtos]
            
        except Exception as e:
            print(f"❌ Error en modelo top canciones usuario: {e}")
            self.db.rollback()
            raise e    
    