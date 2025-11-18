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


@router.post("/", response_model=dict)
def crear_trabajo(data: TrabajoCrear):
    nuevo_id = insertar_trabajo(data.titulo, data.descripcion)
    return {"message": "✅ Trabajo creado exitosamente", "id": nuevo_id}

@router.get("/", response_model=List[Trabajo])
def listar_trabajos():
    return obtener_trabajos()


@router.get("/{id_trabajo}", response_model=Trabajo)
def obtener_trabajo(id_trabajo: int):
    trabajo = obtener_trabajo_por_id(id_trabajo)
    if not trabajo:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    return trabajo


@router.put("/{id_trabajo}", response_model=dict)
def modificar_trabajo(id_trabajo: int, data: TrabajoActualizar):

    filas = actualizar_trabajo(id_trabajo, data.titulo, data.descripcion)
    if filas == 0:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado o sin cambios")
    return {"message": "✅ Trabajo actualizado correctamente"}


@router.delete("/{id_trabajo}", response_model=dict)
def borrar_trabajo(id_trabajo: int):
    filas = eliminar_trabajo(id_trabajo)
    if filas == 0:
        raise HTTPException(status_code=404, detail="Trabajo no encontrado")
    return {"message": "🗑️ Trabajo eliminado correctamente"}
