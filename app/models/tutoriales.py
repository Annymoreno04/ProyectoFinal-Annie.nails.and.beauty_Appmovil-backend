from pydantic import BaseModel
from typing import Optional

class TutorialBase(BaseModel):
    id_categoria: int
    titulo: str
    descripcion: Optional[str] = None

class TutorialCrear(TutorialBase):
    pass

class TutorialActualizar(BaseModel):
    id_categoria: Optional[int]
    titulo: Optional[str]
    descripcion: Optional[str]

class TutorialEnBD(TutorialBase):
    id: int

    class Config:
        from_attributes = True
