from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base
import enum

class RequestType(str, enum.Enum):
    nacimiento = "cert_nacimiento"
    estudios = "cert_estudios"

class EstadoRequest(str, enum.Enum):
    pendiente = "pendiente"
    en_validacion = "en_validacion"
    aprobado = "aprobado"
    rechazado = "rechazado"
    correccion = "corrección"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    correo = Column(String, unique=True, index=True, nullable=False)
    contraseña = Column(String, nullable=False)
    rol = Column(String, nullable=False)

    requests = relationship("Request", back_populates="usuario")


class Request(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(RequestType), nullable=False)
    nombre_usuario = Column(String, nullable=False)
    apellido_usuario = Column(String, nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    lugar_nacimiento = Column(String, nullable=True)
    lugar_estudio = Column(String, nullable=True)
    fecha_inicio_estudios = Column(Date, nullable=True)
    fecha_fin_estudios = Column(Date, nullable=True)
    estado = Column(String, nullable=False, default=EstadoRequest.pendiente)

    archivo_path = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    usuario = relationship("User", back_populates="requests")

    document = relationship("Document", back_populates="request", uselist=False)
    certificate = relationship("Certificate", back_populates="request", uselist=False)


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    dni_path = Column(String, nullable=False)

    request_id = Column(Integer, ForeignKey("requests.id"))
    request = relationship("Request", back_populates="document")


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(RequestType), nullable=False)
    titulo = Column(String, nullable=False)
    nombre_usuario = Column(String, nullable=False)
    apellido_usuario = Column(String, nullable=False)
    lugar_estudio = Column(String, nullable=True)
    fecha_inicio_estudios = Column(Date, nullable=True)
    fecha_fin_estudios = Column(Date, nullable=True)  
    fecha_nacimiento = Column(Date, nullable=True)
    lugar_nacimiento = Column(String, nullable=True)    

    request_id = Column(Integer, ForeignKey("requests.id"))
    request = relationship("Request", back_populates="certificate")





