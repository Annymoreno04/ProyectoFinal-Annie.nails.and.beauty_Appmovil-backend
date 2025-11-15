from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class CitaBase(BaseModel):
    id_usuario: int
    id_servicio: int
    id_empleado: Optional[int] = None
    fecha_cita: date
    hora_inicio: time
    estado: Optional[str] = "pendiente"

class CitaCrear(CitaBase):
    pass



class CitaEnBD(CitaBase):
    id_cita: int

    class Config:
        orm_mode = True

class CitaActualizar(BaseModel):
    estado: Optional[str] = None
    fecha: Optional[str] = None
    hora: Optional[str] = None
    # otros campos opcionales...