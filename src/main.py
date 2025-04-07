from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import logging

from database import drop_db_and_tables, create_db_and_tables, seed_users
from routers.inversor_router import inversor_bp
# from routers.accion_router import accion_bp

app = Flask(__name__)

# Configurar base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simulador.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
def init_app():
    logging.info("Inicializando aplicación Flask")
    drop_db_and_tables(db)
    create_db_and_tables(db)
    seed_users(db)
    logging.info("Base de datos creada y poblada con datos iniciales")

# Ruta raíz
@app.route("/")
def root():
    return jsonify({"message": "Simulador de Bolsa activo y base de datos inicializada"})

# Registrar blueprints (equivalente a include_router en FastAPI)
app.register_blueprint(inversor_bp, url_prefix="/inversores")
# app.register_blueprint(accion_bp, url_prefix="/acciones")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)