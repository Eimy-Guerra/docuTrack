from fastapi import FastAPI
from app.database.database import engine
from app.models import models
from app.schemas import UserCreate

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"mensaje": "¡FastAPI corriendo desde backend!"}



@app.get("/test-schema")
def test_schema():
    user = UserCreate(name="Eimy", email="eimy@example.com", password="123456")
    return user
