from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import date, time

class CitaBase(BaseModel):
    id_usuario: int
    id_servicio: int
    id_empleado: Optional[int] = None
    fecha_cita: date
    hora_inicio: time
    estado: Optional[str] = "pendiente"

class CitaCrear(CitaBase):
    """Modelo para crear una nueva cita"""
    pass

class CitaEnBD(CitaBase):
    """Modelo que representa una cita en la base de datos"""
    id_cita: int

    class Config:
        from_attributes = True

class CitaActualizar(BaseModel):
    """
    Modelo para actualizaciones parciales de citas.
    Todos los campos son opcionales.
    """
    estado: Optional[Literal['pendiente', 'confirmada','cancelada', 'completada', 'no_realizada']] = None
    fecha_cita: Optional[date] = None
    hora_inicio: Optional[time] = None
    id_servicio: Optional[int] = None
    id_empleado: Optional[int] = None
    
    @field_validator('estado', mode='before')
    @classmethod
    def validar_estado(cls, v):
        """Normaliza el estado a minúsculas y maneja strings vacíos"""
        if v is None or v == '':
            return None
        if isinstance(v, str):
            v = v.strip().lower()
            estados_validos = ['pendiente', 'confirmada','cancelada', 'completada', 'no_realizada']
            if v not in estados_validos:
                raise ValueError(f'Estado debe ser uno de: {estados_validos}')
            return v
        return v
    
    @field_validator('fecha_cita', mode='before')
    @classmethod
    def validar_fecha(cls, v):
        """Maneja strings vacíos y None"""
        if v is None or v == '':
            return None
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            try:
                from datetime import datetime
                return datetime.strptime(v, '%Y-%m-%d').date()
            except ValueError:
                raise ValueError('Fecha debe estar en formato YYYY-MM-DD')
        return v
    
    @field_validator('hora_inicio', mode='before')
    @classmethod
    def validar_hora(cls, v):
        """Maneja strings vacíos, None y formatos variados de hora"""
        if v is None or v == '':
            return None
        if isinstance(v, time):
            return v
        if isinstance(v, str):
            try:
                from datetime import datetime
                v = v.strip()
                if len(v) == 8 and v.count(':') == 2:
                    return datetime.strptime(v, '%H:%M:%S').time()
                elif len(v) == 5 and v.count(':') == 1:
                    return datetime.strptime(v, '%H:%M').time()
                else:
                    raise ValueError('Formato de hora no reconocido')
            except ValueError as e:
                raise ValueError(f'Hora debe estar en formato HH:MM:SS o HH:MM: {str(e)}')
        return v
    
    @field_validator('id_servicio', 'id_empleado', mode='before')
    @classmethod
    def validar_ids(cls, v):
        """Maneja strings vacíos y convierte a int"""
        if v is None or v == '':
            return None
        try:
            return int(v)
        except (ValueError, TypeError):
            raise ValueError('ID debe ser un número entero')
    
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat() if v else None,
            time: lambda v: v.isoformat() if v else None,
        }
        extra = 'ignore'
        validate_assignment = True