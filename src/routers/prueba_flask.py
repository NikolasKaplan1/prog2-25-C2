from flask import Flask, request, jsonify, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib
from database import get_session, create_db_and_tables, drop_db_and_tables, seed_users
from flask_sqlalchemy import SQLAlchemy
from database import Inversor


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


