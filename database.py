import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            camera_id VARCHAR(50),
            shelf_id VARCHAR(50)
        );
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS detections (
            id SERIAL PRIMARY KEY,
            scan_id INTEGER REFERENCES scan(id) ON DELETE CASCADE,
            class_name VARCHAR(100),
            count INTEGER,
            avg_confidence REAL
        );
    ''')

    conn.commit()
    cur.close()
    conn.close()

def create_scan(camera_id='CAM_A1', shelf_id='SHELF_1'):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute('''
                INSERT INTO scans
                (camera_id, shelf_id)
                VALUES(%s, %s)
                RETURNING id;
                ''', (camera_id, shelf_id))
      
    scan_id = cur.fetchone()[0]
    
    conn.commit()
    cur.close()
    conn.close()
    
    return scan_id

def save_detection(scan_id, class_name, count, avg_confidence):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute('''
                INSERT INTO detections
                (scan_id, class_name, count, avg_confidence)
                VALUES(%s, %s, %s, %s);
                ''', (scan_id, class_name, count, avg_confidence))

    conn.commit()
    cur.close()
    conn.close()

def get_scans():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute('''
                SELECT
            s.id,
            s.timestamp,
            s.camera_id,
            s.shelf_id,
            json_agg(json_build_object(
                'class_name', d.class_name,
                'count', d.count,
                'avg_confidence', d.avg_confidence
            )) AS detections
        FROM scans s
        LEFT JOIN detections d ON s.id = d.scan_id
        GROUP BY s.id, s.timestamp, s.camera_id, s.shelf_id
        ORDER BY s.timestamp DESC;
                ''') 
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return rows
