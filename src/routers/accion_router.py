from flask import Flask, request, jsonify, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib
from database import get_session, create_db_and_tables, drop_db_and_tables, seed_users
from flask_sqlalchemy import SQLAlchemy
from models import Accion

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///acciones.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Accion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    simbolo = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), unique=True, nullable=False)
    precio = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "simbolo": self.simbolo,
            "nombre": self.nombre,
            "precio": self.precio
        }

@app.route("/acciones", methods=["GET"])
def get_acciones():
    acciones = Accion.query.all()
    return jsonify([accion.to_dict()] for accion in acciones)

@app.route("/acciones/<int:accion_id>", methods=["GET"])
def get_accion_id(accion_id):
    accion = Accion.query.get(accion_id)
    if accion is None:
        abort(404, description="Accion no encontrada")
    return jsonify(accion.to_dict())

@app.route("/acciones", methods=["POST"])
def post_nueva_accion():
    data = request.get_json()
    if not all(key in data for key in ("simbolo", "nombre", "precio")):
        abort(400, description="faltan campos obligatorios por completar")
    
    nuevo = Accion(simbolo=data["simbolo"], nombre=data["nombre"],precio=data["precio"] )
    db.session.add(nuevo)
    db.session.comit()
    return jsonify(nuevo.to_dict())


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)

#cambios
