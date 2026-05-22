import shutil
import uuid
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.articulos import models, schemas

UPLOAD_DIR = "uploads/articulos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

EXTENSIONES_PERMITIDAS = {"jpg", "jpeg", "png", "webp"}

router = APIRouter()


@router.get("/", response_model=list[schemas.ArticuloRespuesta])
def listar_articulos(db: Session = Depends(get_db)):
    return db.query(models.Articulo).all()


@router.get("/{articulo_id}", response_model=schemas.ArticuloRespuesta)
def obtener_articulo(articulo_id: int, db: Session = Depends(get_db)):
    articulo = db.query(models.Articulo).filter(
        models.Articulo.articulo_id == articulo_id).first()
    if not articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return articulo


@router.post("/", response_model=schemas.ArticuloRespuesta)
def crear_articulo(data: schemas.ArticuloCrear, db: Session = Depends(get_db)):
    articulo = models.Articulo(**data.model_dump())
    db.add(articulo)
    db.commit()
    db.refresh(articulo)
    return articulo


@router.put("/{articulo_id}", response_model=schemas.ArticuloRespuesta)
def actualizar_articulo(articulo_id: int, data: schemas.ArticuloActualizar,
                        db: Session = Depends(get_db)):
    articulo = db.query(models.Articulo).filter(
        models.Articulo.articulo_id == articulo_id).first()
    if not articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(articulo, k, v)
    db.commit()
    db.refresh(articulo)
    return articulo


@router.delete("/{articulo_id}")
def eliminar_articulo(articulo_id: int, db: Session = Depends(get_db)):
    articulo = db.query(models.Articulo).filter(
        models.Articulo.articulo_id == articulo_id).first()
    if not articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    if articulo.imagen_url and articulo.imagen_url.startswith("/uploads/"):
        ruta = articulo.imagen_url.lstrip("/")
        if os.path.exists(ruta):
            os.remove(ruta)
    db.delete(articulo)
    db.commit()
    return {"mensaje": "Artículo eliminado"}


@router.post("/{articulo_id}/imagen", response_model=schemas.ArticuloRespuesta)
def subir_imagen(
    articulo_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    articulo = db.query(models.Articulo).filter(
        models.Articulo.articulo_id == articulo_id).first()
    if not articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    # Validar extensión
    ext = file.filename.split(".")[-1].lower()
    if ext not in EXTENSIONES_PERMITIDAS:
        raise HTTPException(
            status_code=400,
            detail=f"Formato no permitido. Usa: {', '.join(EXTENSIONES_PERMITIDAS)}"
        )

    # Validar tamaño (máx 5MB)
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)
    if size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="La imagen no puede superar 5MB")

    # Eliminar imagen anterior si existía
    if articulo.imagen_url and articulo.imagen_url.startswith("/uploads/"):
        ruta_anterior = articulo.imagen_url.lstrip("/")
        if os.path.exists(ruta_anterior):
            os.remove(ruta_anterior)

    # Guardar archivo en disco
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Guardar en BD con retry por si Neon cerró la conexión
    nueva_url = f"/uploads/articulos/{filename}"
    intentos = 3
    for intento in range(intentos):
        try:
            db.expire_all()
            articulo = db.query(models.Articulo).filter(
                models.Articulo.articulo_id == articulo_id).first()
            articulo.imagen_url = nueva_url
            db.commit()
            db.refresh(articulo)
            return articulo
        except Exception as e:
            db.rollback()
            if intento < intentos - 1:
                continue
            if os.path.exists(filepath):
                os.remove(filepath)
            raise HTTPException(
                status_code=500,
                detail="Error al guardar en base de datos, intenta de nuevo"
            )