from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime


class DetalleCrear(BaseModel):
    articulo_id: int
    cantidad: int
    precio_unitario: float


class DetalleRespuesta(BaseModel):
    detalle_id: int
    articulo_id: int
    cantidad: int
    precio_unitario: float
    subtotal_linea: float
    impuestos_linea: float
    total_linea: float

    class Config:
        from_attributes = True


class FacturaCrear(BaseModel):
    cliente_id: int
    fecha_emision: date
    fecha_vencimiento: Optional[date] = None
    estado: str = "Pendiente"
    notas: Optional[str] = None
    detalles: List[DetalleCrear]


class FacturaActualizar(BaseModel):
    estado: Optional[str] = None
    notas: Optional[str] = None


class FacturaRespuesta(BaseModel):
    factura_id: int
    numero_factura: str
    cliente_id: int
    fecha_emision: date
    fecha_vencimiento: Optional[date] = None
    subtotal: float
    impuestos: float
    total: float
    estado: str
    notas: Optional[str] = None
    creado_en: Optional[datetime] = None
    detalles: List[DetalleRespuesta] = []

    class Config:
        from_attributes = True