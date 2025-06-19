from flask import Flask, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_db_connection():
    return psycopg2.connect(
        host="db",
        dbname="postgres",
        user="postgres",
        password="postgres"
    )

@app.route('/api/health')
def health():
    try:
        conn = get_db_connection()
        conn.close()
        return "API and DB connected successfully!", 200
    except Exception as e:
        return f"DB Connection Failed: {str(e)}", 500

@app.route('/api/quotes')
def get_quotes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, quote, author FROM quotes;")
    quotes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{'id': q[0], 'quote': q[1], 'author': q[2]} for q in quotes])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)