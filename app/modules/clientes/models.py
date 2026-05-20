from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    cliente_id      = Column(Integer, primary_key=True, index=True)
    nombre          = Column(String(100), nullable=False)
    nit             = Column(String(20), unique=True, nullable=False)
    direccion       = Column(String(255), nullable=True)
    telefono        = Column(String(20), nullable=True)
    email           = Column(String(100), nullable=True)
    fecha_registro  = Column(DateTime, server_default=func.now())

    facturas = relationship("Factura", back_populates="cliente")