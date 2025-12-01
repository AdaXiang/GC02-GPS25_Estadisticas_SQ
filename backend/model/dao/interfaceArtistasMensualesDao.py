from abc import ABC, abstractmethod
from typing import List, Optional
from backend.model.dto.artistaMensualDTO import ArtistaMensualDTO


class InterfaceArtistasMensualesDao(ABC):
    """
    Interfaz para la gestión de estadísticas mensuales de artistas.
    """
    @abstractmethod
    def actualizar_o_insertar(self, dto: ArtistaMensualDTO) -> bool:
        """Actualiza o inserta un artista mensual."""
        pass

    @abstractmethod
    def obtener_todos(self) -> List[ArtistaMensualDTO]:
        """Devuelve todos los artistas mensuales."""
        pass
    
    @abstractmethod
    def obtener_por_id(self, id_artista: int) -> Optional[ArtistaMensualDTO]:
        """Devuelve un artista mensual por ID."""
        pass

    @abstractmethod
    def obtener_ranking_oyentes(self, limite: int = 10) -> List[ArtistaMensualDTO]:
        """Devuelve el ranking de artistas por número de oyentes."""
        pass

