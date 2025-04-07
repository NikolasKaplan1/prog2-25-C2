from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from transaccion import Transaccion

# Usamos una cadena para evitar problemas de import circular
class Inversor(SQLModel, table=True):
    """
    Modelo de datos para un inversor.
    
    Campos:
      - id: Identificador único autogenerado.
      - nombre: Nombre del inversor.
      - apellidos: Apellidos del inversor.
      - email: Correo electrónico único (indexado).
      - password: Contraseña hasheada.
      - tarjeta_credito: Número de tarjeta de crédito (almacenado de forma segura, idealmente enmascarado o tokenizado).
      - capital: Saldo de la cuenta (inicialmente 0 o el valor asignado).
      - transacciones: Relación con las transacciones realizadas.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    apellidos: str = Field(max_length=150)
    email: str = Field(max_length=255, unique=True, index=True)
    password: str = Field(max_length=255)
    tarjeta_credito: str = Field(max_length=20)
    capital: float = Field(default=0.0, ge=0)
    
    transacciones: List["Transaccion"] = Relationship(back_populates="inversor")
