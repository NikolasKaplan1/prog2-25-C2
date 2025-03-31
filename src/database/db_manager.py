import os
from sqlmodel import SQLModel, create_engine, Session

# Obtén la URL de la base de datos desde una variable de entorno, o usa SQLite por defecto.
DATABASE_URL = "sqlite:///./database.db"

# Crea el engine para conectar con la base de datos.
engine = create_engine(DATABASE_URL, echo=True)


from src.models.inversor import Inversor
from src.models.accion import Accion
from src.models.transaccion import Transaccion

def create_db_and_tables():
    """
    Crea todas las tablas definidas en los modelos.
    Se llama al arrancar la aplicación para asegurar que la BD esté lista.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Proporciona una sesión de base de datos.
    Se utiliza como dependencia para interactuar con la BD en endpoints y otros scripts.
    """
    with Session(engine) as session:
        yield session
