from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.database import Base, engine
from app.core.config import settings
import os

# Importar modelos para que Alembic los detecte
from app.modules.clientes import models as clientes_models
from app.modules.articulos import models as articulos_models
from app.modules.facturas import models as facturas_models

# Importar routers
from app.modules.clientes.router import router as clientes_router
from app.modules.articulos.router import router as articulos_router
from app.modules.facturas.router import router as facturas_router
from app.modules.reportes.router import router as reportes_router

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# ← Agregar esta línea
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Crear carpeta de uploads si no existe
os.makedirs("uploads/articulos", exist_ok=True)

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

# CORS para Flutter
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Servir archivos estáticos (imágenes subidas)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(clientes_router, prefix="/clientes", tags=["Clientes"])
app.include_router(articulos_router, prefix="/articulos", tags=["Artículos"])
app.include_router(facturas_router, prefix="/facturas", tags=["Facturas"])
app.include_router(reportes_router, prefix="/reportes", tags=["Reportes"])

@app.get("/")
def root():
    return {"mensaje": "Savoria API funcionando 🍽️", "version": settings.VERSION}