from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select
from models import AccionDB  # Importar el modelo AccionDB
from main import engine  # Importar el engine desde main.py

accion_bp = Blueprint("accion", __name__)

@accion_bp.route("/acciones", methods=["GET"])
def get_acciones():
    session = Session(engine)
    acciones = session.exec(select(AccionDB)).all()
    return jsonify([accion.model_dump() for accion in acciones])

@accion_bp.route("/acciones/<int:accion_id>", methods=["GET"])
def get_accion_id(accion_id):
    session = Session(engine)
    accion = session.get(AccionDB, accion_id)
    if accion is None:
        abort(404, description="Accion no encontrada")
    return jsonify(accion.model_dump())

@accion_bp.route("/acciones", methods=["POST"])
def post_nueva_accion():
    data = request.get_json()
    if not all(key in data for key in ("simbolo", "nombre", "precio")):
        abort(400, description="Faltan campos obligatorios por completar")
    
    nuevo = AccionDB(simbolo=data["simbolo"], nombre=data["nombre"],precio=data["precio"] )
    
    session = Session(engine)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return jsonify(nuevo.model_dump()), 201


