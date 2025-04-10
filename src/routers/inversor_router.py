from flask import Flask, request, jsonify, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib
from database import get_session, create_db_and_tables, drop_db_and_tables, seed_users
from flask_sqlalchemy import SQLAlchemy
from models import Inversor


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inversores.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Inversor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    capital = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "capital": self.capital
        }
    
@app.route("/inversores", methods=["GET"])
def get_inversor():
    inversores = Inversor.query.all()
    return jsonify([inversor.to_dict()] for inversor in inversores)

@app.route("/inversores/<int:inversor_id>", methods=["GET"])
def get_inversor_id(inversor_id):
    inversor = Inversor.query.get(inversor_id)
    if inversor is None:
        abort(404, description="Inversor no encontrado")
    return jsonify(inversor.to_dict())

@app.route("/inversores", methods=["POST"])
def post_nuevo_inversor():
    data = request.get_json()
    if not all(key in data for key in ("nombre", "email", "capital")):
        abort(400, description= "Faltan campos obligatorios por completar")
    
    nuevo = Inversor(nombre=data["nombre"], email=data["email"], capital=data["capital"])
    db.session.add(nuevo)
    db.session.commit()
    return jsonify(nuevo.to_dict())

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port= 8000)




