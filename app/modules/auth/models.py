from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    usuario_id  = Column(Integer, primary_key=True, index=True)
    nombre      = Column(String(100), nullable=False)
    email       = Column(String(100), unique=True, nullable=False, index=True)
    password    = Column(String(255), nullable=False)
    creado_en   = Column(DateTime(timezone=True), server_default=func.now())