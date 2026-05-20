from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.modules.facturas.models import Factura, DetalleFactura
from app.modules.articulos.models import Articulo
from app.modules.clientes.models import Cliente

router = APIRouter()


@router.get("/resumen")
def resumen_general(db: Session = Depends(get_db)):
    total_facturas = db.query(Factura).count()
    total_clientes = db.query(Cliente).count()
    total_articulos = db.query(Articulo).count()
    total_ventas = db.query(
        func.sum(Factura.total)
    ).filter(Factura.estado == "Pagada").scalar() or 0
    stock_bajo = db.query(Articulo).filter(Articulo.stock <= 3).count()

    return {
        "total_facturas": total_facturas,
        "total_clientes": total_clientes,
        "total_articulos": total_articulos,
        "total_ventas": float(total_ventas),
        "articulos_stock_bajo": stock_bajo,
    }


@router.get("/ventas-por-categoria")
def ventas_por_categoria(db: Session = Depends(get_db)):
    resultado = db.query(
        Articulo.categoria,
        func.sum(DetalleFactura.total_linea).label("total")
    ).join(DetalleFactura).group_by(Articulo.categoria).all()

    return [{"categoria": r[0], "total": float(r[1])} for r in resultado]


@router.get("/top-articulos")
def top_articulos(db: Session = Depends(get_db)):
    resultado = db.query(
        Articulo.nombre,
        func.sum(DetalleFactura.cantidad).label("total_vendido")
    ).join(DetalleFactura).group_by(Articulo.nombre)\
     .order_by(func.sum(DetalleFactura.cantidad).desc())\
     .limit(5).all()

    return [{"nombre": r[0], "total_vendido": int(r[1])} for r in resultado]