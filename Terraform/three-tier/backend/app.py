from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow CORS for communication with React frontend

# Connect to SQLite database (creates the file if not exists)
def get_db_connection():
    conn = sqlite3.connect('feedback.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create the feedback table if not exists
def init_db():
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        comment TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    name = data.get('name')
    comment = data.get('comment')

    if not name or not comment:
        return jsonify({'error': 'Name and comment are required'}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO feedback (name, comment) VALUES (?, ?)', (name, comment))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Feedback submitted successfully'}), 201

@app.route('/feedback', methods=['GET'])
def get_feedback():
    conn = get_db_connection()
    feedbacks = conn.execute('SELECT * FROM feedback').fetchall()
    conn.close()

    feedback_list = [{'id': row['id'], 'name': row['name'], 'comment': row['comment']} for row in feedbacks]
    return jsonify(feedback_list)

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
