from flask import Blueprint, request, jsonify
from database.db_connection import get_connection
from datetime import datetime

import ipaddress

attendance_bp = Blueprint("attendance", __name__)


# ---------------------------------
# Mark Attendance
# ---------------------------------
@attendance_bp.route("/mark_attendance", methods=["POST"])
def mark_attendance():

    data = request.get_json(force=True)

    if not data:
        return jsonify({"error": "No JSON data"}), 400

    student_id = data.get("student_id")
    status = data.get("status")

    if not student_id or not status:
        return jsonify({"error": "Missing fields"}), 400

    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        # Get active session (TIME + NOT CLOSED)
        cursor.execute("""
            SELECT *
            FROM sessions_new
            WHERE NOW() BETWEEN start_time AND end_time
              AND is_closed = 0
            ORDER BY start_time DESC
            LIMIT 1
        """)

        session = cursor.fetchone()

        if not session:
            return jsonify({"error": "No active session"}), 403

        session_id = session["session_id"]

        # Check duplicate attendance
        cursor.execute("""
            SELECT 1
            FROM attendance_new
            WHERE student_id=%s AND session_id=%s
        """, (student_id, session_id))

        if cursor.fetchone():
            return jsonify({"error": "already_marked"}), 409

        # Insert attendance
        cursor.execute("""
            INSERT INTO attendance_new
            (student_id, session_id, status)
            VALUES (%s, %s, %s)
        """, (student_id, session_id, status))

        db.commit()

        cursor.close()
        db.close()

        return jsonify({
            "message": "success",
            "session_id": session_id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------
# Check If Already Marked (Student)
# ---------------------------------
@attendance_bp.route("/check_attendance/<int:student_id>", methods=["GET"])
def check_attendance(student_id):

    db = None
    cursor = None


    try:

        db = get_connection()
        cursor = db.cursor(dictionary=True)


        cursor.execute(
            """
            SELECT 1
            FROM attendance_new a
            JOIN sessions_new s
              ON a.session_id = s.session_id
            WHERE a.student_id=%s
              AND s.status='ACTIVE'
            """,
            (student_id,)
        )

        data = cursor.fetchone()


        if data:
            return jsonify({"marked": True})


        return jsonify({"marked": False})


    except Exception as e:

        return jsonify({"error": str(e)}), 500


    finally:

        if cursor:
            cursor.close()

        if db:
            db.close()

# -------------------------------
# Student Attendance History
# -------------------------------
@attendance_bp.route("/student_history/<int:student_id>", methods=["GET"])
def student_history(student_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    query = """
    SELECT 
        c.course_name,
        a.status,
        a.timestamp
    FROM attendance_new a

    JOIN sessions_new s ON a.session_id = s.session_id
    JOIN courses c ON s.course_id = c.course_id

    WHERE a.student_id = %s

    ORDER BY a.timestamp DESC
    """

    cursor.execute(query, (student_id,))

    data = cursor.fetchall()

    db.close()

    return jsonify(data)

