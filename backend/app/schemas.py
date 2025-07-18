from pydantic import BaseModel, EmailStr

# Esquema para crear un usuario (entrada)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str  # ✅ Contraseña en texto plano (será encriptada en el CRUD)

# Esquema para leer un usuario (salida)
class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True  # ✅ Permite convertir objetos SQLAlchemy en respuestas JSON
