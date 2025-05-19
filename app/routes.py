from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import SessionLocal

tienda_router = APIRouter(prefix="/api", tags=["Tiendas"])

# Dependencia para obtener sesión de DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- CATEGORÍAS ----------

@tienda_router.get("/categorias_tienda", response_model=List[schemas.CategoriaTiendaOut])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(models.CategoriaTienda).all()

@tienda_router.get("/categorias_tienda/{categoria_id}", response_model=schemas.CategoriaTiendaOut)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(models.CategoriaTienda).filter(models.CategoriaTienda.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")
    return categoria

@tienda_router.post("/categorias_tienda", response_model=schemas.CategoriaTiendaOut)
def crear_categoria(categoria: schemas.CategoriaTiendaCreate, db: Session = Depends(get_db)):
    existente = db.query(models.CategoriaTienda).filter(models.CategoriaTienda.nombre == categoria.nombre).first()
    if existente:
        raise HTTPException(status_code=400, detail="La categoría ya existe.")
    nueva = models.CategoriaTienda(**categoria.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@tienda_router.put("/categorias_tienda/{categoria_id}", response_model=schemas.CategoriaTiendaOut)
def actualizar_categoria(categoria_id: int, nueva_categoria: schemas.CategoriaTiendaCreate, db: Session = Depends(get_db)):
    categoria = db.query(models.CategoriaTienda).filter(models.CategoriaTienda.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")

    for key, value in nueva_categoria.dict().items():
        setattr(categoria, key, value)

    db.commit()
    db.refresh(categoria)
    return categoria

@tienda_router.delete("/categorias_tienda/{categoria_id}")
def desactivar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = db.query(models.CategoriaTienda).filter(models.CategoriaTienda.id == categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")

    categoria.estado = "inactiva"
    db.commit()
    return {"msg": "Categoría marcada como inactiva."}

# ---------- TIENDAS ----------

@tienda_router.post("/tiendas", response_model=schemas.TiendaOut)
def crear_tienda(tienda: schemas.TiendaCreate, db: Session = Depends(get_db)):
    nueva = models.Tienda(**tienda.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@tienda_router.get("/tiendas", response_model=List[schemas.TiendaOut])
def listar_tiendas(db: Session = Depends(get_db)):
    return db.query(models.Tienda).all()

@tienda_router.get("/tiendas/{tienda_id}", response_model=schemas.TiendaOut)
def obtener_tienda(tienda_id: int, db: Session = Depends(get_db)):
    tienda = db.query(models.Tienda).filter(models.Tienda.id == tienda_id).first()
    if not tienda:
        raise HTTPException(status_code=404, detail="Tienda no encontrada.")
    return tienda

@tienda_router.put("/tiendas/{tienda_id}", response_model=schemas.TiendaOut)
def actualizar_tienda(tienda_id: int, tienda_actualizada: schemas.TiendaCreate, db: Session = Depends(get_db)):
    tienda = db.query(models.Tienda).filter(models.Tienda.id == tienda_id).first()
    if not tienda:
        raise HTTPException(status_code=404, detail="Tienda no encontrada.")

    for key, value in tienda_actualizada.dict().items():
        setattr(tienda, key, value)

    db.commit()
    db.refresh(tienda)
    return tienda

@tienda_router.delete("/tiendas/{tienda_id}")
def desactivar_tienda(tienda_id: int, db: Session = Depends(get_db)):
    tienda = db.query(models.Tienda).filter(models.Tienda.id == tienda_id).first()
    if not tienda:
        raise HTTPException(status_code=404, detail="Tienda no encontrada.")

    tienda.estado = models.EstadoTiendaEnum.inactiva
    db.commit()
    return {"msg": "Tienda marcada como inactiva."}
