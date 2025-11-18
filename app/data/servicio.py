from typing import List, Optional
from app.core.db import get_conn
from app.models.servicio import ServicioEnBD, ServicioCrear, ServicioActualizar


def obtener_todos() -> List[ServicioEnBD]:
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM servicios")
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return [ServicioEnBD(**fila) for fila in filas]

def obtener_por_id(id_servicio: int) -> Optional[ServicioEnBD]:
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM servicios WHERE id_servicio = %s", (id_servicio,))
    fila = cur.fetchone()
    cur.close()
    conn.close()
    return ServicioEnBD(**fila) if fila else None


def insertar(servicio: ServicioCrear) -> int:
    conn = get_conn()
    cur = conn.cursor()
    sql = """
        INSERT INTO servicios (id_categoria, titulo, descripcion, duracion_minutos)
        VALUES (%s, %s, %s, %s)
    """
    valores = (
        servicio.id_categoria,
        servicio.titulo,
        servicio.descripcion,
        servicio.duracion_minutos,
    )
    cur.execute(sql, valores)
    conn.commit()
    nuevo_id = cur.lastrowid
    cur.close()
    conn.close()
    return nuevo_id

def actualizar(id_servicio: int, servicio: ServicioActualizar) -> bool:
    campos = []
    valores = []

    if servicio.titulo is not None:
        campos.append("titulo = %s")
        valores.append(servicio.titulo)
    if servicio.descripcion is not None:
        campos.append("descripcion = %s")
        valores.append(servicio.descripcion)
    if servicio.duracion_minutos is not None:
        campos.append("duracion_minutos = %s")
        valores.append(servicio.duracion_minutos)

    if not campos:
        return False

    valores.append(id_servicio)
    sql = f"UPDATE servicios SET {', '.join(campos)} WHERE id_servicio = %s"

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, tuple(valores))
    conn.commit()
    actualizado = cur.rowcount > 0
    cur.close()
    conn.close()
    return actualizado


def eliminar(id_servicio: int) -> bool:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM servicios WHERE id_servicio = %s", (id_servicio,))
    conn.commit()
    eliminado = cur.rowcount > 0
    cur.close()
    conn.close()
    return eliminado
