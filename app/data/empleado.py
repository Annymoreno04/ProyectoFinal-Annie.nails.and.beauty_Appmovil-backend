# app/repositorios/empleados_sql.py

from typing import Optional, List
from app.core.db import get_conn  # ✅ conexión a la base de datos
from app.models.empleado import EmpleadoEnBD


# ============================================================
# ✅ OBTENER EMPLEADO POR ID_USUARIO
# ============================================================
def obtener_por_id_usuario(id_usuario: int) -> Optional[EmpleadoEnBD]:
    """
    Obtiene un empleado según el ID de usuario vinculado.
    """
    consulta = """
        SELECT 
            id_empleado,
            id_usuario,
            especialidad,
            anos_experiencia,
            descripcion,
            hora_inicio_atencion,
            hora_fin_atencion,
            estado
        FROM empleados
        WHERE id_usuario = %s
        LIMIT 1
    """

    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(consulta, (id_usuario,))
    fila = cur.fetchone()
    cur.close()
    conn.close()

    if not fila:
        return None

    return EmpleadoEnBD(**fila)


# ============================================================
# ✅ INSERTAR EMPLEADO
# ============================================================
def insertar_empleado(empleado: EmpleadoEnBD) -> int:
    """
    Inserta un nuevo empleado en la base de datos.
    Retorna el ID autoincremental generado.
    """
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
        empleado.estado,
    )

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, valores)
    conn.commit()
    nuevo_id = cur.lastrowid
    cur.close()
    conn.close()

    return nuevo_id


# ============================================================
# ✅ OBTENER TODOS LOS EMPLEADOS
# ============================================================
def obtener_todos() -> List[EmpleadoEnBD]:
    """
    Devuelve la lista de todos los empleados registrados.
    """
    sql = """
        SELECT 
            id_empleado,
            id_usuario,
            especialidad,
            anos_experiencia,
            descripcion,
            hora_inicio_atencion,
            hora_fin_atencion,
            estado
        FROM empleados
        ORDER BY id_empleado ASC
    """

    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute(sql)
    filas = cur.fetchall()
    cur.close()
    conn.close()

    return [EmpleadoEnBD(**fila) for fila in filas]


# ============================================================
# ✅ ACTUALIZAR EMPLEADO
# ============================================================
def actualizar_empleado(id_empleado: int, empleado: EmpleadoEnBD) -> bool:
    """
    Actualiza los datos de un empleado existente.
    Retorna True si la operación fue exitosa.
    """
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

    return actualizado


# ============================================================
# ✅ ELIMINAR EMPLEADO
# ============================================================
def eliminar_empleado(id_empleado: int) -> bool:
    """
    Elimina un empleado de la base de datos.
    Retorna True si la eliminación fue exitosa.
    """
    sql = "DELETE FROM empleados WHERE id_empleado = %s"

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, (id_empleado,))
    conn.commit()
    eliminado = cur.rowcount > 0
    cur.close()
    conn.close()

    return eliminado
