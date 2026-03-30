from flask import Flask, jsonify

app = Flask(__name__)

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
    {"id": 10, "meno": "Katarína", "priezvisko": "Šikovná", "image": "https://picsum.photos/id/90/200"}
]

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

if __name__ == '__main__':
    app.run(debug=True)