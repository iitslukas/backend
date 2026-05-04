import os
import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, send_from_directory, Response, request
from flask_cors import CORS

app = Flask(__name__, static_folder="docs", static_url_path="")
CORS(app)

def get_db():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "dpg-d7ng6tpf9bms738ggtv0-a.oregon-postgres.render.com"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "database_87435"),
        user=os.getenv("DB_USER", "database_87435_user"),
        password=os.getenv("DB_PASSWORD", "6uImoKTzI7jrORsyibzwuQqByoK1W5BA"),
        cursor_factory=psycopg2.extras.RealDictCursor,
    )

# ── API ──────────────────────────────────────────────────────────────────────

@app.route("/api")
def get_students() -> Response:
    sort = request.args.get("sort", "id_asc")
    try:
        with get_db() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM students ORDER BY id")
            students = list(cur.fetchall())

        sort_map = {
            "id_asc":       (lambda s: s["id"],                        False),
            "id_desc":      (lambda s: s["id"],                        True),
            "name_asc":     (lambda s: s["meno"].lower(),              False),
            "name_desc":    (lambda s: s["meno"].lower(),              True),
            "surname_asc":  (lambda s: s["priezvisko"].lower(),        False),
            "surname_desc": (lambda s: s["priezvisko"].lower(),        True),
            "age_asc":      (lambda s: s.get("vek") or 0,             False),
            "age_desc":     (lambda s: s.get("vek") or 0,             True),
        }
        if sort in sort_map:
            key_fn, reverse = sort_map[sort]
            students = sorted(students, key=key_fn, reverse=reverse)

        return jsonify(students)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/student/<int:student_id>")
def get_student(student_id: int) -> Response:
    try:
        with get_db() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
            student = cur.fetchone()
        if student:
            return jsonify(student)
        return jsonify({"error": "Študent sa nenašiel"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat")
def chat_page() -> Response:
    return send_from_directory("docs", "chat.html")

@app.route("/")
def index() -> Response:
    return send_from_directory("docs", "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
