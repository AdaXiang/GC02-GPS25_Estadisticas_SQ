from abc import ABC, abstractmethod
from typing import List, Optional
from backend.model.dto.comunidadMensualDTO import ComunidadDTO


class InterfaceComunidadesMensualesDAO(ABC):
    """
    Interfaz para la gestión de comunidades mensuales.
    """
    @abstractmethod
    def actualizar_o_insertar_comunidad(self, dto) -> bool:
        """Inserta o actualiza una comunidad mensual."""
        pass 

    @abstractmethod
    def obtener_todas(self) -> List[dict]:
        """Devuelve una lista de diccionarios con todas las comunidades."""
        pass
    
    @abstractmethod
    def obtener_ranking_miembros(self, top_n: Optional[int] = 10) -> List[dict]:
        """Devuelve el top N de comunidades con más miembros."""
        pass
    
    @abstractmethod
    def obtener_ranking_publicaciones(self, top_n: Optional[int] = 10) -> List[dict]:
        """Devuelve el top N de comunidades con más publicaciones."""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id_comunidad: int) -> Optional[dict]:
        """Busca una comunidad por su ID."""
        pass
    
    @abstractmethod
    def eliminar(self, id_comunidad: int) -> bool:
        """Elimina una comunidad por ID. Devuelve True si borró algo."""
        pass
    