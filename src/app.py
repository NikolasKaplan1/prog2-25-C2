
"""
Módulo principal de la API REST del simulador de bolsa

En este módulo configuramos y ejecutamos la API Flask que proporciona endpoints
para gestionar inversores, acciones, transacciones y autenticación de usuarios

Attributes
----------
app : Flask
    La aplicación Flask principal
engine : Engine
    Motor de SQLAlchemy conectado a la base de datos 
"""
from flask import Flask, jsonify, request
from sqlmodel import SQLModel, create_engine, Session
from werkzeug.exceptions import HTTPException
from sqlalchemy import text
from dotenv import load_dotenv
import logging
import os

# Carga variables de entorno
load_dotenv()

# Configuración general de Flask
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False 

# Configuración de base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///simulador.db")
engine = create_engine(DATABASE_URL, echo=os.getenv("SQL_ECHO", "False") == "True")

# Configuración de logs
log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
log_dir = os.getenv("LOG_DIR", "logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=log_level,
    filename=os.path.join(log_dir, "acciones.log"),
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@app.before_request
def validate_content_type():
    """
    Valida que las peticiones POST y PUT tengan 'Content-Type: application/json'

    Returns
    -------
    Response:
        Mensaje de error en caso de que el Content-Type no sea correcto
    """
    if request.method in ['POST', 'PUT', 'PATCH']:
        if request.headers.get('Content-Type') != 'application/json' and request.get_json(silent=True) is not None:
            return jsonify({"error": "Content-Type debe ser application/json"}), 415

def init_db(seed: bool = False):
    """
    Inicializa las tablas de la base de datos

    Si "seed" es True, se introducen datos de ejemplo en la base de datos

    Parameters
    ----------
    seed : bool
        Si se quiere rellenar la base de datos con datos de ejemplo
    """
    try:
        from models.models import InversorDB, AccionDB, TransaccionDB
        logger.info("Creando tablas de la base de datos con SQLModel")
        SQLModel.metadata.create_all(engine)

        if seed:
            from sqlmodel import Session
            with Session(engine) as session:
                apple = AccionDB(nombre="Apple Inc.", simbolo="AAPL", precio_actual=180.0, historial_precios="{}")
                carlos = InversorDB(
                    nombre="Carlos", apellidos="Pérez", email="carlos@example.com",
                    contrasena="1234", tarjeta_credito="1234-5678-1234-5678", capital=10000.0
                )
                session.add(apple)
                session.add(carlos)
                session.commit()
                logger.info("Datos demo insertados correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {str(e)}")
        print(f"[ERROR init_db] {e}")  
        raise

@app.route("/")
def root():
    """
    Endpoint raíz de la API

    Returns
    -------
    Response:
        Información general sobre la API y sus endpoints disponibles
    """
    return jsonify({
        "api": "Simulador de Bolsa API",
        "version": "1.0.0",
        "status": "activo",
        "endpoints": {
            "inversores": "/inversores",
            "acciones": "/acciones",
            "transacciones": "/transacciones",
            "autenticaciones": "/autenticaciones"
        }
    })

@app.route("/health")
def health_check():
    """
    Endpoint de verificación del estado del servidor y conexión a la base de datos

    Returns
    -------
    Response:
        Estado de la aplicación y de la base de datos
    """
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    """
    Controlador global de errores para toda la app

    Parameters
    ----------
    e : Exception
        Excepción lanzada

    Returns
    -------
    Response:
        Mensaje de error en formato JSON
    """
    if isinstance(e, HTTPException):
        return jsonify({"error": e.description, "status_code": e.code}), e.code
    logger.error(f"Error inesperado: {str(e)}")
    return jsonify({"error": "Error interno del servidor", "status_code": 500}), 500

def register_blueprints():
    """
    Registra los Blueprints de los diferentes módulos de la API
    """
    from routers.inversor_router import inversor_bp
    from routers.accion_router import accion_bp
    from routers.transaccion_router import transaccion_bp
    from routers.auth_router import auth_bp

    app.register_blueprint(inversor_bp, url_prefix="/inversores")
    app.register_blueprint(accion_bp, url_prefix="/acciones")
    app.register_blueprint(transaccion_bp, url_prefix="/transacciones")
    app.register_blueprint(auth_bp, url_prefix="/autenticaciones")
    
# Exportaciones para WSGI y dev_run.py
__all__ = ["app", "engine", "init_db", "register_blueprints"]

