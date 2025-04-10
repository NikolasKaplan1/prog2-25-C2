from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select
from models import InversorDB  # Importar el modelo AccionDB
from main import engine  # Importar el engine desde main.py
from datetime import datetime

inversor_bp = Blueprint("inversor", __name__)

@inversor_bp.route("/inversores", methods=["GET"])
def get_inversor():
    session = Session(engine)
    inversores = session.exec(select(InversorDB)).all()
    return jsonify([inversor.model_dump() for inversor in inversores])

@inversor_bp.route("/inversores/<int:inversor_id>", methods=["GET"])
def get_inversor_id(inversor_id):
    session = Session(engine)
    inversor = session.get(InversorDB, inversor_id)
    if inversor is None:
        abort(404, description="Inversor no encontrado")
    return jsonify(inversor.model_dump())

@inversor_bp.route("/inversores", methods=["POST"])
def post_nuevo_inversor():
    session = Session(engine)
    data = request.get_json()
    if not all(key in data for key in ("nombre", "apellidos", "email", "contrasena", "tarjeta_credito", "capital")):
        abort(400, description= "Faltan campos obligatorios por completar")
    
    nuevo = InversorDB(nombre=data["nombre"], apellidos=data["apellidos"], email=data["email"], contrasena=data["contrasena"], tarjeta_credito=data["tarjeta_credito"], capital=data["capital"])
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return jsonify(nuevo.model_dump()), 201





