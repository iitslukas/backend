import os
from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# --- Gemini setup ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """Si priateľský a inteligentný AI asistent pre stránku Student Gallery.
Táto stránka zobrazuje zoznam študentov (Peter Hruška, Jana Malá, Michal Kováč,
Lucia Srnková, Marek Vysoký, Ema Biela, Dávid Čierny, Simona Veselá, Jakub Dlhý, Katarína Šikovná).
Backend je napísaný vo Flasku (Python) a frontend používa čisté HTML/CSS/JavaScript.
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
    if not GEMINI_API_KEY:
        return jsonify({"error": "GEMINI_API_KEY nie je nastavený na serveri."}), 500

    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Chýba pole 'message'."}), 400

    user_message = data['message']
    # history: list of {"role": "user"|"model", "parts": [{"text": "..."}]}
    raw_history = data.get('history', [])

    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            system_instruction=SYSTEM_PROMPT
        )
        # Build chat with existing history (excluding the last user message)
        chat_session = model.start_chat(history=raw_history[:-1] if raw_history else [])
        response = chat_session.send_message(user_message)
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)