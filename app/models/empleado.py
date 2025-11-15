from pydantic import BaseModel, field_validator
from datetime import timedelta
from typing import Optional

class EmpleadoEnBD(BaseModel):
    id_empleado: int
    id_usuario: int
    nombre: Optional[str] = None  # 👈 AÑADIDO
    especialidad: Optional[str] = None
    anos_experiencia: Optional[int] = None
    descripcion: Optional[str] = None
    hora_inicio_atencion: Optional[str] = None
    hora_fin_atencion: Optional[str] = None
    estado: Optional[str] = None
  
    # ✅ convierte valores tipo timedelta (que vienen desde MySQL) a string legible
    @field_validator("hora_inicio_atencion", "hora_fin_atencion", mode="before")
    def convertir_tiempo(cls, v):
        if isinstance(v, timedelta):
            total_seconds = int(v.total_seconds())
            horas = total_seconds // 3600
            minutos = (total_seconds % 3600) // 60
            segundos = total_seconds % 60
            return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        return v

