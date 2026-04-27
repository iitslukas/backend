import os
import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

# --- Database ---
DB_CONFIG = {
    "host":     os.getenv("DB_HOST",     "dpg-d7ng6tpf9bms738ggtv0-a.oregon-postgres.render.com"),
    "port":     os.getenv("DB_PORT",     "5432"),
    "dbname":   os.getenv("DB_NAME",     "database_87435"),
    "user":     os.getenv("DB_USER",     "database_87435_user"),
    "password": os.getenv("DB_PASSWORD", "6uImoKTzI7jrORsyibzwuQqByoK1W5BA"),
}

def get_db():
    return psycopg2.connect(**DB_CONFIG, cursor_factory=psycopg2.extras.RealDictCursor)

def init_db():
    sql_path = os.path.join(os.path.dirname(__file__), "students.sql")
    with get_db() as conn, conn.cursor() as cur, open(sql_path, "r", encoding="utf-8") as f:
        cur.execute(f.read())

try:
    init_db()
except Exception as e:
    print(f"DB init warning: {e}")

# --- Gemini setup ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

SYSTEM_PROMPT = """Si priateľský a inteligentný AI asistent pre stránku Student Gallery.
Backend je napísaný vo Flasku (Python) s PostgreSQL, frontend používa čisté HTML/CSS/JavaScript.
Odpovedáš v slovenčine, ak sa ťa pýtajú po slovensky. Ak sa pýtajú po anglicky, odpovedáš po anglicky.
Si nápomocný, priateľský a stručný. Používaj emoji kde to je vhodné."""

# --- Routes ---
@app.route('/')
def home():
    return "Vitajte na Student Gallery API!"

@app.route('/api')
def get_all_students():
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM students ORDER BY id")
        return jsonify(cur.fetchall())

@app.route('/api/student/<int:student_id>')
def get_student(student_id):
    with get_db() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM students WHERE id = %s", (student_id,))
        student = cur.fetchone()
    if student:
        return jsonify(student)
    return jsonify({"error": "Študent sa nenašiel"}), 404

@app.route('/api/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({"error": "GEMINI_API_KEY nie je nastavený na serveri."}), 500

    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Chýba pole 'message'."}), 400

    user_message = data['message']
    raw_history = data.get('history', [])

    try:
        contents = raw_history + [{"role": "user", "parts": [{"text": user_message}]}]
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.85,
                max_output_tokens=1024,
            )
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)
