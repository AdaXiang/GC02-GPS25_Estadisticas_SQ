class ContenidoDTO:
    def __init__(self, idcontenido: int, numventas: int = 0, esalbum: bool = False, 
                 sumavaloraciones: float = 0, numcomentarios: int = 0, 
                 genero: str = None, esnovedad: bool = False): 
        
        self.idContenido = idcontenido
        self.numVentas = numventas
        self.esAlbum = esalbum
        self.sumaValoraciones = sumavaloraciones
        self.numComentarios = numcomentarios
        self.genero = genero
        self.esNovedad = esnovedad

    def to_dict(self):
        return {
            "idContenido": self.idContenido,
            "numVentas": self.numVentas,
            "esAlbum": self.esAlbum,
            "sumaValoraciones": self.sumaValoraciones,
            "numComentarios": self.numComentarios,
            "genero": self.genero,
            "esNovedad": self.esNovedad
        }