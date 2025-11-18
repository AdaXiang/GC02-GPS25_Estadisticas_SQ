class ArtistaMensualDTO:
    def __init__(self, idartista: int, numOyentes: int = 0, valoracionmedia: int = 0):
        self.idArtista = idartista
        self.numOyentes = numOyentes
        self.valoracionMedia = valoracionmedia
