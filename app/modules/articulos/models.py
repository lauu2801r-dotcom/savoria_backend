from sqlalchemy import Column, Integer, String, Numeric, Text
from app.core.database import Base
from sqlalchemy.orm import relationship


class Articulo(Base):
    __tablename__ = "articulos"

    articulo_id     = Column(Integer, primary_key=True, index=True)
    nombre          = Column(String(100), nullable=False)
    descripcion     = Column(Text, nullable=True)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    stock           = Column(Integer, default=0)
    codigo          = Column(String(20), unique=True, nullable=True)
    categoria       = Column(String(50), nullable=True)
    imagen_url = Column(String(255), nullable=True)

    detalles = relationship("DetalleFactura", back_populates="articulo")