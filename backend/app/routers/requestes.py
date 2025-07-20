from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import Request, User
from app.schemas import RequestCreate, RequestOut
from app.auth.auth_utils import get_current_user

router = APIRouter()

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
