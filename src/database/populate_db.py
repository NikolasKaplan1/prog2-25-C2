from sqlmodel import Session
from database.db_manager import engine
from models.inversor import Inversor

def insertar_inversores():
    inversores = [
        Inversor(nombre="Alice", email="alice@example.com", capital=100.0),
        Inversor(nombre="Bob", email="bob@example.com", capital=100.0),
        Inversor(nombre="Charlie", email="charlie@example.com", capital=100.0),
    ]

    with Session(engine) as session:
        session.add_all(inversores)
        session.commit()
        print("Inversores añadidos correctamente.")

if __name__ == "__main__":
    insertar_inversores()
