

"""
Módulo de rutas para la gestión de acciones en la API Flask

Este módulo define endpoints RESTful para hacer operaciones sobre
acciones ccomo obtener la lista completa de acciones, consultar una acción por ID 
y registrar una nueva acción

Utiliza SQLModel para la interacción con la base de datos, y Flask Blueprint para 
modularizar las rutas

Dependencias
------------
- Flask
- SQLModel
- models (AccionDB)
- main (engine de conexión a base de datos)
"""

from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select
from models import AccionDB  
from main import engine  

accion_bp = Blueprint("accion", __name__)

@accion_bp.route("/acciones", methods=["GET"])
def get_acciones():
    """
    Obtener todas las acciones registradas en la base de datos

    Returns
    -------
    Response:
        Una lista de objetos JSON que representan las acciones
    """
    session = Session(engine)
    acciones = session.exec(select(AccionDB)).all()
    return jsonify([accion.model_dump() for accion in acciones])

@accion_bp.route("/acciones/<int:accion_id>", methods=["GET"])
def get_accion_id(accion_id):
    """
    Obtener una acción específica por su identificador único

    Parameters
    ----------
    accion_id : int
        ID de la acción a buscar

    Returns
    -------
    Response:
        Objeto JSON que representa la acción solicitada

    Raises
    ------
    404 Not Found:
        Cuando no se encuentra una acción con el ID proporcionado
    """
    session = Session(engine)
    accion = session.get(AccionDB, accion_id)
    if accion is None:
        abort(404, description="Accion no encontrada")
    return jsonify(accion.model_dump())

@accion_bp.route("/acciones", methods=["POST"])
def post_nueva_accion():
    """
    Crear una nueva acción y guardarla en la base de datos

    El cuerpo de la solicitud debe ser un JSON que contenga los campos:
    "simbolo", "nombre" y "precio_actual"

    Returns
    -------
    Tuple[Response, int]:
        El objeto JSON que representa la acción creada y el código de estado 201

    Raises
    ------
    400 Bad Request:
        Si faltan campos obligatorios en el body de la solicitud
    """
    data = request.get_json()
    if not all(key in data for key in ("simbolo", "nombre", "precio_actual")):
        abort(400, description="Faltan campos obligatorios por completar")
    
    nuevo = AccionDB(simbolo=data["simbolo"], nombre=data["nombre"],precio=data["precio_actual"] )
    
    session = Session(engine)
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return jsonify(nuevo.model_dump()), 201


