from sqlalchemy import (
    Column, Integer, String, Numeric,
    DateTime, ForeignKey, Text, Date
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Factura(Base):
    __tablename__ = "facturas"

    factura_id       = Column(Integer, primary_key=True, index=True)
    numero_factura   = Column(String(20), unique=True, nullable=False)
    cliente_id       = Column(Integer, ForeignKey("clientes.cliente_id"), nullable=False)
    fecha_emision    = Column(Date, nullable=False)
    fecha_vencimiento= Column(Date, nullable=True)
    subtotal         = Column(Numeric(10, 2), default=0)
    impuestos        = Column(Numeric(10, 2), default=0)
    total            = Column(Numeric(10, 2), nullable=False)
    estado           = Column(String(20), default="Pendiente")
    notas            = Column(Text, nullable=True)
    creado_en        = Column(DateTime, server_default=func.now())

    cliente  = relationship("Cliente", back_populates="facturas")
    detalles = relationship(
        "DetalleFactura",
        back_populates="factura",
        cascade="all, delete-orphan"
    )


class DetalleFactura(Base):
    __tablename__ = "detalle_factura"

    detalle_id      = Column(Integer, primary_key=True, index=True)
    factura_id      = Column(Integer, ForeignKey("facturas.factura_id"), nullable=False)
    articulo_id     = Column(Integer, ForeignKey("articulos.articulo_id"), nullable=False)
    cantidad        = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    subtotal_linea  = Column(Numeric(10, 2), nullable=False)
    impuestos_linea = Column(Numeric(10, 2), nullable=False)
    total_linea     = Column(Numeric(10, 2), nullable=False)

    factura  = relationship("Factura", back_populates="detalles")
    articulo = relationship("Articulo", back_populates="detalles")