from typing import List
from fastapi import FastAPI, APIRouter, Depends, HTTPException

from sqlmodel import Session, select
import uvicorn
from pydantic import BaseModel



from database import get_session, create_db_and_tables, drop_db_and_tables, seed_users

from models import Accion

app = FastAPI()
router = APIRouter()


class RespuestaAcciones(BaseModel):
    id: int
    simbolo: str
    nombre: str
    precio: float


class NuevaAccion(BaseModel):
    simbolo: str
    nombre: str
    precio: float


@router.get("/acciones", response_model = List(RespuestaAcciones))
def get_acciones(db: Session = Depends(get_session)):
    acciones = db.exect(select(Accion)).all()
    return [{"id": accion.id, "simbolo": accion.simbolo, "nombre": accion.nombre, "precio": accion.precio} for accion in acciones]

@router.get("/acciones/{accion_id}", response_model = List(RespuestaAcciones))
def get_accion(db: Session = Depends(get_session)):
    accion = db.get(Accion, id)

    if accion is None:
        raise HTTPException(status_code = 404, detail= "Accion no encontrada")
    return {"id": accion.id, "simbolo": accion.username, "nombre": accion.nombre, "precio": accion.precio}


@router.post("/acciones", response_model = RespuestaAcciones, status_code = 201)
def nueva_accion(accion: NuevaAccion, db: Session = Depends(get_session)):
    nueva_accion = Accion(**accion.model_dump())
    db.add(nueva_accion)
    db.commit()
    db.refresh(nueva_accion)
    return nueva_accion
    

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

