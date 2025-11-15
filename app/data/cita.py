from app.core.db import get_conn

# ✅ Crear nueva cita
def insertar_cita(id_usuario, id_servicio, id_empleado, fecha_cita, hora_inicio, estado="pendiente"):
    conexion = get_conn()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO citas (id_usuario, id_servicio, id_empleado, fecha_cita, hora_inicio, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_usuario, id_servicio, id_empleado, fecha_cita, hora_inicio, estado))
        conexion.commit()
        return cursor.lastrowid

# ✅ Listar todas las citas
def obtener_citas():
    conexion = get_conn()
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT 
                c.id_cita,
                c.fecha_cita,
                c.hora_inicio,
                c.estado,
                u.nombre AS nombre_usuario,
                s.titulo AS servicio,
                e.id_empleado,
                e.descripcion AS descripcion_empleado
            FROM citas c
            INNER JOIN usuarios u ON c.id_usuario = u.id_usuario
            INNER JOIN servicios s ON c.id_servicio = s.id_servicio
            LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
            ORDER BY c.fecha_cita DESC, c.hora_inicio ASC
        """)
        return cursor.fetchall()

# ✅ Obtener una cita por ID
def obtener_cita_por_id(id_cita):
    conexion = get_conn()
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT 
                c.id_cita,
                c.fecha_cita,
                c.hora_inicio,
                c.estado,
                u.nombre AS nombre_usuario,
                s.titulo AS servicio,
                e.id_empleado,
                e.descripcion AS descripcion_empleado
            FROM citas c
            INNER JOIN usuarios u ON c.id_usuario = u.id_usuario
            INNER JOIN servicios s ON c.id_servicio = s.id_servicio
            LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
            WHERE c.id_cita = %s
        """, (id_cita,))
        return cursor.fetchone()

# ✅ Actualizar cita
def actualizar_cita(id_cita, id_servicio, id_empleado, fecha_cita, hora_inicio, estado):
    conexion = get_conn()
    with conexion.cursor() as cursor:
        cursor.execute("""
            UPDATE citas
            SET id_servicio = %s,
                id_empleado = %s,
                fecha_cita = %s,
                hora_inicio = %s,
                estado = %s
            WHERE id_cita = %s
        """, (id_servicio, id_empleado, fecha_cita, hora_inicio, estado, id_cita))
        conexion.commit()
        return cursor.rowcount

# ✅ Eliminar cita
def eliminar_cita(id_cita):
    conexion = get_conn()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM citas WHERE id_cita = %s", (id_cita,))
        conexion.commit()
        return cursor.rowcount


# ✅ Actualizar parcialmente una cita (solo campos presentes en `datos`)
def actualizar_cita_por_id(id_cita, datos):
    conexion = get_conn()
    with conexion.cursor() as cursor:
        campos = []
        params = []
        # `datos` es un objeto Pydantic; comprobamos atributos que no sean None
        if hasattr(datos, 'estado') and datos.estado is not None:
            campos.append("estado = %s")
            params.append(datos.estado)
        if hasattr(datos, 'fecha') and datos.fecha is not None:
            campos.append("fecha_cita = %s")
            params.append(datos.fecha)
        if hasattr(datos, 'hora') and datos.hora is not None:
            campos.append("hora_inicio = %s")
            params.append(datos.hora)

        if not campos:
            return 0

        params.append(id_cita)
        sql = "UPDATE citas SET " + ", ".join(campos) + " WHERE id_cita = %s"
        cursor.execute(sql, tuple(params))
        conexion.commit()
        return cursor.rowcount
