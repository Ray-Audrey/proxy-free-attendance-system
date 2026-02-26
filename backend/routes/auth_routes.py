from flask import Blueprint, request, jsonify
from database.db_connection import get_connection

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Missing fields"}), 400

        db = get_connection()
        cursor = db.cursor(dictionary=True)  # ✅ IMPORTANT FIX

        query = "SELECT user_id, role, student_id FROM users WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))

        user = cursor.fetchone()

        cursor.close()
        db.close()

        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        return jsonify({
            "user_id": user["user_id"],
            "role": user["role"],
            "student_id": user["student_id"]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500