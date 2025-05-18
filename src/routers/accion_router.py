"""
Módulo de rutas para la gestión de acciones en la API Flask.

Proporciona endpoints RESTful para consultar y gestionar acciones en la base de 
datos, utilizando SQLModel para el manejo de datos relacional y Flask Blueprint para 
la organización modular del código.

Dependencies
------------
- Flask
- SQLModel
- models (AccionDB)
"""

from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select
from models import AccionDB
import logging

# Creamos un logger para gestionar la información que devolvemos en este módulo
logger = logging.getLogger(__name__)

accion_bp = Blueprint("accion", __name__)

# Creamos una función para evitar la dependencia circular 
def get_engine():
    from app import engine
    return engine

@accion_bp.route("/", methods=["GET"])
def get_acciones():
    """
    Obtiene todas las acciones almacenadas en la base de datos

    Returns
    -------
    Response:
        Lista de objetos JSON que representan las acciones
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            acciones = session.exec(select(AccionDB)).all()
            return jsonify([accion.model_dump() for accion in acciones])
        except Exception as e:
            logger.error(f"Error al obtener acciones: {str(e)}")
            abort(500, description="Error al consultar la base de datos")


@accion_bp.route("/<int:accion_id>", methods=["GET"])
def get_accion_id(accion_id):
    """
    Obtiene una acción en concreto según su identificador

    Parameters
    ----------
    accion_id : int
        ID de la acción a consultar

    Returns
    -------
    Response:
        Objeto JSON que representa la acción solicitada

    Raises
    ------
    404 Not Found:
        Si no se encuentra una acción con el ID indicado
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            accion = session.get(AccionDB, accion_id)
            if accion is None:
                abort(404, description="Acción no encontrada")
            return jsonify(accion.model_dump())
        except Exception as e:
            logger.error(f"Error al obtener acción con ID {accion_id}: {str(e)}")
            abort(500, description="Error al consultar la base de datos")


@accion_bp.route("/", methods=["POST"])
def post_nueva_accion():
    """
    Almacena una nueva acción en la base de datos

    El cuerpo de la solicitud debe contener los siguientes campos:
    "nombre", "simbolo", "precio_actual", y "sector"

    Returns
    -------
    Tuple[Response, int]:
        Objeto JSON que representa la acción creada y código de estado 201

    Raises
    ------
    400 Bad Request:
        Si falta alguno de los campos requeridos en la solicitud
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            data = request.get_json()
            if not data:
                abort(400, description="No se han encontrado datos JSON")
                
            required_fields = ["nombre", "simbolo", "precio_actual", "sector"]
            for field in required_fields:
                if field not in data:
                    abort(400, description=f"Falta el campo obligatorio: {field}")
            
            nueva = AccionDB(
                nombre=data["nombre"], 
                simbolo=data["simbolo"], 
                precio_actual=data["precio_actual"], 
                sector=data["sector"]
            )
            
            session.add(nueva)
            session.commit()
            session.refresh(nueva)
            logger.info(f"Nueva acción creada con ID: {nueva.id}")
            return jsonify(nueva.model_dump()), 201
        except ValueError as ve:
            logger.warning(f"Error de validación al crear una nueva acción: {str(ve)}")
            abort(400, description=str(ve))

        except Exception as e:
            logger.error(f"Error al crear acción: {str(e)}")
            session.rollback()
            abort(500, description="Error al crear la acción")

@accion_bp.route("/<int:accion_id>", methods=["PUT"])
def update_accion(accion_id):
    """
    Corrige o actualiza los datos de una acción ya registrada

    Parameters
    ----------
    accion_id : int
        ID de la acción a actualizar

    Returns
    -------
    Response:
        Objeto JSON que representa la acción actualizada

    Raises
    ------
    404 Not Found:
        Si no se encuentra una acción con el ID indicado
    400 Bad Request:
        Si los datos proporcionados son inválidos
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            data = request.get_json()
            if not data:
                abort(400, description="No han encontrado datos JSON")
                
            accion = session.get(AccionDB, accion_id)
            if accion is None:
                abort(404, description="Acción no encontrada")
            
            # de esta forma actualizamos solo el campo que hayamos elegido
            for field in ["nombre", "simbolo", "precio_actual", "sector"]:
                if field in data:
                    setattr(accion, field, data[field])
            
            session.add(accion)
            session.commit()
            session.refresh(accion)
            logger.info(f"Acción con ID {accion_id} actualizada")
            return jsonify(accion.model_dump())
        except ValueError as ve:
            logger.warning(f"Error de validación al actualizar acción con ID {accion_id}: {str(ve)}")
            abort(400, description=str(ve))

        except Exception as e:
            logger.error(f"Error al actualizar acción con ID {accion_id}: {str(e)}")
            session.rollback()
            abort(500, description="Error al actualizar la acción")

@accion_bp.route("/<int:accion_id>", methods=["DELETE"])
def delete_accion(accion_id):
    """
    Elimina una acción

    Parameters
    ----------
    accion_id : int
        ID de la acción a eliminar

    Returns
    -------
    Response:
        Mensaje de confirmación de eliminación

    Raises
    ------
    404 Not Found:
        Si no se encuentra una acción con el ID indicado
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            accion = session.get(AccionDB, accion_id)
            if accion is None:
                abort(404, description="Acción no encontrada")
            
            session.delete(accion)
            session.commit()
            logger.info(f"Acción con ID {accion_id} eliminada")
            return jsonify({"message": f"Acción con ID {accion_id} eliminada correctamente"})
        
        except Exception as e:
            logger.error(f"Error al eliminar acción con ID {accion_id}: {str(e)}")
            session.rollback()
            abort(500, description="Error al eliminar la acción")