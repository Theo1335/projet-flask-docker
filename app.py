import os
import psycopg2
from psycopg2 import pool
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 3,   
    dsn=os.environ.get("DATABASE_URL")
)

def get_db():
    return connection_pool.getconn()

def release_db(conn):
    connection_pool.putconn(conn)

def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            contenu TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    release_db(conn)

init_db()

@app.route("/")
def home():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT contenu FROM messages")
    messages = cur.fetchall()
    cur.close()
    release_db(conn)
    return render_template('index.html', messages=messages)

@app.route("/ajouter", methods=["POST"])
def ajouter():
    contenu = request.form.get("message")
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (contenu) VALUES (%s)", (contenu,))
    conn.commit()
    cur.close()
    release_db(conn)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)