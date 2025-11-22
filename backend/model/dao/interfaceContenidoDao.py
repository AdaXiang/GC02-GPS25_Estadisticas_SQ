from abc import ABC, abstractmethod
from typing import List, Optional
from backend.model.dto.contenidoDTO import ContenidoDTO

class InterfaceContenidoDao(ABC):
    """
    Interfaz para la gestión de números de reproducciones de contenidos.
    """

    @abstractmethod
    def obtener_todos(self) -> List[ContenidoDTO]:
        """Devuelve todos los registros de números de reproducciones de contenidos."""
        pass

    @abstractmethod
    def actualizar_o_insertar(self, dto: ContenidoDTO) -> bool:
        """Actualiza o inserta un registro de número de reproducciones de contenido."""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id_contenido: int) -> Optional[ContenidoDTO]:
        """Devuelve un registro de número de reproducciones de contenido por ID."""
        pass
    
    @abstractmethod
    def eliminar(self, id_contenido: int) -> bool:
        """Elimina un registro de número de reproducciones de contenido por ID."""
        pass
    
    @abstractmethod
    def get_top_valorados(self, limit: int = 10) -> List[ContenidoDTO]:
        """Devuelve los contenidos con mayor valoración media."""
        pass
    
    @abstractmethod
    def get_top_comentados(self, limit: int = 10) -> List[ContenidoDTO]:
        """Devuelve los contenidos con más comentarios."""
        pass
    
    @abstractmethod
    def get_top_vendidos(self, limit: int = 10) -> List[ContenidoDTO]:
        """Devuelve los contenidos con más ventas."""
        pass

    @abstractmethod
    def get_top_generos_por_ventas(self, limit: int = 10) -> List[tuple]:
        """Devuelve los géneros con más ventas totales."""
        pass
    