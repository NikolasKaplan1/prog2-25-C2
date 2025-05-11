"""
Módulo de rutas para la gestión de acciones en la API Flask.

• Usa src.database.db_manager.get_connection() para abrir la BD.
• Mantiene SQLModel (AccionDB) pero envuelve la conexión cruda en Session(conn).
"""

from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select
from src.database.db_manager import get_connection   # ➊ NUEVO import
from src.models import AccionDB                      # supongo que tus modelos viven en src/models

accion_bp = Blueprint("accion", __name__)

# -------------------------------------------------------------------
@accion_bp.route("/acciones", methods=["GET"])
def get_acciones():
    """Devolver todas las acciones."""
    with get_connection() as conn:                   # ➋ abre conexión
        with Session(conn) as session:
            acciones = session.exec(select(AccionDB)).all()
            return jsonify([a.model_dump() for a in acciones])

# -------------------------------------------------------------------
@accion_bp.route("/acciones/<int:accion_id>", methods=["GET"])
def get_accion_id(accion_id: int):
    """Obtener una acción por ID."""
    with get_connection() as conn:
        with Session(conn) as session:
            accion = session.get(AccionDB, accion_id)
            if accion is None:
                abort(404, "Acción no encontrada")
            return jsonify(accion.model_dump())

# -------------------------------------------------------------------
@accion_bp.route("/acciones", methods=["POST"])
def post_nueva_accion():
    """
    Crear una nueva acción.
    Body JSON: { simbolo, nombre, precio_actual }
    """
    data = request.get_json(force=True)
    if not all(k in data for k in ("simbolo", "nombre", "precio_actual")):
        abort(400, "Faltan campos obligatorios (simbolo, nombre, precio_actual)")

    nueva = AccionDB(
        simbolo=data["simbolo"],
        nombre=data["nombre"],
        precio_actual=data["precio_actual"]          # ➌ nombre de campo correcto
    )

    with get_connection() as conn:
        with Session(conn) as session:
            session.add(nueva)
            session.commit()
            session.refresh(nueva)
            return jsonify(nueva.model_dump()), 201
