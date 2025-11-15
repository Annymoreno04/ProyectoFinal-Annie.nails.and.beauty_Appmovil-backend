from fastapi import APIRouter, HTTPException
from typing import List
from app.models.tutoriales import TutorialCrear, TutorialActualizar,TutorialEnBD
from app.data import tutoriales as tutoriales_sql

router = APIRouter(prefix="/tutoriales", tags=["Tutoriales"])

# ============================================================
# OBTENER TODOS LOS TUTORIALES
# ============================================================
@router.get("/", response_model=List[TutorialEnBD])
def obtener_tutoriales():
    return tutoriales_sql.obtener_tutoriales()

# ============================================================
# OBTENER TUTORIAL POR ID
# ============================================================
@router.get("/{id_tutorial}", response_model=TutorialEnBD)
def obtener_tutorial(id_tutorial: int):
    tutorial = tutoriales_sql.obtener_por_id(id_tutorial)
    if not tutorial:
        raise HTTPException(status_code=404, detail="Tutorial no encontrado")
    return tutorial

# ============================================================
# CREAR TUTORIAL
# ============================================================
@router.post("/", response_model=TutorialEnBD)
def crear_tutorial(tutorial: TutorialCrear):
    nuevo_id = tutoriales_sql.insertar_tutorial(
        tutorial.id_categoria,
        tutorial.titulo,
        tutorial.descripcion
    )
    return {"mensaje": "Tutorial registrado correctamente", "id": nuevo_id}

# ============================================================
# ACTUALIZAR TUTORIAL
# ============================================================
@router.put("/{id_tutorial}", response_model=TutorialEnBD)
def actualizar_tutorial(id_tutorial: int, tutorial: TutorialActualizar):
    actualizado = tutoriales_sql.actualizar_tutorial(
        id_tutorial,
        tutorial.id_categoria,
        tutorial.titulo,
        tutorial.descripcion
    )
    if not actualizado:
        raise HTTPException(status_code=404, detail="Tutorial no encontrado o sin cambios")
    return {"mensaje": "Tutorial actualizado correctamente"}

# ============================================================
# ELIMINAR TUTORIAL
# ============================================================
@router.delete("/{id_tutorial}", response_model=TutorialEnBD)
def eliminar_tutorial(id_tutorial: int):
    eliminado = tutoriales_sql.eliminar_tutorial(id_tutorial)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Tutorial no encontrado")
    return {"mensaje": "Tutorial eliminado correctamente"}
