from sqlmodel import SQLModel, create_engine, Session
from datetime import datetime
from .models import InversorDB, TransaccionDB, AccionDB  # Asegúrate de tener estos modelos importados correctamente
from typing import List


# Configurar la conexión a MySQL
DATABASE_URL = "mysql+pymysql://user:password@localhost/finanzas"  # Cambia el nombre de la base de datos si es necesario

# Crear el motor de conexión
engine = create_engine(DATABASE_URL, echo=True)

# Función para obtener la sesión de base de datos
def get_session() -> Session:
    """
    Obtiene una sesión para interactuar con la base de datos.
    
    Returns:
    --------
    session: Session
        Una sesión activa de la base de datos para realizar consultas y transacciones.
    """
    session = Session(engine)
    return session


# Función para crear las tablas en la base de datos
def create_db_and_tables():
    """
    Crea las tablas de la base de datos utilizando los modelos definidos en SQLModel.
    """
    SQLModel.metadata.create_all(engine)
    print("Base de datos y tablas creadas exitosamente.")


# Función para eliminar las tablas de la base de datos
def drop_db_and_tables():
    """
    Elimina las tablas de la base de datos.
    """
    SQLModel.metadata.drop_all(engine)
    print("Base de datos y tablas eliminadas exitosamente.")


# Función seeder de usuarios (inversores)
def seed_users():
    """
    Agrega usuarios iniciales (inversores) a la base de datos.
    """
    with get_session() as session:
        inversores = [
            InversorDB(nombre="Alice", apellidos="Smith", email="alice@example.com", capital=100.0, tarjeta_credito="1234567890123456"),
            InversorDB(nombre="Bob", apellidos="Jones", email="bob@example.com", capital=100.0, tarjeta_credito="9876543210987654"),
            InversorDB(nombre="Charlie", apellidos="Brown", email="charlie@example.com", capital=100.0, tarjeta_credito="1122334455667788"),
        ]
        session.add_all(inversores)        
        session.commit()
        print("Usuarios iniciales creados.")


# Función para guardar transacciones
def guardar_transaccion(transaccion):
    """
    Guarda una transacción en la base de datos.
    
    Parámetros:
    - transaccion: Instancia de la clase Transaccion a guardar en la base de datos.
    """
    with get_session() as session:
        # Convertimos la transacción en un objeto TransaccionDB para almacenarlo en la base de datos
        transaccion_db = TransaccionDB(
            inversor_id=transaccion.inversor.id,  # ID del inversor
            accion_id=transaccion.accion.id,  # ID de la acción
            cantidad=transaccion.cantidad,
            precio=transaccion.precio,
            fecha_hora=transaccion.fecha_hora
        )
        session.add(transaccion_db)  # Añadimos la transacción
        session.commit()  # Guardamos los cambios
        print("Transacción guardada exitosamente.")
