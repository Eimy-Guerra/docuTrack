from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import timedelta
from typing import Optional

from app.database.database import SessionLocal
from app.models import models
from app import schemas

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------- Seguridad JWT -----------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "tu_clave_secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar el token.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user

# ----------- UTILS -----------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ----------- CREATE USER -----------
@router.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        nombre=user.nombre,
        correo=user.correo,
        contraseña=hash_password(user.contraseña),
        rol=user.rol
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ----------- GET ALL USERS – SOLO ADMIN -----------
@router.get("/users/", response_model=list[schemas.UserOut])
def get_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado.")
    return db.query(models.User).all()

# ----------- GET USER BY ID – SOLO ADMIN O DUEÑO -----------
@router.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.rol != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Solo puedes acceder a tu perfil.")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# ----------- UPDATE USER – SOLO ADMIN O DUEÑO -----------
@router.put("/users/{user_id}", response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user_update: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.rol != "admin" and current_user.id != user_id:
        raise HTTPException(status_code=403, detail="No tienes permiso para editar este perfil.")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    user.nombre = user_update.nombre
    user.correo = user_update.correo
    user.contraseña = hash_password(user_update.contraseña)
    user.rol = user_update.rol
    db.commit()
    db.refresh(user)
    return user

# ----------- DELETE USER – SOLO ADMIN -----------
@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Solo el administrador puede eliminar usuarios.")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    return {"mensaje": f"Usuario con ID {user_id} eliminado correctamente"}
