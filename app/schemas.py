from pydantic import BaseModel, Field, EmailStr, condecimal
from typing import Optional
from enum import Enum

# Enum para estado
class EstadoTiendaEnum(str, Enum):
    pendiente = 'pendiente'
    aprobada = 'aprobada'
    rechazada = 'rechazada'
    inactiva = 'inactiva'

# ---------- Categoría ----------
class CategoriaTiendaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estado: Optional[str] = "activa"

class CategoriaTiendaCreate(CategoriaTiendaBase):
    pass

class CategoriaTiendaOut(CategoriaTiendaBase):
    id: int
    model_config = {
        "from_attributes": True
    }

# ---------- Tienda ----------
class TiendaBase(BaseModel):
    usuario_dueno_id: int
    nombre: str
    descripcion: Optional[str] = None
    direccion_fisica: str
    telefono_contacto: str
    correo_contacto: Optional[EmailStr] = None
    categoria_id: int
    latitud: Optional[condecimal(max_digits=10, decimal_places=8)]
    longitud: Optional[condecimal(max_digits=11, decimal_places=8)]
    estado: Optional[EstadoTiendaEnum] = EstadoTiendaEnum.pendiente

class TiendaCreate(TiendaBase):
    pass

class TiendaOut(TiendaBase):
    id: int
    calificacion_promedio: float
    class Config:
        orm_mode = True
