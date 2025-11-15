from app.core.db import get_conn

# ============================================================
# ✅ Insertar trabajo
# ============================================================
def insertar_trabajo(titulo, descripcion):
    conexion = get_conn()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO trabajos (titulo, descripcion) VALUES (%s, %s)",
                (titulo, descripcion)
            )
            conexion.commit()
            return cursor.lastrowid
    except Exception as e:
        conexion.rollback()
        print(f"❌ Error al insertar trabajo: {e}")
        raise
    finally:
        conexion.close()


# ============================================================
# ✅ Listar todos los trabajos
# ============================================================
def obtener_trabajos():
    conexion = get_conn()
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM trabajos")
            return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener trabajos: {e}")
        raise
    finally:
        conexion.close()


# ============================================================
# ✅ Obtener un trabajo por ID
# ============================================================
def obtener_trabajo_por_id(id_trabajo):
    conexion = get_conn()
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT * FROM trabajos WHERE id = %s",
                (id_trabajo,)
            )
            return cursor.fetchone()
    except Exception as e:
        print(f"❌ Error al obtener trabajo: {e}")
        raise
    finally:
        conexion.close()


# ============================================================
# ✅ Actualizar trabajo
# ============================================================
def actualizar_trabajo(id_trabajo, titulo, descripcion):
    conexion = get_conn()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE trabajos SET titulo = %s, descripcion = %s WHERE id = %s",
                (titulo, descripcion, id_trabajo)
            )
            conexion.commit()
            return cursor.rowcount
    except Exception as e:
        conexion.rollback()
        print(f"❌ Error al actualizar trabajo: {e}")
        raise
    finally:
        conexion.close()


# ============================================================
# ✅ Eliminar trabajo
# ============================================================
def eliminar_trabajo(id_trabajo):
    conexion = get_conn()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "DELETE FROM trabajos WHERE id = %s",
                (id_trabajo,)
            )
            conexion.commit()
            return cursor.rowcount
    except Exception as e:
        conexion.rollback()
        print(f"❌ Error al eliminar trabajo: {e}")
        raise
    finally:
        conexion.close()
