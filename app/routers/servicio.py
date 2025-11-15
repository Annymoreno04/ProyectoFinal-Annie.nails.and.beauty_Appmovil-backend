from fastapi import APIRouter, HTTPException
from typing import List
from app.models.servicio import ServicioEnBD, ServicioCrear, ServicioActualizar
from app.data import servicio as servicios_sql

router = APIRouter(prefix="/servicios", tags=["Servicios"])


# ============================================================
# ✅ OBTENER TODOS LOS SERVICIOS
# ============================================================
@router.get("/", response_model=List[ServicioEnBD])
def obtener_servicios():
    return servicios_sql.obtener_todos()


# ============================================================
# ✅ OBTENER SERVICIO POR ID
# ============================================================
@router.get("/{id_servicio}", response_model=ServicioEnBD)
def obtener_servicio(id_servicio: int):
    servicio = servicios_sql.obtener_por_id(id_servicio)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


# ============================================================
# ✅ CREAR NUEVO SERVICIO
# ============================================================
@router.post("/", response_model=dict)
def crear_servicio(servicio: ServicioCrear):
    nuevo_id = servicios_sql.insertar(servicio)  # ✅ corregido aquí
    return {"mensaje": "Servicio creado correctamente", "id_servicio": nuevo_id}


# ============================================================
# ✅ ACTUALIZAR SERVICIO
# ============================================================
@router.put("/{id_servicio}", response_model=dict)
def actualizar_servicio(id_servicio: int, servicio: ServicioActualizar):
    actualizado = servicios_sql.actualizar(id_servicio, servicio)
    if not actualizado:
        raise HTTPException(status_code=404, detail="Servicio no encontrado o sin cambios")
    return {"mensaje": "Servicio actualizado correctamente"}


# ============================================================
# ✅ ELIMINAR SERVICIO
# ============================================================
@router.delete("/{id_servicio}", response_model=dict)
def eliminar_servicio(id_servicio: int):
    eliminado = servicios_sql.eliminar(id_servicio)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"mensaje": "Servicio eliminado correctamente"}
