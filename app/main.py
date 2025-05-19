from fastapi import FastAPI
from app.routes import tienda_router
from app.database import Base, engine

app = FastAPI(title="API de Tiendas", version="1.0.0")

# Crear las tablas automáticamente si no existen
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(tienda_router)
