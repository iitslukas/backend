import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

# --- Gemini setup ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

SYSTEM_PROMPT = """Si priateľský a inteligentný AI asistent pre stránku Student Gallery.
Táto stránka zobrazuje nasledovných 10 študentov (zo súboru data.json):

ID 1  – Peter Hruška
ID 2  – Jana Malá
ID 3  – Michal Kováč
ID 4  – Lucia Srnková
ID 5  – Marek Vysoký
ID 6  – Ema Biela
ID 7  – Dávid Čierny
ID 8  – Simona Veselá
ID 9  – Jakub Dlhý
ID 10 – Katarína Šikovná

Dáta sú dostupné cez GitHub Raw: https://raw.githubusercontent.com/iitslukas/backend/refs/heads/main/docs/data.json
Backend je napísaný vo Flasku (Python), frontend používa čisté HTML/CSS/JavaScript.
Odpovedáš v slovenčine, ak sa ťa pýtajú po slovensky. Ak sa pýtajú po anglicky, odpovedáš po anglicky.
Si nápomocný, priateľský a stručný. Používaj emoji kde to je vhodné."""

# --- Student data ---
studenti = [
    {"id": 1, "meno": "Peter", "priezvisko": "Hruška", "image": "https://picsum.photos/id/1/200"},
    {"id": 2, "meno": "Jana", "priezvisko": "Malá", "image": "https://picsum.photos/id/10/200"},
    {"id": 3, "meno": "Michal", "priezvisko": "Kováč", "image": "https://picsum.photos/id/20/200"},
    {"id": 4, "meno": "Lucia", "priezvisko": "Srnková", "image": "https://picsum.photos/id/30/200"},
    {"id": 5, "meno": "Marek", "priezvisko": "Vysoký", "image": "https://picsum.photos/id/40/200"},
    {"id": 6, "meno": "Ema", "priezvisko": "Biela", "image": "https://picsum.photos/id/50/200"},
    {"id": 7, "meno": "Dávid", "priezvisko": "Čierny", "image": "https://picsum.photos/id/60/200"},
    {"id": 8, "meno": "Simona", "priezvisko": "Veselá", "image": "https://picsum.photos/id/70/200"},
    {"id": 9, "meno": "Jakub", "priezvisko": "Dlhý", "image": "https://picsum.photos/id/80/200"},
    {"id": 10, "meno": "Katarína", "priezvisko": "Šikovná", "image": "https://picsum.photos/id/90/200"},
]

# --- Existing routes ---
@app.route('/')
def home():
    return "Vitajte na mojom prvom backend API!"

@app.route('/api')
def get_all_students():
    return jsonify(studenti)

@app.route('/api/student/<int:student_id>')
def get_student(student_id):
    # Hľadáme študenta podľa ID
    student = next((s for s in studenti if s["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"error": "Študent sa nenašiel"}), 404

# --- AI Chat route ---
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
        # Build contents list from history + new message
        contents = raw_history + [{"role": "user", "parts": [{"text": user_message}]}]

        response = client.models.generate_content(
            model="gemini-3-flash-preview",
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