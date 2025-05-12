
"""
Módulo de rutas para la gestión de inversores en la API Flask.

Proporciona endpoints RESTful para consultar y registrar inversores en la base de 
datos, utiliza SQLModel para el manejo de datos relacional y Flask Blueprint para 
la organización modular del código

Dependencies
------------
- Flask
- SQLModel
- models (InversorDB)
- main (engine de conexión a la base de datos)
"""

from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select
from models import InversorDB  
from main import engine  
from datetime import datetime

inversor_bp = Blueprint("inversor", __name__)

@inversor_bp.route("/inversores", methods=["GET"])
def get_inversor():
    """
    Obtener todos los inversores registrados en la base de datos

    Returns
    -------
    Response:
        Lista de objetos JSON que representan los inversores
    """
    session = Session(engine)
    inversores = session.exec(select(InversorDB)).all()
    return jsonify([inversor.model_dump() for inversor in inversores])

@inversor_bp.route("/inversores/<int:inversor_id>", methods=["GET"])
def get_inversor_id(inversor_id):
    """
    Obtener un inversor específico por su identificador

    Parameters
    ----------
    inversor_id : int
        ID del inversor a consultar

    Returns
    -------
    Response:
        Objeto JSON que representa el inversor solicitado

    Raises
    ------
    404 Not Found:
        Si no se encuentra un inversor con el ID indicado
    """
    session = Session(engine)
    inversor = session.get(InversorDB, inversor_id)
    if inversor is None:
        abort(404, description="Inversor no encontrado")
    return jsonify(inversor.model_dump())

@inversor_bp.route("/inversores", methods=["POST"])
def post_nuevo_inversor():
    """
    Registrar un nuevo inversor en la base de datos

    El cuerpo de la solicitud debe contener los siguientes campos:
    "nombre", "apellidos", "email", "contrasena", "tarjeta_credito" y "capital"

    Returns
    -------
    Tuple[Response, int]:
        Objeto JSON que representa al inversor creado y código de estado 201

    Raises
    ------
    400 Bad Request:
        Si falta alguno de los campos requeridos en la solicitud
    """
    session = Session(engine)
    data = request.get_json()
    if not all(key in data for key in ("nombre", "apellidos", "email", "contrasena", "tarjeta_credito", "capital")):
        abort(400, description= "Faltan campos obligatorios por completar")
    
    nuevo = InversorDB(nombre=data["nombre"], apellidos=data["apellidos"], email=data["email"], contrasena=data["contrasena"], tarjeta_credito=data["tarjeta_credito"], capital=data["capital"])
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return jsonify(nuevo.model_dump()), 201