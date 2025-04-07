from typing import List
from fastapi import FastAPI, APIRouter, Depends, HTTPException

from sqlmodel import Session, select
import uvicorn
from pydantic import BaseModel


from database import get_session, create_db_and_tables, drop_db_and_tables, seed_users
from models import Inversor


app = FastAPI()
router = APIRouter()


class NuevaCompra(BaseModel):
    pass

#@router.post("/inversores/{inversor_id}/comprar")


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


