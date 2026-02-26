from flask import Flask
from flask_cors import CORS
from routes.student_routes import student_bp
from routes.attendance_routes import attendance_bp
from routes.session_routes import session_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)

CORS(app)

# Register Blueprints
app.register_blueprint(student_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(session_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return "Backend Running Locally ✅"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)