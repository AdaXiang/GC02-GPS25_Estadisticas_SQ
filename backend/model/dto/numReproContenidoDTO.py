class NumReproContenidoDTO:
    def __init__(self, idcontenido: int, numreproducciones: int = 0, esalbum: bool = False, sumavaloraciones: float = 0, numvaloraciones: int = 0, numcomentarios: int = 0):
        self.idContenido = idcontenido
        self.numReproducciones = numreproducciones
        self.esAlbum = esalbum
        self.sumaValoraciones = sumavaloraciones
        self.numValoraciones = numvaloraciones
        self.numComentarios = numcomentarios