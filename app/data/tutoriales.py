
from app.core.db import get_conn


def obtener_tutoriales():
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tutoriales")
    tutoriales = cursor.fetchall()
    conn.close()
    return tutoriales


def obtener_tutorial_por_id(id_tutorial):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tutoriales WHERE id = %s", (id_tutorial,))
    tutorial = cursor.fetchone()
    conn.close()
    return tutorial

def insertar_tutorial(id_categoria, titulo, descripcion):
    conn = get_conn()
    cursor = conn.cursor()
    query = """
        INSERT INTO tutoriales (id_categoria, titulo, descripcion)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (id_categoria, titulo, descripcion))
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    return nuevo_id

def actualizar_tutorial(id_tutorial, id_categoria, titulo, descripcion):
    conn = get_conn()
    cursor = conn.cursor()

    query = """
        UPDATE tutoriales
        SET id_categoria = %s,
            titulo = %s,
            descripcion = %s
        WHERE id = %s
    """

    cursor.execute(query, (id_categoria, titulo, descripcion, id_tutorial))
    conn.commit()
    actualizado = cursor.rowcount > 0
    conn.close()
    return actualizado


def eliminar_tutorial(id_tutorial):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tutoriales WHERE id = %s", (id_tutorial,))
    conn.commit()
    eliminado = cursor.rowcount > 0
    conn.close()
    return eliminado
