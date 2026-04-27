import os
import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="docs", static_url_path="")
CORS(app)

DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "dpg-d7ng6tpf9bms738ggtv0-a.oregon-postgres.render.com"),
    "port":     os.getenv("DB_PORT",     "5432"),
    "dbname":   os.getenv("DB_NAME",     "database_87435"),
    "user":     os.getenv("DB_USER",     "database_87435_user"),
    "password": os.getenv("DB_PASSWORD", "6uImoKTzI7jrORsyibzwuQqByoK1W5BA"),
}

def get_db():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=psycopg2.extras.RealDictCursor)

# Serve frontend
@app.route("/")
def index():
    return send_from_directory("docs", "index.html")

@app.route("/chat")
def chat_page():
    return send_from_directory("docs", "chat.html")

# API
@app.route("/api")
def get_students():
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM students ORDER BY id")
        return jsonify(cur.fetchall())

@app.route("/api/student/<int:student_id>")
def get_student(student_id):
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cur.fetchone()
    if student:
        return jsonify(student)
    return jsonify({"error": "Študent sa nenašiel"}), 404

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
