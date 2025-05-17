
"""
Módulo de rutas para la gestión de transacciones en la API Flask

Proporciona endpoints RESTful para consultar y registrar transacciones de compra/venta
de acciones por parte de inversores en la base de datos, utilizando SQLModel para el 
manejo de datos relacional y Flask Blueprint para la organización modular del código

Dependencies
------------
- Flask
- SQLModel
- models (TransaccionDB, InversorDB, AccionDB)
"""

from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select
from models import TransaccionDB, InversorDB, AccionDB
from datetime import datetime
import logging

# Creamos un logger para este módulo
logger = logging.getLogger(__name__)

transaccion_bp = Blueprint('transaccion', __name__)

# creamos una función para importar engine desde main
def get_engine():
    from main import engine
    return engine


@transaccion_bp.route("/", methods=["GET"])
def get_transacciones():
    """
    Obtiene todas las transacciones almacenadas en la base de datos

    Returns
    -------
    Response:
        Lista de objetos JSON que representan las transacciones
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            transacciones = session.exec(select(TransaccionDB)).all()
            return jsonify([transaccion.model_dump() for transaccion in transacciones])
        
        except Exception as e:
            logger.error(f"Error al obtener transacciones: {str(e)}")
            abort(500, description="Error al consultar la base de datos")


@transaccion_bp.route("/<int:transaccion_id>", methods=["GET"])
def get_transaccion_id(transaccion_id):
    """
    Obtiene una transacción en concreto que viene dada por su identificador

    Parameters
    ----------
    transaccion_id : int
        ID de la transacción a consultar

    Returns
    -------
    Response:
        Objeto JSON que representa la transacción solicitada

    Raises
    ------
    404 Not Found:
        Si no se encuentra una transacción con el ID indicado
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            transaccion = session.get(TransaccionDB, transaccion_id)
            if transaccion is None:
                abort(404, description="Transacción no encontrada")
            return jsonify(transaccion.model_dump())
        
        except Exception as e:
            logger.error(f"Error al obtener transacción con ID {transaccion_id}: {str(e)}")
            abort(500, description="Error al consultar la base de datos")


@transaccion_bp.route("/inversor/<int:inversor_id>", methods=["GET"])
def get_transacciones_inversor(inversor_id):
    """
    Obtiene todas las transacciones que ha realizado un inversor a través de su ID

    Parameters
    ----------
    inversor_id : int
        ID del inversor cuyas transacciones se quieren consultar

    Returns
    -------
    Response:
        Lista de objetos JSON que representan las transacciones del inversor

    Raises
    ------
    404 Not Found:
        Si no se encuentra un inversor con el ID indicado
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            # Verificamos si el inversor existe en la base de datos
            inversor = session.get(InversorDB, inversor_id)
            if inversor is None:
                abort(404, description="Inversor no encontrado")
                
            transacciones = session.exec(
                select(TransaccionDB).where(TransaccionDB.inversor_id == inversor_id)
            ).all()
            
            return jsonify([transaccion.model_dump() for transaccion in transacciones])
        
        except Exception as e:
            logger.error(f"Error al obtener transacciones del inversor con ID {inversor_id}: {str(e)}")
            abort(500, description="Error al consultar la base de datos")

            

@transaccion_bp.route("/accion/<int:accion_id>", methods=["GET"])
def get_transacciones_accion(accion_id):
    """
    Obtiene todas las transacciones que se han realizado con una acción dado su ID

    Parameters
    ----------
    accion_id : int
        ID de la acción cuyas transacciones se quieren consultar

    Returns
    -------
    Response:
        Lista de objetos JSON que representan las transacciones de la acción

    Raises
    ------
    404 Not Found:
        Si no se encuentra una acción con el ID indicado
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            # Verificamos que la acción existe en la base de datos
            accion = session.get(AccionDB, accion_id)
            if accion is None:
                abort(404, description="Acción no encontrada")
                
            transacciones = session.exec(
                select(TransaccionDB).where(TransaccionDB.accion_id == accion_id)
            ).all()
            
            return jsonify([transaccion.model_dump() for transaccion in transacciones])
        
        except Exception as e:
            logger.error(f"Error al obtener transacciones de la acción con ID {accion_id}: {str(e)}")
            abort(500, description="Error al consultar la base de datos")


