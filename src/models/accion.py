from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Accion(SQLModel, table=True):
    """
    Modelo de datos para una acción.
    
    Campos:
      - id: Identificador único autogenerado.
      - simbolo: Código o símbolo de la acción (único).
      - nombre: Nombre de la empresa o acción.
      - precio_actual: Precio vigente de la acción.
      - transacciones: Relación con las transacciones donde se ha usado esta acción.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    simbolo: str = Field(max_length=10, unique=True, index=True)
    nombre: str = Field(max_length=100)
    precio_actual: float
    
    transacciones: List["Transaccion"] = Relationship(back_populates="accion")
