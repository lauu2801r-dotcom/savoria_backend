from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.facturas import models, schemas
from app.modules.articulos.models import Articulo
from datetime import date

router = APIRouter()

IVA = 0.19


def _generar_numero(db: Session) -> str:
    total = db.query(models.Factura).count()
    return f"FAC-{str(total + 1).zfill(4)}"


@router.get("/", response_model=list[schemas.FacturaRespuesta])
def listar_facturas(db: Session = Depends(get_db)):
    return db.query(models.Factura).all()


@router.get("/{factura_id}", response_model=schemas.FacturaRespuesta)
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(models.Factura).filter(
        models.Factura.factura_id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura


@router.post("/", response_model=schemas.FacturaRespuesta)
def crear_factura(data: schemas.FacturaCrear, db: Session = Depends(get_db)):
    detalles = []
    subtotal = 0

    for d in data.detalles:
        articulo = db.query(Articulo).filter(
            Articulo.articulo_id == d.articulo_id).first()
        if not articulo:
            raise HTTPException(
                status_code=404,
                detail=f"Artículo {d.articulo_id} no encontrado")

        subtotal_linea = d.precio_unitario * d.cantidad
        impuestos_linea = subtotal_linea * IVA
        total_linea = subtotal_linea + impuestos_linea
        subtotal += subtotal_linea

        detalles.append(models.DetalleFactura(
            articulo_id=d.articulo_id,
            cantidad=d.cantidad,
            precio_unitario=d.precio_unitario,
            subtotal_linea=subtotal_linea,
            impuestos_linea=impuestos_linea,
            total_linea=total_linea,
        ))

        # Descontar stock
        articulo.stock = max(0, articulo.stock - d.cantidad)

    impuestos = subtotal * IVA
    total = subtotal + impuestos

    factura = models.Factura(
        numero_factura=_generar_numero(db),
        cliente_id=data.cliente_id,
        fecha_emision=data.fecha_emision,
        fecha_vencimiento=data.fecha_vencimiento,
        subtotal=subtotal,
        impuestos=impuestos,
        total=total,
        estado=data.estado,
        notas=data.notas,
        detalles=detalles,
    )

    db.add(factura)
    db.commit()
    db.refresh(factura)
    return factura


@router.put("/{factura_id}", response_model=schemas.FacturaRespuesta)
def actualizar_factura(factura_id: int, data: schemas.FacturaActualizar,
                       db: Session = Depends(get_db)):
    factura = db.query(models.Factura).filter(
        models.Factura.factura_id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    for k, v in data.model_dump(exclude_none=True).items():
        setattr(factura, k, v)
    db.commit()
    db.refresh(factura)
    return factura


@router.delete("/{factura_id}")
def eliminar_factura(factura_id: int, db: Session = Depends(get_db)):
    factura = db.query(models.Factura).filter(
        models.Factura.factura_id == factura_id).first()
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    db.delete(factura)
    db.commit()
    return {"mensaje": "Factura eliminada"}