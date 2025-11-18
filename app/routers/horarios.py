
from fastapi import APIRouter, HTTPException
from app.core.db import get_conn  

router = APIRouter(
    prefix="/horarios",
    tags=["Horarios"]
)

@router.get("/")
def obtener_horarios():
    try:
        conn = get_conn()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM horarios ORDER BY id ASC")
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        return data

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Error al obtener horarios")
