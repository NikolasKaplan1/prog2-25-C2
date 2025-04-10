from sqlmodel import SQLModel, Field
from typing import List
from datetime import datetime

class InversorDB(SQLModel, table=True):
    __tablename__ = "inversores"  # Nombre de la tabla en la base de datos

    id: int = Field(default=None, primary_key=True)  # El ID único del inversor
    nombre: str
    apellidos: str
    email: str
    contrasena: str
    tarjeta_credito: str
    capital: float

    # Relación con las transacciones
    transacciones: List["TransaccionDB"] = []


class AccionDB(SQLModel, table=True):
    __tablename__ = "acciones"  # Nombre de la tabla para las acciones

    id: int = Field(default=None, primary_key=True)  # ID único de la acción
    simbolo: str
    nombre: str
    precio_actual: float
    historial_precios: dict[str, float]  # Este campo puede necesitar una conversión para almacenarse correctamente en la base de datos


class TransaccionDB(SQLModel, table=True):
    __tablename__ = "transacciones"  # Nombre de la tabla para las transacciones

    id: int = Field(default=None, primary_key=True)  # ID único de la transacción
    inversor_id: int = Field(foreign_key="inversores.id")  # Relación con el inversor
    accion_id: int = Field(foreign_key="acciones.id")  # Relación con la acción
    cantidad: int
    precio: float
    fecha_hora: datetime = Field(default=datetime.utcnow())  # Fecha y hora de la transacción

    # Relación con los inversores y las acciones
    inversor: InversorDB  # Relación con Inversor
    accion: AccionDB  # Relación con Accion
