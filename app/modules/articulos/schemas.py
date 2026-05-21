from pydantic import BaseModel
from typing import Optional


class ArticuloCrear(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio_unitario: float
    stock: int = 0
    codigo: Optional[str] = None
    categoria: Optional[str] = None
    # En ArticuloCrear y ArticuloActualizar:
    imagen_url: Optional[str] = None

    # En ArticuloRespuesta:
    imagen_url: Optional[str] = None


class ArticuloActualizar(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_unitario: Optional[float] = None
    stock: Optional[int] = None
    codigo: Optional[str] = None
    categoria: Optional[str] = None
      # En ArticuloCrear y ArticuloActualizar:
    imagen_url: Optional[str] = None

    # En ArticuloRespuesta:
    imagen_url: Optional[str] = None

class ArticuloRespuesta(BaseModel):
    articulo_id: int
    nombre: str
    descripcion: Optional[str]
    precio_unitario: float
    stock: int
    codigo: Optional[str]
    categoria: Optional[str]
      # En ArticuloCrear y ArticuloActualizar:
    imagen_url: Optional[str] = None

    # En ArticuloRespuesta:
    imagen_url: Optional[str] = None

    class Config:
        from_attributes = True