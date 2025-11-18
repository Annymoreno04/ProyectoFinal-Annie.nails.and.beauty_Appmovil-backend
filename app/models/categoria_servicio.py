from pydantic import BaseModel
from typing import Optional

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaCrear(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id_categoria: int

    class Config:
        from_attributes = True
        
class CategoriaActualizar(BaseModel):
    nombre: str
    descripcion: str