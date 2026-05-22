from pydantic import BaseModel, EmailStr


class RegistroData(BaseModel):
    nombre: str
    email: EmailStr
    password: str


class LoginData(BaseModel):
    email: EmailStr
    password: str


class UsuarioRespuesta(BaseModel):
    usuario_id: int
    nombre: str
    email: str

    class Config:
        from_attributes = True