from abc import ABC, abstractmethod
from typing import List, Optional
from backend.model.dto.numReproContenidoDTO import NumReproContenidoDTO

class InterfaceNumReproContenidoDao(ABC):
    """
    Interfaz para la gestión de números de reproducciones de contenidos.
    """

    @abstractmethod
    def obtener_todos(self) -> List[NumReproContenidoDTO]:
        """Devuelve todos los registros de números de reproducciones de contenidos."""
        pass

    @abstractmethod
    def actualizar_o_insertar(self, dto: NumReproContenidoDTO) -> bool:
        """Actualiza o inserta un registro de número de reproducciones de contenido."""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id_contenido: int) -> Optional[NumReproContenidoDTO]:
        """Obtiene un registro de número de reproducciones de contenido por su ID."""
        pass
    
    @abstractmethod
    def actualizar_reproducciones(self, id_contenido: int, nuevas_reproducciones: int) -> bool:
        """Actualiza el número de reproducciones de un contenido dado su ID."""
        pass