import os
import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, send_from_directory, Response
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
    try:
        with get_db() as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM students ORDER BY id")
            return jsonify(cur.fetchall())
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

# ── SPA fallback (serves React app for any non-API route) ────────────────────

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path: str) -> Response:
    file_path = os.path.join(app.static_folder, path)  # type: ignore[arg-type]
    if path and os.path.isfile(file_path):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
