from fastapi import FastAPI
from app.database.database import engine
from app.models import user  # importa el modelo para que SQLAlchemy lo registre

app = FastAPI()

# Crear las tablas en la base de datos
user.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola Eimy, FastAPI está corriendo con PostgreSQL!"}
