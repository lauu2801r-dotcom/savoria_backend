from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.articulos import models, schemas

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
    db.delete(articulo)
    db.commit()
    return {"mensaje": "Artículo eliminado"}