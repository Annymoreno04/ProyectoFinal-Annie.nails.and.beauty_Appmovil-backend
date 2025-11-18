from app.core.db import get_conn
import traceback

def insertar_cita(id_usuario, id_servicio, id_empleado, fecha_cita, hora_inicio, estado="pendiente"):
    conexion = get_conn()
    with conexion.cursor() as cursor:
        cursor.execute("""
            INSERT INTO citas (id_usuario, id_servicio, id_empleado, fecha_cita, hora_inicio, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_usuario, id_servicio, id_empleado, fecha_cita, hora_inicio, estado))
        conexion.commit()
        return cursor.lastrowid

def obtener_citas():
    conexion = get_conn()
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT 
                c.id_cita,
                c.fecha_cita,
                c.hora_inicio,
                c.estado,
                u.id_usuario,
                u.nombre AS nombre_usuario,
                u.telefono,
                s.id_servicio,
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

def obtener_cita_por_id(id_cita):
    conexion = get_conn()
    with conexion.cursor(dictionary=True) as cursor:
        cursor.execute("""
            SELECT 
                c.id_cita,
                c.fecha_cita,
                c.hora_inicio,
                c.estado,
                u.id_usuario,
                u.nombre AS nombre_usuario,
                u.telefono,
                s.id_servicio,
                s.titulo AS servicio,
                e.id_empleado,
                e.descripcion AS descripcion_empleado
            FROM citas c
            INNER JOIN usuarios u ON c.id_usuario = u.id_usuario
            INNER JOIN servicios s ON c.id_servicio = s.id_servicio
            LEFT JOIN empleados e ON c.id_empleado = e.id_empleado
            WHERE c.id_cita = %s
            ORDER BY c.fecha_cita DESC, c.hora_inicio ASC
        """, (id_cita,))
        return cursor.fetchone()

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


def eliminar_cita(id_cita):
    conexion = get_conn()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM citas WHERE id_cita = %s", (id_cita,))
        conexion.commit()
        return cursor.rowcount


def actualizar_cita_por_id(id_cita, datos):
    """
    Actualiza solo los campos presentes en el objeto datos.
    """
    conexion = None
    cursor = None
    
    try:
        conexion = get_conn()
        
        if not conexion.is_connected():
            print("⚠️ Conexión perdida, reconectando...")
            conexion.reconnect(attempts=3, delay=1)
        
        cursor = conexion.cursor()
        campos = []
        params = []
        
        datos_dict = datos.dict(exclude_none=True)
        
        print(f"🔍 Datos recibidos: {datos_dict}")
        
        if not datos_dict:
            print(f"⚠️ Sin campos para actualizar en cita {id_cita}")
            return 0
    
        if 'estado' in datos_dict:
            valor_estado = datos_dict['estado']
            print(f"🔍 Estado detectado: '{valor_estado}'")
            
            estados_validos = ['pendiente', 'confirmada','cancelada', 'completada', 'no_realizada']
            if valor_estado.lower() not in estados_validos:
                raise ValueError(f"Estado inválido: '{valor_estado}'. Debe ser uno de: {estados_validos}")
            
            campos.append("estado = %s")
            params.append(valor_estado.lower())
            
        # Procesar otros campos
        if 'fecha_cita' in datos_dict:
            valor_fecha = datos_dict['fecha_cita']
            campos.append("fecha_cita = %s")
            if hasattr(valor_fecha, 'isoformat'):
                params.append(valor_fecha.isoformat())
            else:
                params.append(str(valor_fecha))
            
        if 'hora_inicio' in datos_dict:
            valor_hora = datos_dict['hora_inicio']
            campos.append("hora_inicio = %s")
            if hasattr(valor_hora, 'isoformat'):
                params.append(valor_hora.isoformat())
            else:
                params.append(str(valor_hora))
            
        if 'id_servicio' in datos_dict:
            campos.append("id_servicio = %s")
            params.append(int(datos_dict['id_servicio']))
            
        if 'id_empleado' in datos_dict:
            campos.append("id_empleado = %s")
            params.append(int(datos_dict['id_empleado']))
        
        if not campos:
            print(f"⚠️ Sin campos válidos para actualizar")
            return 0
        
        params.append(int(id_cita))
        sql = "UPDATE citas SET " + ", ".join(campos) + " WHERE id_cita = %s"
        
        print(f"📝 SQL: {sql}")
        print(f"📝 Params: {params}")
        
        cursor.execute(sql, tuple(params))
        conexion.commit()
        filas_afectadas = cursor.rowcount
        
        print(f"✅ Cita {id_cita} actualizada: {filas_afectadas} fila(s)")
        
        # Verificar
        cursor.execute("SELECT estado, fecha_cita, hora_inicio FROM citas WHERE id_cita = %s", (id_cita,))
        resultado = cursor.fetchone()
        print(f"✅ Valores en BD: {resultado}")
        
        return filas_afectadas
        
    except Exception as e:
        print(f"❌ ERROR: {type(e).__name__}: {str(e)}")
        print(traceback.format_exc())
        
        if conexion and conexion.is_connected():
            try:
                conexion.rollback()
            except:
                pass
        raise
        
    finally:
        if cursor:
            try:
                cursor.close()
            except:
                pass
        if conexion and conexion.is_connected():
            try:
                conexion.close()
            except:
                pass