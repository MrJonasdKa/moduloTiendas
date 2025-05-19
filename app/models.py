from sqlalchemy import Column, Integer, String, Text, ForeignKey, DECIMAL, Enum, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base
import enum
from datetime import datetime

# Opcional: para manejar el enum de estado
class EstadoTiendaEnum(str, enum.Enum):
    pendiente = 'pendiente'
    aprobada = 'aprobada'
    rechazada = 'rechazada'
    inactiva = 'inactiva'

class CategoriaTienda(Base):
    __tablename__ = "categorias_tienda"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(Text)
    estado = Column(Enum("activa", "inactiva"), default="activa", nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    tiendas = relationship("Tienda", back_populates="categoria")

class Tienda(Base):
    __tablename__ = "tiendas"

    id = Column(Integer, primary_key=True, index=True)
    usuario_dueno_id = Column(Integer, nullable=False)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    direccion_fisica = Column(String(255), nullable=False)
    telefono_contacto = Column(String(20), nullable=False)
    correo_contacto = Column(String(255))
    categoria_id = Column(Integer, ForeignKey("categorias_tienda.id"), nullable=False)
    latitud = Column(DECIMAL(10, 8))
    longitud = Column(DECIMAL(11, 8))
    estado = Column(Enum(EstadoTiendaEnum), default=EstadoTiendaEnum.pendiente)
    calificacion_promedio = Column(DECIMAL(3, 2), default=0.00)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow)

    categoria = relationship("CategoriaTienda", back_populates="tiendas")
