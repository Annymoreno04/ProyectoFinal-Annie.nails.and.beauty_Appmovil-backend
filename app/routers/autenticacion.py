# app/rutas/autenticacion.py
from fastapi import APIRouter, HTTPException, status, Form, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Optional
from ..models.autenticacion import Token
from ..models.usuario import Usuario, UsuarioEnBD, UsuarioRegistro
from ..core.seguridad import verificar_contrasena, crear_token_acceso,  encriptar_contrasena
from ..core.configuracion import CLAVE_SECRETA, ALGORITMO
from ..models.usuario import UsuarioActualizar
from ..data.usuarios import actualizar_usuario
import mysql.connector
import asyncio

from ..data.usuarios import obtener_por_nombre_usuario, insertar_usuario

# from ..data.usuarios import obtener_por_nombre_usuario, insertar_usuario 


router = APIRouter(prefix="/autenticacion")

# Solo header Authorization: Bearer <token>
oauth2 = OAuth2PasswordBearer(tokenUrl="/autenticacion/iniciar-sesion")

@router.post("/iniciar-sesion", response_model=Token)
def iniciar_sesion(
    username: str = Form(...),
    password: str = Form(...),
):
    
    #clave = encriptar_contrasena("Abc123")
    #return {"access_token": clave, "token_type": "bearer"}

    usuario = obtener_por_nombre_usuario(username)
    # Validacion de usuario + clave (en BD esperamos hash bcrypt en columna 'clave')
    if not usuario or not usuario.clave or not verificar_contrasena(password, usuario.clave):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")

    # sub = identificacion, uid = id
    access_token = crear_token_acceso(nombre_usuario=usuario.nombre_usuario, id_usuario=usuario.id_usuario)
    
  
    token = Token(
    access_token=access_token,
    token_type="bearer",
    id_rol=usuario.id_rol
)

    return token

@router.post("/registrar", response_model=Usuario)
async def registrar_usuario(p: UsuarioRegistro):
    await asyncio.sleep(1)
    try:
        # 1️⃣ Verificar si el usuario ya existe
        existente = obtener_por_nombre_usuario(p.nombre_usuario)
        if existente:
            raise HTTPException(status_code=400, detail="El nombre de usuario ya existe.")

        # 2️⃣ Encriptar contraseña
        clave_hash = encriptar_contrasena(p.clave)

        # 3️⃣ Crear objeto de tipo UsuarioEnBD para insertar
        nuevo_usuario = UsuarioEnBD(
            nombre_usuario=p.nombre_usuario,
            clave=clave_hash,
            nombre=p.nombre,
            telefono=p.telefono,
            correo=p.correo,
            id_rol=2,
            estado="activo"
        )

        # 4️⃣ Insertar usuario usando la función del módulo data
        nuevo_id = insertar_usuario(nuevo_usuario)

        # 5️⃣ Devolver objeto Usuario (coincide con response_model)
        return Usuario(
            id_usuario=nuevo_id,
            id_rol=2,
            nombre_usuario=p.nombre_usuario,
            nombre=p.nombre,
            telefono=p.telefono,
            correo=p.correo,
            estado="activo"
        )

    except mysql.connector.Error as e:
        raise HTTPException(status_code=400, detail=f"Error al registrar usuario: {str(e)}")




def obtener_usuario_actual(token: str = Depends(oauth2)) -> Usuario:
    error_credenciales = HTTPException(
        status_code=401,
        detail="Token invalido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        datos = jwt.decode(token, CLAVE_SECRETA, algorithms=[ALGORITMO])
        nombre_usuario = datos.get("sub")  # usamos identificacion como 'sub'
        uid = datos.get("uid")
        if not nombre_usuario or not uid:
            raise error_credenciales
    except JWTError:
        raise error_credenciales

    usuario_bd: Optional[UsuarioEnBD] = obtener_por_nombre_usuario(nombre_usuario)
    
    if not usuario_bd:
        raise error_credenciales

    # No exponemos 'clave' en la respuesta
    return Usuario(
        id_usuario=usuario_bd.id_usuario,
        id_rol=usuario_bd.id_rol,
        nombre_usuario=usuario_bd.nombre_usuario,
        nombre=usuario_bd.nombre,
        telefono=usuario_bd.telefono,
        correo=usuario_bd.correo,
        estado=usuario_bd.estado,
    )

@router.put("/perfil", response_model=UsuarioEnBD)
async def actualizar_perfil(
    datos: UsuarioActualizar, 
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    return actualizar_usuario(usuario_actual.id_usuario, datos)
