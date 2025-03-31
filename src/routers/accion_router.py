from typing import List
from fastapi import FastAPI, APIRouter, Depends, HTTPException

from sqlmodel import Session, select
import uvicorn
from pydantic import BaseModel


from db import get_session, create_db_and_tables, drop_db_and_tables, seed_users
from models import Accion

app = FastAPI()
router = APIRouter()


class RespuestaAcciones(BaseModel):
    id: int
    simbolo: str
    nombre: str
    precio: float


@router.get("/acciones", response_model = List(RespuestaAcciones))
def get_acciones(db: Session = Depends(get_session)):
    acciones = db.exect(select(Accion)).all()
    return [{"id": accion.id, "simbolo": accion.simbolo, "nombre": accion.nombre, "precio": accion.precio} for accion in acciones]

@router.get("/acciones/{accion_id}")
def get_accion(db: Session = Depends(get_session)):
    pass

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

