from fastapi import APIRouter, Depends, HTTPException, Path, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.models import Request, User, EstadoRequest
from app.schemas import RequestCreate, RequestOut
from app.auth.auth_utils import get_current_user
from app import schemas
from reportlab.pdfgen import canvas
from fastapi.responses import FileResponse
import os


router = APIRouter()

@router.get("/requests/", response_model=list[schemas.RequestOut])
def listar_solicitudes(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado. Solo administradores.")
    
    return db.query(Request).all()

from fastapi import Form

@router.post("/requests/", response_model=RequestOut)
async def crear_solicitud(
    tipo: str = Form(...),
    nombre_usuario: str = Form(...),
    apellido_usuario: str = Form(...),
    fecha_nacimiento: str = Form(None),
    lugar_nacimiento: str = Form(None),
    lugar_estudio: str = Form(None),
    fecha_inicio_estudios: str = Form(None),
    fecha_fin_estudios: str = Form(None),
    cedula_archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.rol != "cliente":
        raise HTTPException(status_code=403, detail="Solo los clientes pueden crear solicitudes.")

    nueva_solicitud = Request(
        tipo=tipo,
        nombre_usuario=nombre_usuario,
        apellido_usuario=apellido_usuario,
        fecha_nacimiento=fecha_nacimiento,
        lugar_nacimiento=lugar_nacimiento,
        lugar_estudio=lugar_estudio,
        fecha_inicio_estudios=fecha_inicio_estudios,
        fecha_fin_estudios=fecha_fin_estudios,
        estado="pendiente",
        user_id=current_user.id
    )

    # Guardar archivo de cédula
    carpeta = "cedulas"
    os.makedirs(carpeta, exist_ok=True)
    nombre_archivo = f"cedula_{current_user.id}_{cedula_archivo.filename}"
    ruta_destino = os.path.join(carpeta, nombre_archivo)

    with open(ruta_destino, "wb") as buffer:
        buffer.write(await cedula_archivo.read())

    nueva_solicitud.cedula_path = ruta_destino

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

    if solicitud.estado in [EstadoRequest.rechazado, EstadoRequest.aprobado]:
        raise HTTPException(status_code=400, detail="La solicitud ya fue rechazada o aprobada y no puede modificarse.")

    solicitud.estado = EstadoRequest.en_validacion
    db.commit()
    db.refresh(solicitud)

    return solicitud

@router.put("/requests/{id}/aprobar", response_model=schemas.RequestOut)
def aprobar_solicitud(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado.")

    solicitud = db.query(Request).filter(Request.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    if solicitud.estado in [EstadoRequest.aprobado, EstadoRequest.rechazado]:
        raise HTTPException(status_code=400, detail="No se puede modificar una solicitud que ya fue aprobada o rechazada.")

    if solicitud.estado not in [EstadoRequest.en_validacion, EstadoRequest.correccion]:
        raise HTTPException(status_code=400, detail="Solo se puede aprobar desde 'en_validación' o 'corrección'.")

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

    if solicitud.estado != EstadoRequest.en_validacion:
        raise HTTPException(status_code=400, detail="Solo se puede solicitar corrección desde 'en_validación'.")

    solicitud.estado = EstadoRequest.correccion
    db.commit()
    db.refresh(solicitud)

    return solicitud

@router.put("/requests/{id}/rechazar", response_model=schemas.RequestOut)
def rechazar_solicitud(
    id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado.")

    solicitud = db.query(Request).filter(Request.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    if solicitud.estado in [EstadoRequest.aprobado, EstadoRequest.rechazado]:
        raise HTTPException(status_code=400, detail="No se puede modificar una solicitud que ya fue aprobada o rechazada.")

    if solicitud.estado not in [EstadoRequest.en_validacion, EstadoRequest.correccion]:
        raise HTTPException(status_code=400, detail="Solo se puede rechazar desde 'en_validación' o 'corrección'.")

    solicitud.estado = EstadoRequest.rechazado
    db.commit()
    db.refresh(solicitud)

    return solicitud


@router.post("/requests/{id}/upload", response_model=schemas.RequestOut)
def subir_documento(
    id: int,
    archivo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    solicitud = db.query(Request).filter(Request.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    if solicitud.user_id != current_user.id and current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para modificar esta solicitud.")

    # Carpeta donde guardas los archivos
    import os
    carpeta = "archivos"
    os.makedirs(carpeta, exist_ok=True)

    nombre_archivo = f"request_{id}_{archivo.filename}"
    ruta_destino = os.path.join(carpeta, nombre_archivo)

    if solicitud.estado in [EstadoRequest.aprobado, EstadoRequest.rechazado]:
        raise HTTPException(status_code=400, detail="No se puede adjuntar archivos a una solicitud aprobada o rechazada.")

    with open(ruta_destino, "wb") as buffer:
        buffer.write(archivo.file.read())

    solicitud.archivo_path = ruta_destino
    db.commit()
    db.refresh(solicitud)

    return solicitud


@router.get("/requests/{id}/certificado", response_class=FileResponse)
def generar_certificado_pdf(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    solicitud = db.query(Request).filter(Request.id == id).first()
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada.")

    if solicitud.estado != EstadoRequest.aprobado:
        raise HTTPException(status_code=400, detail="Solo se puede generar certificado de una solicitud aprobada.")

    if solicitud.user_id != current_user.id and current_user.rol != "admin":
        raise HTTPException(status_code=403, detail="No tienes permiso para acceder a esta solicitud.")

    carpeta_certificados = "certificados"
    os.makedirs(carpeta_certificados, exist_ok=True)

    nombre_archivo = f"certificado_{id}.pdf"
    ruta_certificado = os.path.join(carpeta_certificados, nombre_archivo)

    c = canvas.Canvas(ruta_certificado)
    c.setFont("Helvetica", 12)

        # Normalizamos el tipo de certificado
    tipo_normalizado = solicitud.tipo.lower()

    if "nacimiento" in tipo_normalizado:
        c.drawString(100, 750, " CERTIFICADO DE NACIMIENTO ")
        c.drawString(100, 720, f"Nombre: {solicitud.nombre_usuario} {solicitud.apellido_usuario}")
        c.drawString(100, 700, f"Fecha de nacimiento: {solicitud.fecha_nacimiento}")
        c.drawString(100, 680, f"Lugar de nacimiento: {solicitud.lugar_nacimiento or 'No especificado'}")
        c.drawString(100, 640, "Este documento certifica el nacimiento registrado en el sistema.")
    else:
        c.drawString(100, 750, " CERTIFICADO DE ESTUDIOS ")
        c.drawString(100, 720, f"Nombre: {solicitud.nombre_usuario} {solicitud.apellido_usuario}")
        c.drawString(100, 700, f"Fecha de nacimiento: {solicitud.fecha_nacimiento}")
        c.drawString(100, 680, f"Lugar de estudios: {solicitud.lugar_estudio}")
        
        fecha_fin = solicitud.fecha_fin_estudios if solicitud.fecha_fin_estudios else "Actualmente cursando"
        

        c.drawString(100, 660, f"Desde: {solicitud.fecha_inicio_estudios}")
        c.drawString(250, 660, f"Hasta: {fecha_fin}")
        
        c.drawString(100, 620, "Este documento certifica la aprobación del ciclo académico.")

    # Firma institucional
    c.drawString(100, 600, "Emitido electrónicamente por el sistema institucional.")
    c.showPage()
    c.save()

    return FileResponse(ruta_certificado, media_type='application/pdf', filename=nombre_archivo)

@router.get("/mis-requests/", response_model=list[schemas.RequestOut])
def listar_mis_solicitudes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Request).filter(Request.user_id == current_user.id).all()
