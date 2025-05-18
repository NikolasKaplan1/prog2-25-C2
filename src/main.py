from flask import Flask, jsonify, request
from sqlmodel import SQLModel, create_engine
from werkzeug.exceptions import HTTPException
import os
import logging
from dotenv import load_dotenv


# Cargamos las variables de entorno
load_dotenv()

# Configuración de la aplicación
app = Flask(__name__)
# Para mantener el orden de las claves ne las respuestas de JSON
app.config['JSON_SORT_KEYS'] = False  

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///simulador.db")
engine = create_engine(DATABASE_URL, echo=bool(os.getenv("SQL_ECHO", "False") == "True"))

# Configuración de los logs
log_level = getattr(logging, os.getenv("LOG_LEVEL", "INFO"))
log_dir = os.getenv("LOG_DIR", "logs")
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=log_level,
    filename=f'{log_dir}/acciones.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Middleware para validar el tipo de contenido
@app.before_request
def validate_content_type():
    if request.method in ['POST', 'PUT', 'PATCH']:
        if request.headers.get('Content-Type') != 'application/json' and request.get_json(silent=True) is not None:
            return jsonify({
                "error": "Content-Type debe ser application/json"
            }), 415

# Inicialización de la base de datos
print("app es instancia de:", type(app))

@app._got_first_request
def init_db():
    try:
        logger.info("Creando tablas de la base de datos...")
        SQLModel.metadata.create_all(engine)
        logger.info("Base de datos creada y poblada con datos iniciales")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {str(e)}")
        raise

# Ruta raíz
@app.route("/")
def root():
    return jsonify({
        "api": "Simulador de Bolsa API",
        "version": "1.0.0",
        "status": "activo",
        "endpoints": {
            "inversores": "/inversores",
            "acciones": "/acciones",
            "transacciones": "/transacciones"
        }
    })

# Ruta de verificación
@app.route("/health")
def health_check():
    try:
        # Verificar la conexión a la base de datos
        from sqlmodel import Session
        with Session(engine) as session:
            session.exec("SELECT 1")
        return jsonify({"status": "healthy", "database": "connected"})
    except Exception as e:
        logger.error(f"Error en health check: {str(e)}")
        return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500

# Controlador de errores globales
@app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, HTTPException):
        response = {
            "error": e.description,
            "status_code": e.code
        }
        status_code = e.code
    else:
        logger.error(f"Error inesperado: {str(e)}")
        response = {
            "error": "Error interno del servidor",
            "status_code": 500
        }
        status_code = 500
    
    return jsonify(response), status_code

# Importamos los blueprints tras definir engine para evitar dependencia circular
def register_blueprints():
    from routers.inversor_router import inversor_bp
    from routers.accion_router import accion_bp
    from routers.transaccion_router import transaccion_bp
    
    # Registra los blueprints 
    app.register_blueprint(inversor_bp, url_prefix="/inversores")
    app.register_blueprint(accion_bp, url_prefix="/acciones")
    app.register_blueprint(transaccion_bp, url_prefix="/transacciones")

if __name__ == "__main__":
    # Registra los blueprints antes de iniciar la aplicación
    register_blueprints()
    
    port = int(os.getenv("PORT", 8000))
    debug = bool(os.getenv("DEBUG", "True") == "True")
    host = os.getenv("HOST", "0.0.0.0")
    
    app.run(host=host, port=port, debug=debug)