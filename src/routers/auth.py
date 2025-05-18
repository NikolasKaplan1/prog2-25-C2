from flask import Blueprint, request, jsonify
from models import User
from database import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Faltan campos"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Usuario ya existe"}), 409

    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Usuario registrado"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if not user or not user.check_password(data.get('password')):
        return jsonify({"error": "Credenciales inválidas"}), 401

    token = create_access_token(identity=user.username)
    return jsonify(access_token=token)
