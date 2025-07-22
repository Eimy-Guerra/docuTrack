from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from passlib.context import CryptContext
from app.models.models import User           
from app.database.database import Base


DATABASE_URL = "postgresql://postgres:test223@localhost:5432/docutrack_db" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Verifica si los usuarios ya existen
    if db.query(User).filter(User.correo == "carlos.cliente@example.com").first():
        print("⚠️ Los datos ya fueron inicializados.")
        return

    # Crear usuarios
    carlos = User(
        nombre="Carlos Diaz",
        correo="carlos.cliente@example.com",
        contraseña=pwd_context.hash("Cliente456$"),
        rol="USER"
    )

    maria = User(
        nombre="Maria Torres",
        correo="maria.torres@example.com",
        contraseña=pwd_context.hash("Segura123$"),
        rol="ADMIN"
    )

    db.add_all([carlos, maria])
    db.commit()
    db.close()
    print("✅ Usuarios de prueba creados correctamente.")

if __name__ == "__main__":
    init()
