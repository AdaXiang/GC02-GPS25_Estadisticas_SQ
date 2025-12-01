from abc import ABC, abstractmethod
from typing import List, Optional
from backend.model.dto.reproduccionDTO import ReproduccionDTO


class InterfaceReproduccionesDao(ABC):
    """
    Interfaz para la gestión de reproducciones.
    """
    @abstractmethod
    def insertar_reproduccion(self, id_usuario: int, id_contenido: int, segundos: int):
        """Registra una nueva reproducción."""
        pass

    @abstractmethod
    def obtener_historial_por_usuario(self, id_usuario: int, limit: int = 50) -> list[ReproduccionDTO]:
        """Recupera el historial de reproducciones de un usuario."""
        pass
    
    @abstractmethod
    def eliminar_todo_el_historial(self) -> int:
        """Elimina todas las reproducciones, devolviendo el número de registros eliminados."""
        pass
    
    @abstractmethod
    def get_top_reproducciones_usuario(self, id_usuario: int, limit: int = 10) -> list[ReproduccionDTO]:
        """Devuelve los contenidos más reproducidos por un usuario."""
        pass
    
