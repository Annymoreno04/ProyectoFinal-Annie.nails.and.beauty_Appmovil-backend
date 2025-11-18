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

class Trabajo(TrabajoBase):
    id: int

    class Config:
        from_attributes = True
