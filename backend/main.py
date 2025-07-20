from fastapi import FastAPI
from app.database.database import engine
from app.models import models
from app.schemas import UserCreate
from app.routers import users
from app.routers import requestes

app = FastAPI()

app.include_router(users.router, prefix="", tags=["Usuarios"])

app.include_router(requestes.router)

models.Base.metadata.create_all(bind=engine)

