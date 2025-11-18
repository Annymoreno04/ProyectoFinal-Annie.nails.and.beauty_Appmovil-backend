
from fastapi import APIRouter, HTTPException, Depends, status, Body
from typing import List
from app.models.cita import CitaCrear, CitaActualizar, CitaEnBD
from app.models.usuario import Usuario
from app.data import cita as citas_sql
from .autenticacion import obtener_usuario_actual
import traceback
import json

router = APIRouter(prefix="/citas", tags=["citas"])


@router.get("/", response_model=List[dict])
def obtener_citas():
    try:
        resultado = citas_sql.obtener_citas()
        print(f"✅ Citas obtenidas exitosamente: {len(resultado)} registros")
        return resultado
    except Exception as e:
        print(f"❌ ERROR EN OBTENER_CITAS:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener citas: {str(e)}"
        )

@router.get("/{id_cita}", response_model=dict)
def obtener_cita_por_id(id_cita: int):
    try:
        cita = citas_sql.obtener_cita_por_id(id_cita)
        if not cita:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        return cita
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR EN OBTENER_CITA_POR_ID:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener cita: {str(e)}"
        )

@router.post("/", response_model=dict)
def crear_cita(cita: CitaCrear):
    try:
        nuevo_id = citas_sql.insertar_cita(
            cita.id_usuario,
            cita.id_servicio,
            cita.id_empleado,
            cita.fecha_cita,
            cita.hora_inicio,
            cita.estado,
        )
        return {"mensaje": "Cita registrada correctamente", "id_cita": nuevo_id}
    except Exception as e:
        print(f"❌ ERROR EN CREAR_CITA:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear cita: {str(e)}"
        )

@router.put("/{id_cita}", response_model=dict)
def actualizar_cita(
    id_cita: int, 
    cita: CitaActualizar, 
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    try:
    
        if usuario_actual.id_rol != 1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. Solo administradores."
            )
        
        cita_actual = citas_sql.obtener_cita_por_id(id_cita)
        if not cita_actual:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        
        actualizado = citas_sql.actualizar_cita_por_id(id_cita, cita)
        if not actualizado:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
        
        return {"mensaje": "Cita actualizada correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR EN ACTUALIZAR_CITA:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cita: {str(e)}"
        )

@router.patch("/{cita_id}", response_model=dict)
def actualizar_estado_cita(
    cita_id: int, 
    datos: CitaActualizar = Body(...),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    try:
        print(f"=" * 80)
        print(f"🔍 DEBUG PATCH /citas/{cita_id}")
        print(f"👤 Usuario: {usuario_actual.nombre} (ID: {usuario_actual.id_usuario}, Rol: {usuario_actual.id_rol})")
        
        datos_dict = datos.dict(exclude_none=True)
        print(f"📦 Datos a actualizar: {json.dumps(datos_dict, indent=2, default=str)}")
     
        if not datos_dict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se proporcionaron campos para actualizar"
            )
        
        nuevo_estado = datos_dict.get('estado')
        
        # ROL 1 = ADMIN - Puede cambiar a: confirmada, cancelada
        if usuario_actual.id_rol == 1:
            if nuevo_estado and nuevo_estado not in ['confirmada', 'cancelada', 'pendiente']:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Administradores solo pueden cambiar estados a: pendiente, confirmada. No pueden usar: {nuevo_estado}"
                )
            print(f"✅ Admin puede modificar la cita")
  
        elif usuario_actual.id_rol == 3:
            if nuevo_estado and nuevo_estado not in ['completada', 'no_realizada']:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Empleados solo pueden cambiar estados a: completada, no_realizada. No pueden usar: {nuevo_estado}"
                )

            cita_actual = citas_sql.obtener_cita_por_id(cita_id)
            if not cita_actual:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cita con ID {cita_id} no encontrada"
                )
            
            if cita_actual.get('estado') != 'confirmada':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Solo puedes completar citas que estén en estado 'confirmada'. Estado actual: {cita_actual.get('estado')}"
                )
            
            print(f"✅ Empleado puede completar la cita")
        
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para modificar citas"
            )
        
        if usuario_actual.id_rol != 3:
            cita = citas_sql.obtener_cita_por_id(cita_id)
            if not cita:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Cita con ID {cita_id} no encontrada"
                )
            print(f"📋 Estado actual: {cita.get('estado')}")
        
        print(f"🔄 Aplicando cambios...")
        filas_afectadas = citas_sql.actualizar_cita_por_id(cita_id, datos)
        
        if filas_afectadas == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No hay campos para actualizar o los valores son iguales"
            )

        cita_actualizada = citas_sql.obtener_cita_por_id(cita_id)
        print(f"✅ Cita actualizada - Nuevo estado: {cita_actualizada.get('estado')}")
        print(f"=" * 80)
        
        return {
            "mensaje": "Cita actualizada correctamente",
            "id_cita": cita_id,
            "estado_nuevo": cita_actualizada.get('estado'),
            "campos_actualizados": list(datos_dict.keys())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar cita: {str(e)}"
        )

@router.delete("/{id_cita}", response_model=dict)
def eliminar_cita(
    id_cita: int,
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    try:
        print(f"🗑️ Eliminando cita {id_cita} - Usuario: {usuario_actual.nombre}")
        
        eliminado = citas_sql.eliminar_cita(id_cita)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Cita no encontrada")
        
        print(f"✅ Cita {id_cita} eliminada correctamente")
        return {"mensaje": "Cita eliminada correctamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR EN ELIMINAR_CITA:")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar cita: {str(e)}"
        )