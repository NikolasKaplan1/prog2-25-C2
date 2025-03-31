from typing import List
from fastapi import FastAPI, APIRouter, Depends, HTTPException

from sqlmodel import Session, select
import uvicorn
from pydantic import BaseModel


from db import get_session, create_db_and_tables, drop_db_and_tables, seed_users
from models import Inversor


app = FastAPI()
router = APIRouter()

class RespuestaInversores(BaseModel):
    id: int
    nombre: str
    capital: float

class RespuestaInversorId(BaseModel):
    id: int
    nombre: str
    capital: float
    email: str

class NuevoInversor(BaseModel):
    nombre: str
    capital: float
    email: str

@router.get("/inversores", response_model = List[RespuestaInversores])
def get_inversores(db: Session = Depends(get_session)):
    inversores = db.exect(select(Inversor)).all()
    return [{"id": inversor.id, "nombre": inversor.nombre, "capital": inversor.capital} for inversor in inversores]

@router.get("/inversores/{inversor_id}", response_model = List[RespuestaInversorId])
def get_inversor(db: Session= Depends(get_session)):
    inversor = db.get(Inversor, id)

    if inversor is None:
        raise HTTPException(status_code = 404, detail= "User not found")
    return {"id": inversor.id, "nombre": inversor.username, "email": inversor.email, "capital": inversor.capital}

@router.post("/inversores", response_model = RespuestaInversorId, status_code= 201)
def nuevo_inversor(inversor: NuevoInversor, db: Session=Depends[get_session]):
    nuevo_inversor = Inversor(**inversor.model_dump())
    db.add(nuevo_inversor)
    db.commit()
    db.refresh(nuevo_inversor)
    return nuevo_inversor

 

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)