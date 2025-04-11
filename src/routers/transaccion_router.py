

"""
Módulo de rutas para la gestión de transacciones en la API Flask

Define endpoints RESTful para consultar y registrar transacciones de comprao venta 
de acciones por parte de los inversores

Utiliza SQLModel para la persistencia de datos y Flask Blueprint para la 
modularización de rutas

Dependencias
------------
- Flask
- SQLModel
- models (TransaccionDB)
- main (engine de conexión a la base de datos)
"""

from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select
from models import TransaccionDB
from main import engine
from datetime import datetime

transaccion_bp = Blueprint('transaccion', __name__)

@transaccion_bp.route("/transacciones", methods=["GET"])
def get_transacciones():
    """
    Obtener una lista de transacciones con filtros

    Parameters:
    -----------
    inversor_id: int 
        Filtra por ID del inversor
    accion_id: int
        Filtra por ID de la acción

    Returns
    -------
    Response:
        Lista de objetos JSON que representan las transacciones encontradas
    """
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
    """
    Obtener una transacción específica por su ID

    Parameters
    ----------
    transaccion_id : int
        ID de la transacción

    Returns
    -------
    Response:
        Objeto JSON con los detalles de la transacción

    Raises
    ------
    404 Not Found:
        Cuando no se encuentre la transacción
    """
    session = Session(engine)
    transaccion = session.get(TransaccionDB, transaccion_id)

    if transaccion is None:
        abort(404, description="Transaccion no encontrada")

    return jsonify(transaccion.model_dump())

@transaccion_bp.route("/transacciones", methods=["POST"])
def post_nueva_transaccion():
    """
    Registrar una nueva transacción de compra/venta.

    El cuerpo de la solicitud debe contener los campos:
    "inversor_id", "accion_id", "cantidad" y"precio".

    Returns
    -------
    Tuple[Response, int]:
        Objeto JSON de la transacción creada y código HTTP 201

    Raises
    ------
    400 Bad Request:
        Si faltan campos obligatorios en la solicitud
    """
    session = Session(engine)
    data = request.get_json()

    if not all(key in data for key in ("inversor_id", "accion_id", "cantidad", "precio")):
        abort(400, description="Faltan campos obligatorios")

    nueva = TransaccionDB(inversor_id=data["inversor_id"], accion_id=data["accion_id"], cantidad=data["cantidad"], precio=data["precio"], fecha_hora=datetime.now(datetime.timezone.utc))

    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    
    return jsonify(nueva.model_dump()), 201

