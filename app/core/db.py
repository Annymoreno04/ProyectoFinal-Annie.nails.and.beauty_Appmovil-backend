
import mysql.connector                

# ------------------------
# Función de conexión a MySQL
# ------------------------
def get_conn():
    # Retorna un objeto de conexión a la base de datos MySQL
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="annienails"
    )
