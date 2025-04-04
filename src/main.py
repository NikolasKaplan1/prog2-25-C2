from fastapi import FastAPI
from src.database.db_manager import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # Crea todas las tablas definidas en tus modelos si no existen.
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Simulador de Bolsa activo y base de datos inicializada"}

import os
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn

from database import create_db_and_tables, drop_db_and_tables, seed_users


from routers.inversor_router import router as inversor_router
#from routers.accion_router import router as accion_router



# Create logs folder if it doesn't exist
os.makedirs('logs', exist_ok=True)

logging.basicConfig(level=logging.INFO, filename='logs/acciones.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Creating db tables")
    drop_db_and_tables()
    create_db_and_tables()
    logging.info("Seeding inversors")
    seed_users()
    logging.info("Application started")
    yield
    logging.info("Application shutdown")


app = FastAPI(lifespan=lifespan)


# Registramos los routers
app.include_router(inversor_router)
#app.include_router(accion_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