@transaccion_bp.route("/", methods=["POST"])
def post_nueva_transaccion():
    """
    Crea y almacena una nueva transacción en la base de datos

    El cuerpo de la solicitud debe contener los siguientes campos:
    "inversor_id", "accion_id", "tipo", "cantidad", "precio", y opcionalmente "fecha"

    Returns
    -------
    Tuple[Response, int]:
        Objeto JSON que representa la transacción creada y código de estado 201

    Raises
    ------
    400 Bad Request:
        Si falta alguno de los campos requeridos en la solicitud o si los datos no son válidos
    404 Not Found:
        Si no se encuentra el inversor o la acción
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            data = request.get_json()
            if not data:
                abort(400, description="No han encontrado datos JSON")
                
            # Validamos que todos los campos estén completos
            required_fields = ["inversor_id", "accion_id", "tipo", "cantidad", "precio"]
            for field in required_fields:
                if field not in data:
                    abort(400, description=f"Falta el campo obligatorio: {field}")
            
            # Confirmamos el tipo de transacción que se va a realizar
            if data["tipo"] not in ["compra", "venta"]:
                abort(400, description="El tipo de transacción debe ser 'compra' o 'venta'")
            
            # Revisa si el invbersor existe en la base de datos
            inversor = session.get(InversorDB, data["inversor_id"])
            if inversor is None:
                abort(404, description="Inversor no encontrado")
            
            # revisa si la acción existe en la base de datos
            accion = session.get(AccionDB, data["accion_id"])
            if accion is None:
                abort(404, description="Acción no encontrada")
            
            if data["cantidad"] <= 0:
                abort(400, description="La cantidad debe ser mayor que cero")
            if data["precio"] <= 0:
                abort(400, description="El precio debe ser mayor que cero")
            
            if "fecha" not in data:
                data["fecha"] = datetime.now().isoformat()
            
            # En el caso de una venta, verificamos que haya suficientes acciones
            if data["tipo"] == "venta":
                # Implementar lógica para verificar el saldo de acciones
                # Esta lógica depende de cómo estás llevando el inventario de acciones
                pass
            
            # Creamos la transacción
            nueva_transaccion = TransaccionDB(
                inversor_id=data["inversor_id"],
                accion_id=data["accion_id"],
                tipo=data["tipo"],
                cantidad=data["cantidad"],
                precio=data["precio"],
                fecha=data["fecha"]
            )
            
            # Actualiza el capital del inversor
            monto_total = data["cantidad"] * data["precio"]
            if data["tipo"] == "compra":
                if inversor.capital < monto_total:
                    abort(400, description="El inversor no tiene suficiente capital para esta compra")
                inversor.capital -= monto_total
            else:  # venta
                inversor.capital += monto_total
            
            session.add(nueva_transaccion)
            session.add(inversor)
            session.commit()
            session.refresh(nueva_transaccion)
            
            logger.info(f"Nueva transacción creada con ID: {nueva_transaccion.id}")
            return jsonify(nueva_transaccion.model_dump()), 201
        
        except ValueError as ve:
            logger.warning(f"Error de validación al crear transacción: {str(ve)}")
            abort(400, description=str(ve))

        except Exception as e:
            logger.error(f"Error al crear transacción: {str(e)}")
            session.rollback()
            abort(500, description="Error al crear la transacción")

@transaccion_bp.route("/<int:transaccion_id>", methods=["DELETE"])
def delete_transaccion(transaccion_id):
    """
    Elimina una transacción existente en la base de datos

    Parameters
    ----------
    transaccion_id : int
        ID de la transacción a eliminar

    Returns
    -------
    Response:
        Mensaje de confirmación de que la transacción ha sido eliminada

    Raises
    ------
    404 Not Found:
        Si no se encuentra una transacción con el ID indicado
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            transaccion = session.get(TransaccionDB, transaccion_id)
            if transaccion is None:
                abort(404, description="Transacción no encontrada")
            
            inversor = session.get(InversorDB, transaccion.inversor_id)
            if inversor:
                monto_total = transaccion.cantidad * transaccion.precio
                if transaccion.tipo == "compra":
                    inversor.capital += monto_total  
                else:  
                    inversor.capital -= monto_total  
                session.add(inversor)
            
            session.delete(transaccion)
            session.commit()
            
            logger.info(f"Transacción con ID {transaccion_id} eliminada")
            return jsonify({"message": f"Transacción con ID {transaccion_id} eliminada correctamente"})
        
        except Exception as e:
            logger.error(f"Error al eliminar transacción con ID {transaccion_id}: {str(e)}")
            session.rollback()
            abort(500, description="Error al eliminar la transacción")