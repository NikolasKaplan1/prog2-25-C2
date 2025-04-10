from flask import Flask, request, jsonify, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib
from database import get_session, create_db_and_tables, drop_db_and_tables, seed_users
from flask_sqlalchemy import SQLAlchemy
from models import Transaccion


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mercado.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/transacciones", methods=["GET"])
def get_transacciones():
    session = get_session()
    query = session.exec(Transaccion)

    inversor_id = request.args.get("inversor_id")
    accion_id = request.args.get("accion_id")

    if inversor_id:
        query = query.filter(Transaccion.inversor_id == inversor_id)

    if accion_id:
        query = query.filter(Transaccion.accion_id == accion_id)

    transacciones = query.all()

    res = [{"id": transaccion.id, "inversor_id": transaccion.inversor_id, "accion_id": transaccion.accion_id, "cantidad": transaccion.cantidad, "precio": transaccion.precio, "frecha": transaccion.fecha.isoformat()} for transaccion in transacciones]

    return jsonify(res), 200

@app.route("/transacciones/<int:transaccion_id>", methods=["GET"])
def get_transaccion(transaccion_id: int):
    session = get_session()
    transaccion = session.exec(Transaccion).filter_by(id=transaccion_id).first()

    if transaccion is None:
        abort(404, description="Transaccion no encontrada")

    res = {"id": transaccion.id, "inversor_id": transaccion.inversor_id, "accion_id": transaccion.accion_id, "cantidad": transaccion.cantidad, "precio": transaccion.precio, "frecha": transaccion.fecha.isoformat()}

    return jsonify(res), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
