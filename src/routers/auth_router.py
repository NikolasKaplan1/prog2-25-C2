from flask import Blueprint, request, jsonify, abort
from sqlmodel import Session, select
from models import InversorDB
from datetime import datetime
import logging

# Creamos un logger para este módulo
logger = logging.getLogger(__name__)

auth_bp = Blueprint('autenticacion', __name__)

# Importamos engine
def get_engine():
    from app import engine
    return engine

@auth_bp.route("/register", methods=["POST"])
def register_inversor():
    """
    Registra un nuevo inversor

    Requiere en el cuerpo JSON los campos:
    "nombre", "apellidos", "email", "contrasena", "tarjeta_credito", "capital"

    Returns
    -------
    Tuple[Response, int]:
        Objeto JSON del inversor creado y código 201

    Raises
    ------
    400 Bad Request:
        Si faltan campos requeridos
    409 Conflict:
        Si el email ya está registrado
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            data = request.get_json()
            if not data:
                abort(400, description="No se han encontrado datos JSON")

            required_fields = [
                "nombre", "apellidos", "email", "contrasena",
                "tarjeta_credito", "capital"
            ]
            for field in required_fields:
                if field not in data:
                    abort(400, description=f"Falta el campo obligatorio: {field}")

            # Verificar si ya existe el email
            existente = session.exec(
                select(InversorDB).where(InversorDB.email == data["email"])
            ).first()
            if existente:
                abort(409, description="El email ya está registrado")

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
            logger.info(f"Nuevo inversor registrado: {nuevo.email}")
            return jsonify(nuevo.model_dump()), 201

        except ValueError as e:
            logger.warning(f"Error de validación: {str(e)}")
            abort(400, description=str(e))
        except Exception as e:
            logger.error(f"Error al registrar inversor: {str(e)}")
            session.rollback()
            abort(500, description="Error al registrar el inversor")


@auth_bp.route("/login", methods=["POST"])
def login_inversor():
    """
    Autentica a un inversor y devuelve un token ficticio

    Requiere en el cuerpo JSON los campos:
    "email" y "contrasena"

    Returns
    -------
    Tuple[Response, int]:
        JSON con token de acceso y código 200

    Raises
    ------
    400 Bad Request:
        Si faltan campos obligatorios
    401 Unauthorized:
        Si las credenciales son inválidas
    """
    engine = get_engine()
    with Session(engine) as session:
        try:
            data = request.get_json()
            if not data:
                abort(400, description="No se han encontrado datos JSON")

            required_fields = ["email", "contrasena"]
            for field in required_fields:
                if field not in data:
                    abort(400, description=f"Falta el campo obligatorio: {field}")

            inversor = session.exec(
                select(InversorDB).where(InversorDB.email == data["email"])
            ).first()

            if not inversor or inversor.contrasena != data["contrasena"]:
                abort(401, description="Credenciales inválidas")

            token = f"TOKEN_{inversor.id}_{inversor.email}"
            logger.info(f"Inversor autenticado: {inversor.email}")
            return jsonify({"access_token": token}), 200

        except Exception as e:
            logger.error(f"Error en login: {str(e)}")
            abort(500, description="Error interno en la autenticación")