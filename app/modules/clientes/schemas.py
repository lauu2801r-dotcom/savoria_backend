from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ClienteCrear(BaseModel):
    nombre: str
    nit: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None


class ClienteActualizar(BaseModel):
    nombre: Optional[str] = None
    nit: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None


class ClienteRespuesta(BaseModel):
    cliente_id: int
    nombre: str
    nit: str
    direccion: Optional[str]
    telefono: Optional[str]
    email: Optional[str]
    fecha_registro: Optional[datetime]

    class Config:
        from_attributes = True