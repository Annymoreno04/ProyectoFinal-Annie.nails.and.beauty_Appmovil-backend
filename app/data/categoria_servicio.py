from app.core.db import get_conn

def insertar_categoria(nombre, descripcion):
    conexion = get_conn()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "INSERT INTO categorias_servicios (nombre, descripcion) VALUES (%s, %s)",
                (nombre, descripcion)
            )
            conexion.commit()
            return cursor.lastrowid
    except Exception as e:
        conexion.rollback()
        print(f"❌ Error al insertar categoría: {e}")
        raise
    finally:
        conexion.close()

def obtener_categorias():
    conexion = get_conn()
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM categorias_servicios")
            return cursor.fetchall()
    except Exception as e:
        print(f"❌ Error al obtener categorías: {e}")
        raise
    finally:
        conexion.close()

def obtener_categoria_por_id(id_categoria):
    conexion = get_conn()
    try:
        with conexion.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT * FROM categorias_servicios WHERE id_categoria = %s",
                (id_categoria,)
            )
            return cursor.fetchone()
    except Exception as e:
        print(f"❌ Error al obtener categoría: {e}")
        raise
    finally:
        conexion.close()


def actualizar_categoria(id_categoria, nombre, descripcion):
    conexion = get_conn()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "UPDATE categorias_servicios SET nombre = %s, descripcion = %s WHERE id_categoria = %s",
                (nombre, descripcion, id_categoria)
            )
            conexion.commit()
            return cursor.rowcount
    except Exception as e:
        conexion.rollback()
        print(f"❌ Error al actualizar categoría: {e}")
        raise
    finally:
        conexion.close()  


def eliminar_categoria(id_categoria):
    conexion = get_conn()
    try:
        with conexion.cursor() as cursor:
            cursor.execute(
                "DELETE FROM categorias_servicios WHERE id_categoria = %s",
                (id_categoria,)
            )
            conexion.commit()
            return cursor.rowcount
    except Exception as e:
        conexion.rollback()
        print(f"❌ Error al eliminar categoría: {e}")
        raise
    finally:
        conexion.close()
