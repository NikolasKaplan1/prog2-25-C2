from sqlmodel import SQLModel, create_engine, Session
from datetime import datetime
from models import InversorDB, TransaccionDB, AccionDB  # Asegúrate de que la ruta es correcta.
from typing import Generator

# Configurar la conexión a MySQL
DATABASE_URL = "mysql+pymysql://user:password@localhost/finanzas"  # Cambia el nombre de la base de datos si es necesario

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

def get_session() -> Generator[Session, None, None]:
    """
    Obtiene una sesión para interactuar con la base de datos.
    
    Yield:
    ------
    Session: Una sesión activa de la base de datos para realizar consultas y transacciones.
    """
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

def create_db_and_tables():
    """
    Crea las tablas de la base de datos utilizando los modelos definidos en SQLModel.
    """
    SQLModel.metadata.create_all(engine)
    print("Base de datos y tablas creadas exitosamente.")

def drop_db_and_tables():
    """
    Elimina las tablas de la base de datos.
    """
    SQLModel.metadata.drop_all(engine)
    print("Base de datos y tablas eliminadas exitosamente.")

def seed_users():
    """
    Agrega usuarios iniciales (inversores) a la base de datos.
    """
    with next(get_session()) as session:
        inversores = [
            InversorDB(nombre="Alice", apellidos="Smith", email="alice@example.com", capital=100.0, tarjeta_credito="1234567890123456"),
            InversorDB(nombre="Bob", apellidos="Jones", email="bob@example.com", capital=100.0, tarjeta_credito="9876543210987654"),
            InversorDB(nombre="Charlie", apellidos="Brown", email="charlie@example.com", capital=100.0, tarjeta_credito="1122334455667788"),
        ]
        session.add_all(inversores)
        session.commit()
        print("Usuarios iniciales creados.")

def guardar_transaccion(transaccion):
    """
    Guarda una transacción en la base de datos.
    
    Parámetros:
    - transaccion: Instancia de la clase Transaccion a guardar en la base de datos.
    """
    with next(get_session()) as session:
        transaccion_db = TransaccionDB(
            inversor_id=transaccion.inversor.id,
            accion_id=transaccion.accion.id,
            cantidad=transaccion.cantidad,
            precio=transaccion.precio,
            fecha_hora=transaccion.fecha_hora
        )
        session.add(transaccion_db)
        session.commit()
        print("Transacción guardada exitosamente.")
