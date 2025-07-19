from pydantic import BaseModel, EmailStr
from typing import Optional
import enum
from datetime import date

# ----------- ENUM -----------

class RequestType(str, enum.Enum):
    nacimiento = "cert_nacimiento"
    estudios = "cert_estudios"

# ----------- USER SCHEMAS -----------

class UserBase(BaseModel):
    nombre: str
    correo: EmailStr

class UserCreate(UserBase):
    contraseña: str
    rol: str

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

class RequestCreate(RequestBase):
    user_id: int

class RequestOut(RequestBase):
    id: int
    user_id: int

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

