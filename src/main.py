from flask import Flask, jsonify
from sqlmodel import SQLModel, create_engine, Session
import os
import logging

from models import InversorDB, AccionDB, TransaccionDB  # Importar tus modelos
from routers.inversor_router import inversor_bp
from routers.accion_router import accion_bp
from routers.transaccion_router import transaccion_bp

# from routers.accion_router import accion_bp

app = Flask(__name__)

DATABASE_URL = "sqlite:///simulador.db"
engine = create_engine(DATABASE_URL, echo=True)

# Configurar logs
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    filename='logs/acciones.log',
    filemode='a',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Inicialización de la app
@app.before_first_request
def init_db():
    logging.info("creando tablas de la base de dato...")
    SQLModel.metadata.create_all(engine)
    logging.info("Base de datos creada y poblada con datos iniciales")

# Ruta raíz
@app.route("/")
def root():
    return jsonify({"message": "Simulador de Bolsa activo y base de datos inicializada"})

# Registrar blueprints (equivalente a include_router en FastAPI)
app.register_blueprint(inversor_bp, url_prefix="/inversores")
app.register_blueprint(accion_bp, url_prefix="/acciones")
app.register_blueprint(transaccion_bp, url_prefix="/transacciones")



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
