from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Inversor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    nombre: str = Field(max_length=100)
    email: str = Field(max_length=255)
    capital: float = Field(max_length=255)