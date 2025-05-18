from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime


class InversorDB(SQLModel, table=True):
    """
    Este modelo representa a un inversor en el sistema

    Attributes
    ----------
    id : int
        Identificador único para cada inversor
    nombre : str
        Nombre del inversor
    apellidos : str
        Apellidos del inversor
    email : str
        Direccioón de correo electrónico del inversor
    contrasena : str
        Contraseña del inversor
    tarjeta_credito : str
        Número de la tarjeta de crédito del inversor
    capital : float
        Capital disponible que tiene el inversor para invertir
    transacciones : List[TransaccionDB]
        Listado de transacciones realizadas por el inversor
    """
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
    """
    Modelo que representa una acción realizada en el sistema

    Esta clase define los atributos principales de una acción que puede ser objegto de 
    inversión, así como la relación entre las transacciones asociadas

    Attributes
    ----------
    id : int
        Indentificador único de la acción y clave primaria
    simbolo : str
        Símbolo de la acción (como puede ser "TSLA")
    nombre : str
        Nombre de la empresa o del título de la acción
    precio_actual : floar
        Precio actual de la acción en el mercado
    historial_precios : str
        Historial de precios de la acción
    transacciones : List[TransaccionesDB]
        Listado con las transacciones en las que se ha visto involucrada esta acción
    """

    __tablename__ = "acciones"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    simbolo: str
    nombre: str
    precio_actual: float
    historial_precios: Optional[str]  

    # Relación con TransaccionDB (uno a muchos)
    transacciones: List["TransaccionDB"] = Relationship(back_populates="accion")


class TransaccionDB(SQLModel, table=True):
    """
    Modelo que representa la transacción realizada por un inversor sobre una acción

    Esta clase almacena la información relacionada con las operaciones de compra/venta de acciones, 
    incluyendo la cantidad, el precio, fecha y relaciones con el inversor

    Attributes
    ----------
    id : int
        Identificador único para cada transacción
    inversor_id : int
        Identificador del inversor que realiza dicha transacción, es la clave ajena
    accion_id : int
        Identificador de la acción involucrada en la transacción, es la clave ajena
    cantidad : int
        Número de acciones compradas o vendidas
    precio : float
        Precio de cada acción en el momento en el que se realiza la transacción
    fecha_hora : datetime
        Fceha y hora a la que se realiza la transacción
    """
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
