import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def get_db():
    return psycopg2.connect(os.environ.get("DATABASE_URL"))

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS messages (id SERIAL PRIMARY KEY, contenu TEXT NOT NULL) """)
    conn.commit()
    cur.close()
    conn.close()

@app.route("/")
def home():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT contenu FROM messages")
    messages = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', messages=messages)

@app.route("/ajouter", methods=["POST"])
def ajouter():
    contenu = request.form.get("message")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (contenu) VALUES (%s)", (contenu,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect("/")

init_db()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)