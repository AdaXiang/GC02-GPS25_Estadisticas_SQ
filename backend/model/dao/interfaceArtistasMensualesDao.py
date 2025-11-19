from abc import ABC, abstractmethod
from typing import List, Optional
from backend.model.dto.artistaMensualDTO import ArtistaMensualDTO


class InterfaceArtistasMensualesDao(ABC):
    """
    Interfaz para la gestión de estadísticas mensuales de artistas.
    """

    @abstractmethod
    def obtener_por_id(self, id_artista: int) -> Optional[ArtistaMensualDTO]:
        """Devuelve un artista mensual por ID."""
        pass

    @abstractmethod
    def obtener_ranking_oyentes(self, limite: int = 10) -> List[ArtistaMensualDTO]:
        """Devuelve el ranking de artistas por número de oyentes."""
        pass

    @abstractmethod
    def upsert(self, dto: ArtistaMensualDTO) -> ArtistaMensualDTO:
        """Inserta o actualiza un artista mensual."""
        pass
