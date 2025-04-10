from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select
from models import TransaccionDB, InversorDB, AccionDB
from main import engine
from datetime import datetime

transaccion_bp = Blueprint('transaccion', __name__)

@transaccion_bp.route("/transacciones", methods=["GET"])
def get_transacciones():
    session = Session(engine)
    
    inversor_id = request.args.get("inversor_id")
    accion_id = request.args.get("accion_id")

    query = select(TransaccionDB)

    if inversor_id:
        query = query.filter(TransaccionDB.inversor_id == inversor_id)

    if accion_id:
        query = query.filter(TransaccionDB.accion_id == accion_id)

    transacciones = session.exec(query).all()
    return jsonify([transaccion.model_dump() for transaccion in transacciones])

@transaccion_bp.route("/transacciones/<int:transaccion_id>", methods=["GET"])
def get_transaccion(transaccion_id: int):
    session = Session(engine)
    transaccion = session.get(TransaccionDB, transaccion_id)

    if transaccion is None:
        abort(404, description="Transaccion no encontrada")

    return jsonify(transaccion.model_dump())

@transaccion_bp.route("/transacciones", methods=["POST"])
def post_nueva_transaccion():
    session = Session(engine)
    data = request.get_json()

    if not all(key in data for key in ("inversor_id", "accion_id", "cantidad", "precio")):
        abort(400, description="Faltan campos obligatorios")

    nueva = TransaccionDB(inversor_id=data["inversor_id"], accion_id=data["accion_id"], cantidad=data["cantidad"], precio=data["precio"], fecha_hora=datetime.now(datetime.timezone.utc))

    session.add(post_nueva_transaccion)
    session.commit()
    session.refresh(nueva)
    
    return jsonify(nueva.model_dump()), 201

