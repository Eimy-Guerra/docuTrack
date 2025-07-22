# DocuTrack — Sistema de Solicitudes y Emisión de Certificados

Sistema enfocado en gestionar solicitudes ciudadanas de certificados de nacimiento y estudios.  

---

## Tecnologías Elegidas

| Tecnología    | ¿Por qué se eligió? |
|---------------|---------------------|
| **FastAPI**   | Backend rápido y moderno. Utiliza python por lo que la curva de aprendizaje no fue tan difícil. |
| **PostgreSQL**| Era lo solicitado. |
| **React & Next.js** | Frontend dinámico, orientado a componentes y con renderizado eficiente. |
| **JWT (JSON Web Tokens)** | Era lo solicitado. |
| **ReportLab (Python)** | Generación dinámica de certificados PDF con datos personalizados. |

---

#### Instalación y Ejecución

```bash
# Clona el repositorio
git clone https://github.com/usuario/docutrack.git

### Para Backend

## Crea y activa entorno virtual
python -m venv env
source env/bin/activate  # En Windows: \DocuTrack\ .\env\Scripts\activate


## Instala dependencias
pip install -r requirements.txt

# Ejecuta el servidor
\DocuTrack\backend> uvicorn main:app --reload


##Puertos:
Backend disponible en: http://localhost:8000 


### Para Frontend
cd docutrack/frontend


## Instala dependencias
npm install


## Ejecuta el servidor
DocuTrack\frontend> npm run dev


##Puertos:
Frontend disponible en: http://localhost:3000



La comunicación entre back y front ocurre cuando el frontend hace llamadas a la API del backend usando el puerto correspondiente (localhost:8000)


### Acceso y Roles

## Inicialización de la Base de Datos (Datos de Ejemplo)

Para facilitar la validación del sistema, se incluye un script que genera datos de prueba automáticos (init_db.py). Este script crea:

- 1 usuario de rol `USER` (Carlos Díaz)
- 1 usuario de rol `ADMIN` (María Torres)
- 1 solicitud de certificado tipo nacimiento vinculada a Carlos

## Cómo ejecutar?

1. Asegúrate de tener PostgreSQL activo y configurado correctamente
2. Instala las dependencias del backend
3. Activa tu entorno virtual (si usas uno)
4. Ejecuta el script desde la raíz del proyecto. Es decir: \DocuTrack\backend> python app/init_db.py


### Roles

 - Usuario estándar: Puede registrarse, iniciar sesión, elegir tipo de solicitud, adjuntar documento, enviar solicitud, hacer seguimiento, y descargar el certificado si fue aprobado.
   Credencial de usuario: Nombre: Carlos Díaz, correo: carlos.cliente@example.com,  contraseña: Cliente456$


 - Administrador: Puede visualizar todas las solicitudes, tratarlas, corregir, rechazar o aprobar.
   Credencial de administrador: Nombre": María Torres, Correo": maria.torres@example.com, Contraseña": Segura123$


## Mejoras por realizar:

Actualmente el sistema permite a los usuarios adjuntar documentos al enviar sus solicitudes, estos archivos son almacenados en la carpeta /cedulas/ y su ruta se registra en la base de datos bajo el campo archivo_path. Sin embargo, la visualización directa de los documentos desde el panel de administración aún no se encuentra habilitada ya que durante las pruebas de integración, se detectaron inconsistencias relacionadas con el mapeo del campo archivo_path en el esquema de salida. Por limitaciones técnicas y de tiempo durante la fase final de desarrollo, esta funcionalidad queda documentada como pendiente para futuras mejoras.


# Comentario personal
Este más allá de ser una prueba técnica, fue para mi una muestra de que las ganas de aprender y la curiosidad te pueden llevar a realizar cosas inimaginables. A nivel personal, toda esta experiencia servirá para recordarme que, a pesar de todas las dificultades, soy capaz de hacer esto y mucho más. 