
from fastapi import APIRouter, Depends
from app.models.usuario import Usuario
from .autenticacion import obtener_usuario_actual
from ..models.dashboard import RespuestaDashboard, NombreValor
from app.core.db import get_conn

router = APIRouter()

@router.get("/dashboard", response_model=RespuestaDashboard)
def obtener_dashboard(usuario_actual: Usuario = Depends(obtener_usuario_actual)):

    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

  
    sql_citas_mes = """
        SELECT DAY(fecha_cita) AS dia, COUNT(*) AS total
        FROM citas
        WHERE MONTH(fecha_cita) = MONTH(CURDATE())
        AND YEAR(fecha_cita) = YEAR(CURDATE())
        GROUP BY dia
        ORDER BY dia
    """
    cursor.execute(sql_citas_mes)
    datos_citas_mes = cursor.fetchall()

    citas_mes = [
        NombreValor(nombre=str(r["dia"]), valor=r["total"])
        for r in datos_citas_mes
    ]

 
    sql_citas_categoria = """
        SELECT cs.nombre AS categoria, COUNT(*) AS total
        FROM citas c
        JOIN servicios s ON c.id_servicio = s.id_servicio
        JOIN categorias_servicios cs ON s.id_categoria = cs.id_categoria
        GROUP BY cs.id_categoria, cs.nombre
        ORDER BY total DESC
    """
    cursor.execute(sql_citas_categoria)
    datos_categoria = cursor.fetchall()

    citas_categorias = [
        NombreValor(nombre=r["categoria"], valor=r["total"])
        for r in datos_categoria
    ]

   
    sql_citas_servicio = """
        SELECT s.titulo AS servicio, COUNT(*) AS total
        FROM citas c
        JOIN servicios s ON c.id_servicio = s.id_servicio
        GROUP BY s.id_servicio, s.titulo
        ORDER BY total DESC
        LIMIT 5
    """
    cursor.execute(sql_citas_servicio)
    datos_servicios = cursor.fetchall()

    citas_servicios = [
        NombreValor(nombre=r["servicio"], valor=r["total"])
        for r in datos_servicios
    ]

    sql_citas_estado = """
        SELECT estado, COUNT(*) AS total
        FROM citas
        GROUP BY estado
    """
    cursor.execute(sql_citas_estado)
    datos_estado = cursor.fetchall()

    citas_estado = [
        NombreValor(nombre=r["estado"], valor=r["total"])
        for r in datos_estado
    ]


    tarjetas = []


    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
    tarjetas.append(NombreValor(nombre="Usuarios", valor=cursor.fetchone()["total"]))

    cursor.execute("SELECT COUNT(*) AS total FROM empleados")
    tarjetas.append(NombreValor(nombre="Empleados", valor=cursor.fetchone()["total"]))

    cursor.execute("SELECT COUNT(*) AS total FROM servicios")
    tarjetas.append(NombreValor(nombre="Servicios", valor=cursor.fetchone()["total"]))

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM citas
        WHERE MONTH(fecha_cita) = MONTH(CURDATE())
        AND YEAR(fecha_cita) = YEAR(CURDATE())
    """)
    tarjetas.append(NombreValor(nombre="Citas del mes", valor=cursor.fetchone()["total"]))

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM citas
        WHERE estado = 'completada'
    """)
    tarjetas.append(NombreValor(nombre="Citas completadas", valor=cursor.fetchone()["total"]))

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM citas
        WHERE estado = 'cancelada'
    """)
    tarjetas.append(NombreValor(nombre="Citas canceladas", valor=cursor.fetchone()["total"]))

    return RespuestaDashboard(
        ventas_mes=citas_mes,              
        ventas_tiendas=citas_categorias,   
        ventas_categorias=citas_servicios, 
        tarjetas=tarjetas
    )
