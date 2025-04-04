from typing import List
from fastapi import FastAPI, APIRouter, Depends, HTTPException

from sqlmodel import Session, select
import uvicorn
from pydantic import BaseModel



from database import get_session, create_db_and_tables, drop_db_and_tables, seed_users

from database import Inversor


app = FastAPI()
router = APIRouter()

class RespuestaInversor(BaseModel):
    id: int
    nombre: str
    email: str
    capital: float
    

class NuevoInversor(BaseModel):
    nombre: str
    email: str
    capital: float
    

@router.get("/inversores", response_model = List[RespuestaInversor])
def get_inversores(db: Session = Depends(get_session)):
    inversores = db.exect(select(Inversor)).all()
    return [{"id": inversor.id, "nombre": inversor.nombre, "email": inversor.email, "capital": inversor.capital} for inversor in inversores]

@router.get("/inversores/{inversor_id}", response_model = List[RespuestaInversor])

def get_inversor(db: Session= Depends(get_session)):
    inversor = db.get(Inversor, id)

    if inversor is None:
        raise HTTPException(status_code = 404, detail= "Inversor no encontrado")
    return {"id": inversor.id, "nombre": inversor.nombre, "email": inversor.email, "capital": inversor.capital}

@router.post("/inversores", response_model = RespuestaInversor, status_code= 201)
def nuevo_inversor(inversor: NuevoInversor, db: Session=Depends(get_session)):
    nuevo_inversor = Inversor(**inversor.model_dump())
    db.add(nuevo_inversor)
    db.commit()
    db.refresh(nuevo_inversor)
    return nuevo_inversor

 

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)