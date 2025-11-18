
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional
from ..models.usuario import Usuario, UsuarioEnBD, UsuarioActualizar
from ..data.usuarios import actualizar_usuario, obtener_por_nombre_usuario
from .autenticacion import obtener_usuario_actual

router = APIRouter(prefix="/usuario", tags=["usuario"])

router_usuarios = APIRouter(tags=["usuarios"])


@router.get("/perfil", response_model=Usuario)
def obtener_perfil(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """Obtiene el perfil del usuario autenticado"""
    return usuario_actual


@router.get("/info", response_model=Usuario)
def obtener_info(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """Obtiene la información del usuario autenticado"""
    return usuario_actual


@router.get("/detalles", response_model=Usuario)
def obtener_detalles(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """Obtiene los detalles completos del usuario autenticado"""
    return usuario_actual


@router.put("/perfil", response_model=UsuarioEnBD)
def actualizar_perfil(
    datos: UsuarioActualizar,
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Actualiza el perfil completo del usuario"""
    try:
        usuario_actualizado = actualizar_usuario(usuario_actual.id_usuario, datos)
        return usuario_actualizado
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar perfil: {str(e)}"
        )


@router.put("/nombre")
def actualizar_nombre(
    nuevo_nombre: str,
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Actualiza solo el nombre del usuario"""
    if not nuevo_nombre or len(nuevo_nombre.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre no puede estar vacío"
        )
    
    datos = UsuarioActualizar(nombre=nuevo_nombre.strip())
    usuario_actualizado = actualizar_usuario(usuario_actual.id_usuario, datos)
    
    return {
        "mensaje": "Nombre actualizado correctamente",
        "nombre_anterior": usuario_actual.nombre,
        "nombre_nuevo": usuario_actualizado.nombre
    }


@router.put("/telefono")
def actualizar_telefono(
    nuevo_telefono: str,
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Actualiza solo el teléfono del usuario"""
    if not nuevo_telefono or len(nuevo_telefono.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El teléfono no puede estar vacío"
        )
    
    datos = UsuarioActualizar(telefono=nuevo_telefono.strip())
    usuario_actualizado = actualizar_usuario(usuario_actual.id_usuario, datos)
    
    return {
        "mensaje": "Teléfono actualizado correctamente",
        "telefono_anterior": usuario_actual.telefono,
        "telefono_nuevo": usuario_actualizado.telefono
    }


@router.put("/correo")
def actualizar_correo(
    nuevo_correo: str,
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Actualiza solo el correo del usuario"""
    if not nuevo_correo or "@" not in nuevo_correo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Correo inválido"
        )
    
    datos = UsuarioActualizar(correo=nuevo_correo.strip())
    usuario_actualizado = actualizar_usuario(usuario_actual.id_usuario, datos)
    
    return {
        "mensaje": "Correo actualizado correctamente",
        "correo_anterior": usuario_actual.correo,
        "correo_nuevo": usuario_actualizado.correo
    }


@router.get("/estado")
def obtener_estado(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """Obtiene el estado del usuario (activo/inactivo)"""
    return {
        "estado": usuario_actual.estado,
        "id_usuario": usuario_actual.id_usuario,
        "nombre_usuario": usuario_actual.nombre_usuario
    }


@router.get("/activo")
def obtener_activo(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """Verifica si el usuario está activo"""
    return {
        "activo": usuario_actual.estado == "activo",
        "estado": usuario_actual.estado
    }


@router.get("/resumen")
def obtener_resumen(usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    """Obtiene un resumen de la información del usuario"""
    return {
        "id_usuario": usuario_actual.id_usuario,
        "nombre_usuario": usuario_actual.nombre_usuario,
        "nombre": usuario_actual.nombre,
        "correo": usuario_actual.correo,
        "telefono": usuario_actual.telefono,
        "rol": usuario_actual.id_rol,
        "estado": usuario_actual.estado
    }


@router.get("/validar/disponible")
def validar_disponibilidad(
    campo: str,
    valor: str,
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """Valida si un valor está disponible para un campo específico"""
    if campo not in ["nombre_usuario", "correo"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Campo no válido. Campos permitidos: nombre_usuario, correo"
        )
    
    if campo == "nombre_usuario" and valor == usuario_actual.nombre_usuario:
        return {"disponible": True, "mensaje": "Es tu nombre de usuario actual"}
    
    if campo == "correo" and valor == usuario_actual.correo:
        return {"disponible": True, "mensaje": "Es tu correo actual"}

    return {"disponible": True, "campo": campo, "valor": valor}


@router.get("/ayuda")
def obtener_ayuda():
    """Obtiene ayuda sobre los endpoints disponibles"""
    return {
        "endpoints": [
            "GET /usuario/perfil - Obtiene el perfil del usuario",
            "GET /usuario/info - Obtiene información del usuario",
            "GET /usuario/detalles - Obtiene detalles del usuario",
            "PUT /usuario/perfil - Actualiza el perfil completo",
            "PUT /usuario/nombre - Actualiza solo el nombre",
            "PUT /usuario/telefono - Actualiza solo el teléfono",
            "PUT /usuario/correo - Actualiza solo el correo",
            "GET /usuario/estado - Obtiene el estado del usuario",
            "GET /usuario/activo - Verifica si está activo",
            "GET /usuario/resumen - Obtiene un resumen",
            "GET /usuario/validar/disponible - Valida disponibilidad de campo",
            "GET /usuario/ayuda - Obtiene esta ayuda"
        ]
    }


@router_usuarios.post("/usuarios/actualizar")
async def actualizar_perfil_clientes(
    nombre: Optional[str] = None,
    correo: Optional[str] = None,
    telefono: Optional[str] = None,
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Endpoint para actualizar el perfil del usuario (compatible con cliente React Native).
    
    Parámetros en body (JSON):
    - nombre: nuevo nombre (opcional)
    - correo: nuevo correo (opcional)
    - telefono: nuevo teléfono (opcional)
    """
    try:
        datos = UsuarioActualizar(
            nombre=nombre,
            correo=correo,
            telefono=telefono
        )
        
        usuario_actualizado = actualizar_usuario(usuario_actual.id_usuario, datos)
        
        return {
            "success": True,
            "mensaje": "Perfil actualizado correctamente",
            "usuario": usuario_actualizado
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error al actualizar perfil: {str(e)}"
        )

