from pydantic import BaseModel
from typing import Optional

class ServicioEnBD(BaseModel):
    id_servicio: int
    id_categoria: int
    titulo: str
    descripcion: Optional[str] = None
    duracion_minutos: Optional[int] = 45


class ServicioCrear(BaseModel):
    id_categoria: int
    titulo: str
    descripcion: Optional[str] = None
    duracion_minutos: Optional[int] = 45


class ServicioActualizar(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    duracion_minutos: Optional[int] = None
