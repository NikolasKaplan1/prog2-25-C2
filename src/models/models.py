from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime


class InversorDB(SQLModel, table=True):
    __tablename__ = "inversores"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    apellidos: str
    email: str
    contrasena: str
    tarjeta_credito: str
    capital: float

    # Relación con TransaccionDB (uno a muchos)
    transacciones: List["TransaccionDB"] = Relationship(back_populates="inversor")


class AccionDB(SQLModel, table=True):
    __tablename__ = "acciones"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    simbolo: str
    nombre: str
    precio_actual: float
    historial_precios: Optional[str]  # Puedes serializar el dict a JSON si quieres

    # Relación con TransaccionDB (uno a muchos)
    transacciones: List["TransaccionDB"] = Relationship(back_populates="accion")


class TransaccionDB(SQLModel, table=True):
    __tablename__ = "transacciones"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    inversor_id: int = Field(foreign_key="inversores.id")
    accion_id: int = Field(foreign_key="acciones.id")
    cantidad: int
    precio: float
    fecha_hora: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones inversas
    inversor: Optional[InversorDB] = Relationship(back_populates="transacciones")
    accion: Optional[AccionDB] = Relationship(back_populates="transacciones")
