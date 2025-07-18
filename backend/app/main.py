from fastapi import FastAPI
from app.database.database import engine
from app.models import user

app = FastAPI()

user.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"mensaje": "¡FastAPI corriendo desde backend!"}
