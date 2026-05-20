from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.clientes import models, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.ClienteRespuesta])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(models.Cliente).all()


@router.get("/{cliente_id}", response_model=schemas.ClienteRespuesta)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.cliente_id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.post("/", response_model=schemas.ClienteRespuesta)
def crear_cliente(data: schemas.ClienteCrear, db: Session = Depends(get_db)):
    cliente = models.Cliente(**data.model_dump())
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.put("/{cliente_id}", response_model=schemas.ClienteRespuesta)
def actualizar_cliente(cliente_id: int, data: schemas.ClienteActualizar,
                       db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.cliente_id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(cliente, k, v)
    db.commit()
    db.refresh(cliente)
    return cliente


@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int, db: Session = Depends(get_db)):
    cliente = db.query(models.Cliente).filter(
        models.Cliente.cliente_id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    db.delete(cliente)
    db.commit()
    return {"mensaje": "Cliente eliminado"}