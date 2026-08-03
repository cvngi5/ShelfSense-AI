import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('shelf_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY,
            timestamp TEXT,
            class_name TEXT,
            count INTEGER,
            avg_confidence REAL
        )
    ''')
    conn.commit()
    conn.close()
    
def save_detection(class_name, count, avg_confidence):
    conn = sqlite3.connect('shelf_data.db')
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    
    c.execute('''
              INSERT INTO detections (timestamp, class_name, count, avg_confidence)
              VALUES (?, ?, ?, ?)
              ''', (timestamp, class_name, count, avg_confidence))
    conn.commit()
    conn.close()
        
def get_all_detections():
            conn = sqlite3.connect('shelf_data.db')
            c = conn.cursor()
            c.execute('SELECT * FROM detections')
            rows = c.fetchall()
            conn.close()
            return rows         