class ComunidadDTO:
    def __init__(self, idcomunidad, numpublicaciones: int = 0, nummiembros: int = 0):
        # idcomunidad lo dejamos dinámico (sin int estricto) porque a veces llega como string "1"
        self.idComunidad = idcomunidad
        self.numPublicaciones = numpublicaciones
        self.numMiembros = nummiembros

    def to_dict(self):
        return {
            "idComunidad": self.idComunidad,
            "numPublicaciones": self.numPublicaciones,
            "numMiembros": self.numMiembros
        }