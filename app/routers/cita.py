from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.cita import CitaCrear, CitaActualizar, CitaEnBD
from app.models.usuario import Usuario
from app.data import cita as citas_sql
from .autenticacion import obtener_usuario_actual


router = APIRouter(prefix="/citas", tags=["citas"])

# ============================================================
# ✅ OBTENER TODAS LAS CITAS
# ============================================================
@router.get("/", response_model=List[dict])
def obtener_citas():
    return citas_sql.obtener_citas()

# ============================================================
# ✅ OBTENER CITA POR ID
# ============================================================
@router.get("/{id_cita}", response_model=dict)
def obtener_cita_por_id(id_cita: int):
    cita = citas_sql.obtener_cita_por_id(id_cita)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

# ============================================================
# ✅ CREAR CITA
# ============================================================
@router.post("/", response_model=dict)
def crear_cita(cita: CitaCrear):
    nuevo_id = citas_sql.insertar_cita(
        cita.id_usuario,
        cita.id_servicio,
        cita.id_empleado,
        cita.fecha_cita,
        cita.hora_inicio,
        cita.estado,
    )
    return {"mensaje": "Cita registrada correctamente", "id_cita": nuevo_id}

# ============================================================
# ✅ ACTUALIZAR CITA
# ============================================================
@router.put("/{id_cita}", response_model=dict)
def actualizar_cita(id_cita: int, cita: CitaActualizar, usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    cita_actual = citas_sql.obtener_cita_por_id(id_cita)
    if not cita_actual:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    actualizado = citas_sql.actualizar_cita_por_id(id_cita, cita)
    if not actualizado:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    return {"mensaje": "Cita actualizada correctamente"}

# ============================================================
# ✅ ELIMINAR CITA
# ============================================================
@router.delete("/{id_cita}", response_model=dict)
def eliminar_cita(id_cita: int):
    eliminado = citas_sql.eliminar_cita(id_cita)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return {"mensaje": "Cita eliminada correctamente"}


@router.patch("/{cita_id}", response_model=dict)
def actualizar_estado_cita(cita_id: int, datos: CitaActualizar, usuario_actual: Usuario = Depends(obtener_usuario_actual)):
    # Solo admins pueden cambiar estados de citas
    if usuario_actual.id_rol != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acceso denegado. Solo administradores pueden cambiar estados.")
    
    cita = citas_sql.obtener_cita_por_id(cita_id)
    if not cita:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada")
    
    # Aplicar solo los campos presentes en `datos`
    actualizado = citas_sql.actualizar_cita_por_id(cita_id, datos)
    if not actualizado:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar o sin cambios")
    
    return {"mensaje": "Cita actualizada correctamente"}