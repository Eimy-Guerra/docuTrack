from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database.database import SessionLocal
from app.models import models
from app import schemas
from app.auth.auth_utils import get_current_user, create_access_token  # ✅ Importar desde nuevo módulo

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------- DB DEPENDENCY -----------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------- UTILS -----------
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ----------- CREATE USER -----------
@router.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.correo == user.correo).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")

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

# ----------- TOKEN -----------
@router.post("/token", response_model=schemas.Token)
def login(
    user_login: schemas.LoginUser,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.correo == user_login.correo).first()
    if not user or not verify_password(user_login.contraseña, user.contraseña):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


