from datetime import datetime

class ReproduccionDTO:
    def __init__(self, id_usuario: int, id_contenido: int, segundos: int, fecha: datetime | None = None, id_reproduccion: int | None = None):
        self.id_reproduccion = id_reproduccion
        self.id_usuario = id_usuario
        self.id_contenido = id_contenido
        self.segundos = segundos
        self.fecha = fecha 

    def to_dict(self):
        return {
            "id": self.id_reproduccion,
            "idUsuario": self.id_usuario,
            "idContenido": self.id_contenido,
            "segundosReproducidos": self.segundos,
            "fechaReproduccion": self.fecha.isoformat() if self.fecha else None
        }