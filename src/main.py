from flask import Flask, jsonify
import os
import logging

from src.database.db_manager import init_db           # ← 1
from routers.inversor_router import inversor_bp
from routers.accion_router import accion_bp
from routers.transaccion_router import transaccion_bp

app = Flask(__name__)

# ---------------------------------------------------
#  Logs
# ---------------------------------------------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    filename="logs/acciones.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# ---------------------------------------------------
#  Crear BD (una sola vez)
# ---------------------------------------------------
@app.before_first_request
def bootstrap_db():
    logging.info("Creando tablas (si no existen)…")
    init_db(seed=False)                               # 2
    logging.info("Base de datos lista.")

# ---------------------------------------------------
#  Rutas base
# ---------------------------------------------------
@app.route("/")
def root():
    return jsonify({"message": "Simulador de Bolsa activo y BD inicializada"})

# ---------------------------------------------------
#  Blueprints
# ---------------------------------------------------
#  IMPORTANTE: los routers ahora definen rutas relativas "/", no "*/acciones*".
app.register_blueprint(inversor_bp,  url_prefix="/inversores")
app.register_blueprint(accion_bp,    url_prefix="/acciones")
app.register_blueprint(transaccion_bp, url_prefix="/transacciones")

# ---------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
