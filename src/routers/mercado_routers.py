from flask import Flask, request, jsonify, abort
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import hashlib
from database import get_session, create_db_and_tables, drop_db_and_tables, seed_users
from flask_sqlalchemy import SQLAlchemy
from models import Mercado


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mercado.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

@app.route("/mercado/simular", methods=["POST"])
def post_simular_mercado():
    session = get_session()
    acciones = session.exec(Mercado).all()

    if acciones is None:
        abort(404, description="No hay acciones en el mercado")

    modificadas = 0
    
    for accion in acciones:
        precio_act = accion.precio

        if accion.precio < 100:
            accion.precio *= 1.05

        else:
            accion.precio *= 0.98

        if accion.precio != precio_act:
            modiicadas += 1

    session.commit()

    return jsonify({"mensage": "Precios actualizados", "acciones_modificadas": modificadas}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)


