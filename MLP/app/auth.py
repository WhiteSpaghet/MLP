# app/auth.py

from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

USERS_FILE = os.path.join("app", "users.json")

# Asegurar archivo de usuarios
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)

def load_users():
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    users = load_users()
    if username in users:
        return jsonify({"error": "Usuario ya existe"}), 400

    users[username] = generate_password_hash(password)
    save_users(users)
    return jsonify({"msg": "Usuario registrado exitosamente"})

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    users = load_users()
    if username not in users:
        return jsonify({"error": "Usuario no encontrado"}), 404

    if not check_password_hash(users[username], password):
        return jsonify({"error": "Contraseña incorrecta"}), 401

    session["user"] = username
    return jsonify({"msg": "Login exitoso", "user": username})

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"msg": "Logout exitoso"})
