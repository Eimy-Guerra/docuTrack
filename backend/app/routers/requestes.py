from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import Request, User, EstadoRequest
from app.schemas import RequestCreate, RequestOut
from app.auth.auth_utils import get_current_user
from app import schemas



router = APIRouter()

@router.get("/requests/", response_model=list[schemas.RequestOut])
def listar_solicitudes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado. Solo administradores.")
    
    return db.query(Request).all()

@router.post("/requests/", response_model=RequestOut)
def crear_solicitud(
    solicitud: RequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.rol != "cliente":
        raise HTTPException(status_code=403, detail="Solo los clientes pueden crear solicitudes.")

    nueva_solicitud = Request(
        tipo=solicitud.tipo,
        nombre_usuario=solicitud.nombre_usuario,
        apellido_usuario=solicitud.apellido_usuario,
        fecha_nacimiento=solicitud.fecha_nacimiento,
        lugar_estudio=solicitud.lugar_estudio,
        fecha_inicio_estudios=solicitud.fecha_inicio_estudios,
        fecha_fin_estudios=solicitud.fecha_fin_estudios,
        estado="pendiente",
        user_id=current_user.id
    )

    db.add(nueva_solicitud)
    db.commit()
    db.refresh(nueva_solicitud)

    return nueva_solicitud

@router.get("/requests/{request_id}", response_model=schemas.RequestOut)
def obtener_solicitud_individual(
    request_id: int = Path(..., title="ID de la solicitud"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado. Solo administradores.")

    solicitud = db.query(Request).filter(Request.id == request_id).first()

    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    return solicitud

@router.put("/requests/{id}/validar", response_model=schemas.RequestOut)
def validar_solicitud(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado.")

    solicitud = db.query(Request).filter(Request.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    solicitud.estado = EstadoRequest.en_validacion
    db.commit()
    db.refresh(solicitud)

    return solicitud

@router.put("/requests/{id}/aprobar", response_model=schemas.RequestOut)
def aprobar_solicitud(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado.")

    solicitud = db.query(Request).filter(Request.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    solicitud.estado = EstadoRequest.aprobado
    db.commit()
    db.refresh(solicitud)

    return solicitud

@router.put("/requests/{id}/corregir", response_model=schemas.RequestOut)
def solicitar_correccion(id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado.")

    solicitud = db.query(Request).filter(Request.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    solicitud.estado = EstadoRequest.correccion
    db.commit()
    db.refresh(solicitud)

    return solicitud

