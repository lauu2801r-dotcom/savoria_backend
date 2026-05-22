from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.auth import models, schemas
import bcrypt

router = APIRouter()


def _hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def _verificar(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


@router.post("/registro", response_model=schemas.UsuarioRespuesta)
def registro(data: schemas.RegistroData, db: Session = Depends(get_db)):
    existe = db.query(models.Usuario).filter(
        models.Usuario.email == data.email).first()
    if existe:
        raise HTTPException(status_code=400,
                            detail="Ya existe una cuenta con ese correo")
    usuario = models.Usuario(
        nombre=data.nombre,
        email=data.email,
        password=_hash(data.password),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.post("/login", response_model=schemas.UsuarioRespuesta)
def login(data: schemas.LoginData, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.email == data.email).first()
    if not usuario or not _verificar(data.password, usuario.password):
        raise HTTPException(status_code=401,
                            detail="Correo o contraseña incorrectos")
    return usuario