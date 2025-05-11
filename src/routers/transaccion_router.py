"""
Rutas REST para transacciones (compra / venta).

• Usa la conexión centralizada con SQLite (get_connection)
• Refleja el nuevo esquema: usuario_id, simbolo, tipo, cantidad, precio_unitario
"""

from datetime import datetime, timezone
from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select

from src.database.db_manager import get_connection
from src.models import TransaccionDB

transaccion_bp = Blueprint("transaccion", __name__)


# ---------------------------------------------------------------------------
@transaccion_bp.route("/transacciones", methods=["GET"])
def listar_transacciones():
    """
    Filtros por ?usuario_id=…&simbolo=…
    """
    usuario_id = request.args.get("usuario_id")
    simbolo    = request.args.get("simbolo")

    with get_connection() as conn:
        with Session(conn) as session:
            query = select(TransaccionDB)

            if usuario_id:
                query = query.where(TransaccionDB.usuario_id == int(usuario_id))
            if simbolo:
                query = query.where(TransaccionDB.simbolo == simbolo.upper())

            transacciones = session.exec(query).all()
            return jsonify([t.model_dump() for t in transacciones])


# ---------------------------------------------------------------------------
@transaccion_bp.route("/transacciones/<int:transaccion_id>", methods=["GET"])
def obtener_transaccion(transaccion_id: int):
    """Obtener una transacción por ID."""
    with get_connection() as conn:
        with Session(conn) as session:
            trans = session.get(TransaccionDB, transaccion_id)
            if trans is None:
                abort(404, "Transacción no encontrada")
            return jsonify(trans.model_dump())


# ---------------------------------------------------------------------------
@transaccion_bp.route("/transacciones", methods=["POST"])
def crear_transaccion():
    """
    Body JSON requerido:
    {
        "usuario_id": 1,
        "simbolo": "AAPL",
        "tipo": "compra" | "venta",
        "cantidad": 3,
        "precio_unitario": 178.5
    }
    """
    data = request.get_json(force=True)
    campos = ("usuario_id", "simbolo", "tipo", "cantidad", "precio_unitario")
    if not all(k in data for k in campos):
        abort(400, f"Faltan campos obligatorios: {campos}")

    if data["tipo"] not in ("compra", "venta"):
        abort(400, "Tipo debe ser 'compra' o 'venta'")

    nueva = TransaccionDB(
        usuario_id     = data["usuario_id"],
        simbolo        = data["simbolo"].upper(),
        tipo           = data["tipo"],
        cantidad       = data["cantidad"],
        precio_unitario= data["precio_unitario"],
        fecha          = datetime.now(timezone.utc),
    )

    with get_connection() as conn:
        with Session(conn) as session:
            session.add(nueva)
            session.commit()
            session.refresh(nueva)
            return jsonify(nueva.model_dump()), 201
