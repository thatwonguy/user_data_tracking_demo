from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)

# Initialize SQLite database
def init_db():
    with sqlite3.connect('usage_data.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS user_usage (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                event_type TEXT,
                event_data TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track_event', methods=['POST'])
def track_event():
    user_id = request.json.get('user_id')
    event_type = request.json.get('event_type')
    event_data = request.json.get('event_data')
    
    with sqlite3.connect('usage_data.db') as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO user_usage (user_id, event_type, event_data) 
            VALUES (?, ?, ?)
        ''', (user_id, event_type, event_data))
        conn.commit()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
