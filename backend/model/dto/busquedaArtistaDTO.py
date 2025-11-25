class BusquedaArtistaDTO:
    def __init__(self, idartista: int, numBusquedas: int = 0):
        self.idArtista = idartista
        self.numBusquedas = numBusquedas
    
    def to_dict(self):
        return {
            "idArtista": self.idArtista,
            "numBusquedas": self.numBusquedas
        }