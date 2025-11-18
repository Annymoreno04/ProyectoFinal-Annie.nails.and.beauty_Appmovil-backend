from fastapi import APIRouter, HTTPException
from app.models.categoria_servicio import Categoria, CategoriaCrear
from app.data import categoria_servicio as categoria_repo

router = APIRouter(prefix="/Categoria_servicios", tags=["Categoría_servicios"])

@router.post("/", response_model=Categoria)
def crear_categoria(categoria: CategoriaCrear):
    nuevo_id = categoria_repo.insertar_categoria(categoria.nombre, categoria.descripcion)
    return Categoria(id_categoria=nuevo_id, **categoria.dict())

@router.get("/", response_model=list[Categoria])
def listar_categorias():
    return categoria_repo.obtener_categorias()

@router.get("/{id_categoria}", response_model=Categoria)
def obtener_categoria(id_categoria: int):
    categoria = categoria_repo.obtener_categoria_por_id(id_categoria)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

@router.put("/{id_categoria}")
def actualizar_categoria(id_categoria: int, categoria: CategoriaCrear):
    filas_afectadas = categoria_repo.actualizar_categoria(
        id_categoria, categoria.nombre, categoria.descripcion
    )
    if filas_afectadas == 0:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"mensaje": "Categoría actualizada correctamente"}


@router.delete("/{id_categoria}")
def eliminar_categoria(id_categoria: int):
    filas_afectadas = categoria_repo.eliminar_categoria(id_categoria)
    if filas_afectadas == 0:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return {"mensaje": "Categoría eliminada correctamente"}
