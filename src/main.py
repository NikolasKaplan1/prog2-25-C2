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

