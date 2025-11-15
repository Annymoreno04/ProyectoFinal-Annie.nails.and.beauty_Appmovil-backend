# app/rutas/empleados.py

from fastapi import APIRouter, HTTPException
from typing import List
from app.models.empleado import EmpleadoEnBD
from app.core.db import get_conn  # conexión directa a la base de datos

router = APIRouter(
    prefix="/empleados",
    tags=["Empleados"]
)

# ============================================================
# ✅ OBTENER TODOS LOS EMPLEADOS
# ============================================================
@router.get("/", response_model=List[EmpleadoEnBD])
def obtener_empleados():
    sql = """
        SELECT 
            e.id_empleado,
            e.id_usuario,
            u.nombre,              -- ✅ nombre del usuario
            e.especialidad,
            e.anos_experiencia,
            e.descripcion,
            e.hora_inicio_atencion,
            e.hora_fin_atencion,
            e.estado
        FROM empleados e
        INNER JOIN usuarios u ON e.id_usuario = u.id_usuario
        ORDER BY e.id_empleado ASC
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql)
    filas = cur.fetchall()
    cur.close()
    conn.close()

    if not filas:
        raise HTTPException(status_code=404, detail="No hay empleados registrados")

    return [EmpleadoEnBD(**fila) for fila in filas]



# ============================================================
# ✅ OBTENER EMPLEADO POR ID_USUARIO
# ============================================================
@router.get("/usuario/{id_usuario}", response_model=EmpleadoEnBD)
def obtener_empleado_por_usuario(id_usuario: int):
    sql = """
        SELECT 
            id_empleado, id_usuario, especialidad, anos_experiencia,
            descripcion, hora_inicio_atencion, hora_fin_atencion, estado
        FROM empleados
        WHERE id_usuario = %s
        LIMIT 1
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql, (id_usuario,))
    fila = cur.fetchone()
    cur.close()
    conn.close()

    if not fila:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    return EmpleadoEnBD(**fila)


# ============================================================
# ✅ CREAR NUEVO EMPLEADO
# ============================================================
@router.post("/", response_model=dict)
def crear_empleado(empleado: EmpleadoEnBD):
    sql = """
        INSERT INTO empleados (
            id_usuario, especialidad, anos_experiencia, descripcion,
            hora_inicio_atencion, hora_fin_atencion, estado
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    valores = (
        empleado.id_usuario,
        empleado.especialidad,
        empleado.anos_experiencia,
        empleado.descripcion,
        empleado.hora_inicio_atencion,
        empleado.hora_fin_atencion,
        empleado.estado or "activo"
    )

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, valores)
    conn.commit()
    nuevo_id = cur.lastrowid
    cur.close()
    conn.close()

    return {"mensaje": "Empleado registrado correctamente", "id_empleado": nuevo_id}


# ============================================================
# ✅ ACTUALIZAR EMPLEADO
# ============================================================
@router.put("/{id_empleado}", response_model=dict)
def actualizar_empleado(id_empleado: int, empleado: EmpleadoEnBD):
    sql = """
        UPDATE empleados
        SET 
            especialidad = %s,
            anos_experiencia = %s,
            descripcion = %s,
            hora_inicio_atencion = %s,
            hora_fin_atencion = %s,
            estado = %s
        WHERE id_empleado = %s
    """

    valores = (
        empleado.especialidad,
        empleado.anos_experiencia,
        empleado.descripcion,
        empleado.hora_inicio_atencion,
        empleado.hora_fin_atencion,
        empleado.estado,
        id_empleado
    )

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, valores)
    conn.commit()
    actualizado = cur.rowcount > 0
    cur.close()
    conn.close()

    if not actualizado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado o sin cambios")

    return {"mensaje": "Empleado actualizado correctamente"}


# ============================================================
# ✅ ELIMINAR EMPLEADO
# ============================================================
@router.delete("/{id_empleado}", response_model=dict)
def eliminar_empleado(id_empleado: int):
    sql = "DELETE FROM empleados WHERE id_empleado = %s"

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, (id_empleado,))
    conn.commit()
    eliminado = cur.rowcount > 0
    cur.close()
    conn.close()

    if not eliminado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    return {"mensaje": "Empleado eliminado correctamente"}
