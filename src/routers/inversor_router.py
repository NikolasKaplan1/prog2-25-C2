"""
Módulo de rutas para la gestión de inversores en la API Flask

Proporciona endpoints RESTful para consultar y registrar inversores en la base de 
datos, utiliza SQLModel para el manejo de datos relacional y Flask Blueprint para 
la organización modular del código

Dependencies
------------
- Flask
- SQLModel
- models (InversorDB)
"""
from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select
from models import InversorDB
import logging                      

# Creamos un logger para este módulo
logger = logging.getLogger(__name__)

inversor_bp = Blueprint("inversor", __name__)

# Evitamos dependencias circulares al importar engine donde es necesario
def get_engine():
    from main import engine
    return engine

@inversor_bp.route("/", methods=["GET"])
def get_inversores():
    """
    Obtenemos todos los inversores registrados en la base de datos

    Returns
    -------
    Response:
        Lista de objetos JSON que representan los inversores
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            inversores = session.exec(select(InversorDB)).all()
            return jsonify([inversor.model_dump() for inversor in inversores])
        except Exception as e:
            logger.error(f"Error al obtener inversores: {str(e)}")
            abort(500, description="Error al consultar la base de datos")



@inversor_bp.route("//<int:inversor_id>", methods=["GET"])
def get_inversor_id(inversor_id):
    """
    Obtiene un inversor específico por su identificador

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
        Si el inversor con el ID indicado no es encotrado
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            inversor = session.get(InversorDB, inversor_id)
            if inversor is None:
                abort(404, description="Inversor no encontrado")
            return jsonify(inversor.model_dump())
        except Exception as e:
            logger.error(f"Error al obtener inversor {inversor_id}: {str(e)}")
            abort(500, description="Error al consultar la base de datos")


@inversor_bp.route("/", methods=["POST"])
def post_nuevo_inversor():
    """
    Registra un nuevo inversor en la base de datos

    El cuerpo de la solicitud debe contener los siguientes campos:
    "nombre", "apellidos", "email", "contrasena", "tarjeta_credito" y "capital"

    Returns
    -------
    Tuple[Response, int]:
        Objeto JSON que representa al inversor creado y código de estado 201

    Raises
    ------
    400 Bad Request:
        Si falta alguno de los campos necesarios para la solicitud
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            data = request.get_json()
            if not data:
                abort(400, description="No se han encontrado datos JSON")
                
            required_fields = ["nombre", "apellidos", "email", "contrasena", "tarjeta_credito", "capital"]
            for field in required_fields:
                if field not in data:
                    abort(400, description=f"Falta el campo obligatorio: {field}")
            
            nuevo = InversorDB(
                nombre=data["nombre"], 
                apellidos=data["apellidos"], 
                email=data["email"], 
                contrasena=data["contrasena"], 
                tarjeta_credito=data["tarjeta_credito"], 
                capital=data["capital"]
            )
            
            session.add(nuevo)
            session.commit()
            session.refresh(nuevo)
            logger.info(f"Nuevo inversor creado con ID: {nuevo.id}")
            return jsonify(nuevo.model_dump()), 201
        except ValueError as e:
            logger.warning(f"Error de validación al crear inversor: {str(e)}")
            abort(400, description=str(e))
        except Exception as e:
            logger.error(f"Error al crear inversor: {str(e)}")
            session.rollback()
            abort(500, description="Error al crear el inversor")


@inversor_bp.route("/<int:inversor_id", methods=["PUT"])
def update_inversor(inversor_id):
    """
    Corrige o modifica los datos de un inversor existente

    Parameters
    ----------
    inversor_id : int
        ID del inversor a actualizar

    Returns
    -------
    Response:
        Objeto JSON que representa el inversor actualizado

    Raises
    ------
    404 Not Found:
        Si no se encuentra un inversor con el ID indicado
    400 Bad Request:
        Si los datos proporcionados son inválidos
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            data = request.get_json()
            if not data:
                abort(404, description="No se han encontrado datos JSON")

            inversor = session.get(InversorDB, inversor_id)
            if inversor is None:
                abort(404, description="Inversor no encotrado")

            for field in ["nombre", "apellidos", "email",  "contrasena", "tarjeta_credito", "capital"]:
                if field in data:
                    setattr(inversor, field, data[field])

            session.add(inversor)
            session.commit()
            session.refresh(inversor)
            logger.info(f"Inversor con el ID {inversor_id} actualizado correctamente")
            return jsonify(inversor.model_dump())
        
        except ValueError as ve:
            logger.warning(f"Error de validación al actualizar el inversor con ID {inversor_id}: {str(ve)}")
            abort(404, desciption=str(ve))

        except Exception as e:
            logger.error(f"Error al actualizar inversor con ID {inversor_id}: {str(e)}")
            session.rollback()
            abort(500, description="Error al actualizar el inversor")


@inversor_bp.route("/<int:inversor_id>", methods=["DELETE"])
def delete_inversor(inversor_id):
    """
    Eliminana un inversor existente

    Parameters
    ----------
    inversor_id : int
        ID del inversor a eliminar

    Returns
    -------
    Response:
        Mensaje de confirmación de eliminación

    Raises
    ------
    404 Not Found:
        Si no se encuentra un inversor con el ID indicado
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            inversor = session.get(InversorDB, inversor_id)
            if inversor is None:
                abort(404, description="Inversor no encontrado")
            
            session.delete(inversor)
            session.commit()
            logger.info(f"Inversor con ID {inversor_id} eliminado")
            return jsonify({"message": f"Inversor con ID {inversor_id} eliminado correctamente"})
        except Exception as e:
            logger.error(f"Error al eliminar inversor con ID {inversor_id}: {str(e)}")
            session.rollback()
            abort(500, description="Error al eliminar el inversor")