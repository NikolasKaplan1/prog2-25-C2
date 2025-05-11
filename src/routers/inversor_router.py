"""
Rutas para gestionar inversores en la API.

✔  Elimina dependencia de `main.engine`
✔  Usa la conexión centralizada de src.database.db_manager
✔  Ajusta los campos al nuevo esquema (password_hash, perfil, capital_inicial)
"""

from datetime import datetime
from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select

from src.database.db_manager import get_connection      # ← NUEVO
from src.models import InversorDB                       # adapta el import a tu paquete

inversor_bp = Blueprint("inversor", __name__)


# ---------------------------------------------------------------------------
@inversor_bp.route("/inversores", methods=["GET"])
def listar_inversores():
    """Devolver todos los inversores."""
    with get_connection() as conn:
        with Session(conn) as session:
            inversores = session.exec(select(InversorDB)).all()
            return jsonify([inv.model_dump() for inv in inversores])


# ---------------------------------------------------------------------------
@inversor_bp.route("/inversores/<int:inversor_id>", methods=["GET"])
def obtener_inversor(inversor_id: int):
    """Obtener un inversor por su ID."""
    with get_connection() as conn:
        with Session(conn) as session:
            inversor = session.get(InversorDB, inversor_id)
            if inversor is None:
                abort(404, "Inversor no encontrado")
            return jsonify(inversor.model_dump())


# ---------------------------------------------------------------------------
@inversor_bp.route("/inversores", methods=["POST"])
def crear_inversor():
    """
    Crear un nuevo inversor.

    Body JSON requerido:
    {
        "nombre": "Ana",
        "email": "ana@mail.com",
        "password_hash": "<hash bcrypt>",
        "perfil": "conservador" | "agresivo",
        "capital_inicial": 10000
    }
    """
    data = request.get_json(force=True)
    campos = ("nombre", "email", "password_hash", "perfil", "capital_inicial")
    if not all(k in data for k in campos):
        abort(400, f"Faltan campos obligatorios: {campos}")

    nuevo = InversorDB(
        nombre=data["nombre"],
        email=data["email"],
        password_hash=data["password_hash"],
        perfil=data["perfil"],
        capital_inicial=data["capital_inicial"],
        capital_disponible=data["capital_inicial"],       # comienza igual
        fecha_registro=datetime.utcnow(),                 # opcional: explícito
    )

    with get_connection() as conn:
        with Session(conn) as session:
            session.add(nuevo)
            session.commit()
            session.refresh(nuevo)
            return jsonify(nuevo.model_dump()), 201
