from fastapi import APIRouter, HTTPException
from typing import List
from app.data.trabajos import (
    insertar_trabajo,
    obtener_trabajos,
    obtener_trabajo_por_id,
    actualizar_trabajo,
    eliminar_trabajo,
)
from app.models.trabajos import Trabajo, TrabajoCrear, TrabajoActualizar

router = APIRouter(prefix="/trabajos", tags=["Trabajos"])


# ============================================================
# ✅ Crear trabajo
# ============================================================
@router.post("/", response_model=dict)
def crear_trabajo(data: TrabajoCrear):
    nuevo_id = insertar_trabajo(data.titulo, data.descripcion)
    return {"message": "✅ Trabajo creado exitosamente", "id": nuevo_id}


# ============================================================
# ✅ Obtener todos los trabajos
# ============================================================
@router.get("/", response_model=List[Trabajo])
def listar_trabajos():
    # obtener_trabajos devuelve lista de dicts; FastAPI convertirá a modelos
    return obtener_trabajos()


# ============================================================
# ✅ Obtener un trabajo por ID
# ============================================================
@router.get("/{id_trabajo}", response_model=Trabajo)
def obtener_trabajo(id_trabajo: int):
    trabajo = obtener_trabajo_por_id(id_trabajo)
    if not trabajo:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    return trabajo


# ============================================================
# ✅ Actualizar trabajo
# ============================================================
@router.put("/{id_trabajo}", response_model=dict)
def modificar_trabajo(id_trabajo: int, data: TrabajoActualizar):
    # si quieres permitir actualizar solo algunos campos
    # obtén el registro actual para completar valores faltantes (opcional)
    filas = actualizar_trabajo(id_trabajo, data.titulo, data.descripcion)
    if filas == 0:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado o sin cambios")
    return {"message": "✅ Trabajo actualizado correctamente"}


# ============================================================
# ✅ Eliminar trabajo
# ============================================================
@router.delete("/{id_trabajo}", response_model=dict)
def borrar_trabajo(id_trabajo: int):
    filas = eliminar_trabajo(id_trabajo)
    if filas == 0:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    return {"message": "🗑️ Trabajo eliminado correctamente"}
