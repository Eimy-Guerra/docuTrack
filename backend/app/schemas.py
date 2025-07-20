from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date
import enum

# ----------- ENUM -----------
class RequestType(str, enum.Enum):
    nacimiento = "cert_nacimiento"
    estudios = "cert_estudios"

class RolType(str, enum.Enum):
    admin = "admin"
    cliente = "cliente"


# ----------- AUTH SCHEMAS -----------

class LoginUser(BaseModel):
    correo: str
    contraseña: str

class Token(BaseModel):
    access_token: str
    token_type: str

# ----------- USER SCHEMAS -----------

class LoginUser(BaseModel):
    correo: str
    contraseña: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    nombre: str
    correo: EmailStr

class UserCreate(UserBase):
    contraseña: str
    rol: RolType  

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

# ----------- REQUEST SCHEMAS -----------

class RequestBase(BaseModel):
    tipo: RequestType
    nombre_usuario: str
    apellido_usuario: str
    fecha_nacimiento: Optional[date] = None
    fecha_inicio_estudios: Optional[date] = None
    fecha_fin_estudios: Optional[date] = None
    estado: str

class RequestCreate(BaseModel):  
    tipo: RequestType
    nombre_usuario: str
    apellido_usuario: str
    fecha_nacimiento: Optional[date] = None
    lugar_estudio: Optional[str] = None
    fecha_inicio_estudios: Optional[date] = None
    fecha_fin_estudios: Optional[date] = None

class RequestOut(RequestBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
    class Config:
        orm_mode = True

# ----------- DOCUMENT SCHEMAS -----------

class DocumentBase(BaseModel):
    dni_path: str

class DocumentCreate(DocumentBase):
    request_id: int

class DocumentOut(DocumentBase):
    id: int
    request_id: int

    class Config:
        orm_mode = True

# ----------- CERTIFICATE SCHEMAS -----------

class CertificateBase(BaseModel):
    tipo: RequestType
    titulo: str
    nombre_usuario: str
    apellido_usuario: str
    lugar_estudio: Optional[str] = None
    fecha_inicio_estudios: Optional[date] = None
    fecha_fin_estudios: Optional[date] = None  
    fecha_nacimiento: Optional[date] = None    

class CertificateCreate(CertificateBase):
    request_id: int

class CertificateOut(CertificateBase):
    id: int
    request_id: int

    class Config:
        orm_mode = True

