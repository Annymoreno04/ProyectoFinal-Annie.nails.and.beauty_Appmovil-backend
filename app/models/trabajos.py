from pydantic import BaseModel
from typing import Optional

class TrabajoBase(BaseModel):
    titulo: str
    descripcion: str

class TrabajoCrear(TrabajoBase):
    pass

class TrabajoActualizar(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None

# Modelo usado en responses (incluye id)
class Trabajo(TrabajoBase):
    id: int

    class Config:
        orm_mode = True
