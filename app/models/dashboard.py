from pydantic import BaseModel
from typing import List, Union


class NombreValor(BaseModel):
    nombre: str
    valor: Union[int, float]


class RespuestaDashboard(BaseModel):
    ventas_mes: List[NombreValor]            # Citas por día del mes
    ventas_tiendas: List[NombreValor]        # Citas por categoría
    ventas_categorias: List[NombreValor]     # Citas por servicio
    tarjetas: List[NombreValor]              # Métricas del dashboard
