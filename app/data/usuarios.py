# app/repositorios/usuarios_sql.py
from typing import Optional
from app.core.db import get_conn
from app.models.usuario import UsuarioEnBD, UsuarioActualizar


def obtener_por_nombre_usuario(nombre_usuario: str) -> Optional[UsuarioEnBD]:
    consulta = """
        SELECT  id_usuario, id_rol, nombre_usuario, nombre, telefono, correo, estado, clave
        FROM usuarios
        WHERE nombre_usuario = %s
        LIMIT 1
    """

    conn = get_conn()
 
    cursor = conn.cursor(dictionary=True)
    cursor.execute(consulta, (nombre_usuario,))
    fila = cursor.fetchone()
    cursor.close()

    if not fila:
        return None

    # Mapea dict a Pydantic; keys ya coinciden con nombres de campos
    return UsuarioEnBD(**fila)
 

def insertar_usuario(usuario: UsuarioEnBD):
    conn = get_conn()  # ✅ Llamar a la función correctamente
    cursor = conn.cursor()  # ✅ No es "cur()", es "cursor()"
    
    sql = """
        INSERT INTO usuarios (nombre_usuario, clave, nombre, telefono, correo, id_rol, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        usuario.nombre_usuario,
        usuario.clave,
        usuario.nombre,
        usuario.telefono,
        usuario.correo,
        usuario.id_rol,
        usuario.estado, 
    )
    
    cursor.execute(sql, valores)
    conn.commit()  # ✅ Guarda los cambios
    nuevo_id = cursor.lastrowid  # ✅ Obtiene el ID autoincremental
    
    cursor.close()
    conn.close()
    
    return nuevo_id


def actualizar_usuario(id_usuario: int, datos: UsuarioActualizar) -> UsuarioEnBD:
    conn = get_conn()
    cursor = conn.cursor()

    # Construir la consulta UPDATE dinámicamente solo con campos que no sean None
    campos = []
    valores = []
    
    if datos.nombre is not None:
        campos.append("nombre = %s")
        valores.append(datos.nombre)
    
    if datos.telefono is not None:
        campos.append("telefono = %s")
        valores.append(datos.telefono)
    
    if datos.correo is not None:
        campos.append("correo = %s")
        valores.append(datos.correo)
    
    if not campos:
        # Si no hay campos a actualizar, devolver usuario actual
        cursor.close()
        conn.close()
        return obtener_usuario_por_id(id_usuario)
    
    valores.append(id_usuario)
    
    consulta = f"UPDATE usuarios SET {', '.join(campos)} WHERE id_usuario = %s"
    
    cursor.execute(consulta, valores)
    conn.commit()  # ✅ Commit ANTES de recuperar los datos
    
    # Obtener el usuario actualizado con la MISMA conexión
    cursor_dict = conn.cursor(dictionary=True)  # ✅ Usar diccionario
    consulta_select = """
        SELECT id_usuario, id_rol, nombre_usuario, nombre, telefono, correo, estado, clave
        FROM usuarios
        WHERE id_usuario = %s
        LIMIT 1
    """
    
    cursor_dict.execute(consulta_select, (id_usuario,))
    fila = cursor_dict.fetchone()
    cursor.close()
    cursor_dict.close()
    conn.close()
    
    if not fila:
        raise ValueError(f"Usuario con ID {id_usuario} no encontrado")
    
    return UsuarioEnBD(**fila)


def obtener_usuario_por_id(id_usuario: int) -> Optional[UsuarioEnBD]:
    """Obtiene un usuario por su ID"""
    consulta = """
        SELECT id_usuario, id_rol, nombre_usuario, nombre, telefono, correo, estado, clave
        FROM usuarios
        WHERE id_usuario = %s
        LIMIT 1
    """
    
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(consulta, (id_usuario,))
    fila = cursor.fetchone()
    cursor.close()
    conn.close()

    if not fila:
        return None

    return UsuarioEnBD(**fila)



