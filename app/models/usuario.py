
from pydantic import BaseModel, EmailStr
from typing import Optional

class Usuario(BaseModel):
    id_usuario: Optional[int] = None         # ID autoincremental
    id_rol: int                              # Rol obligatorio
    nombre_usuario: str                      # Nombre de usuario único
    nombre: str                              # Nombre completo
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    estado: Optional[str] = "activo"         # Por defecto activo

class UsuarioEnBD(Usuario):
    clave: Optional[str] = None              # Contraseña encriptada

class UsuarioRegistro(BaseModel):
    nombre_usuario: str
    clave: str
    nombre: str
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None

class UsuarioActualizar(BaseModel):
    nombre: Optional[str]
    telefono: Optional[str]
    correo: Optional[str]
    clave: Optional[str]
    id_rol: Optional[int]

class UsuarioAActualizar(BaseModel):
    nombre: Optional[str]
    correo: Optional[str]
    telefono: Optional[str]
