from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from inversor import Inversor
from accion import Accion

class Transaccion(SQLModel, table=True):
    """
    Modelo de datos para registrar una transacción.
    
    Campos:
      - id: Identificador único autogenerado.
      - cantidad: Número de acciones involucradas en la operación.
      - precio: Precio de la acción en el momento de la transacción.
      - timestamp: Fecha y hora en que se realizó la transacción.
      - inversor_id: Clave foránea que enlaza con el Inversor.
      - accion_id: Clave foránea que enlaza con la Accion.
      - inversor: Relación inversa para acceder al inversor.
      - accion: Relación inversa para acceder a la acción.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    cantidad: float
    precio: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    inversor_id: int = Field(foreign_key="inversor.id")
    accion_id: int = Field(foreign_key="accion.id")
    
    inversor: Optional["Inversor"] = Relationship(back_populates="transacciones")
    accion: Optional["Accion"] = Relationship(back_populates="transacciones")
