from abc import ABC, abstractmethod
from typing import List, Optional
from backend.model.dto.busquedaArtistaDTO import BusquedaArtistaDTO


class InterfaceBusquedasArtistasDao(ABC):
    """
    Interfaz para la gestión de búsquedas de artistas.
    """

    @abstractmethod
    def insertar_o_actualizar_busqueda(self, id_artista: int, id_usuario: int | None = None):
        """Inserta una búsqueda para un artista o actualiza si ya existe."""
        pass

    @abstractmethod
    def get_top_artistas_busquedas(self, limit: int = 10) -> List[BusquedaArtistaDTO]:
        """Devuelve el ranking de artistas más buscados del mes."""
        pass

