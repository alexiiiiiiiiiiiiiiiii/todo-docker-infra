from flask import Flask, jsonify, request, Response
import psycopg2
import os
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter

app = Flask(__name__)

# ➕ Init Prometheus metrics
metrics = PrometheusMetrics(app)
task_counter = Counter("todo_api_tasks_total", "Nombre total de requêtes GET /api/tasks")
add_task_counter = Counter("todo_api_add_task_total", "Nombre total de tâches ajoutées via POST")

# 🔌 Connexion à PostgreSQL
def get_db():
    return psycopg2.connect(
        host="db",
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

# ✅ GET toutes les tâches
@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    task_counter.inc()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks;")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks)

# ➕ POST ajout de tâche
@app.route("/api/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or "label" not in data:
        return jsonify({"error": "Le champ 'label' est requis"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (label) VALUES (%s);", (data["label"],))
    conn.commit()
    cur.close()
    conn.close()
    add_task_counter.inc()
    return jsonify({"message": "Tâche ajoutée"}), 201

# 📤 Export CSV
@app.route("/api/export", methods=["GET"])
def export_csv():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, label FROM tasks;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    output = "id,label\n"
    output += "\n".join([f"{row[0]},{row[1]}" for row in rows])
    return Response(output, mimetype="text/csv")

# 🔁 Health check pour Traefik
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

# ▶️ Lancement de l’app Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("API_PORT", 5000)))
