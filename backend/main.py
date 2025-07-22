from fastapi import FastAPI
from app.database.database import engine
from app.models import models
from app.schemas import UserCreate
from app.routers import users
from app.routers import requestes
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(users.router, prefix="", tags=["Usuarios"])

app.include_router(requestes.router)

app.mount("/cedulas", StaticFiles(directory="cedulas"), name="cedulas")

models.Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # o ["*"] para permitir todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)