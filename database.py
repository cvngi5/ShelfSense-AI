import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

def get_connection():
    """create a PostgreSQL database connection"""
    return psycopg2.connect(**DB_CONFIG)

def create_scan(camera_id, shelf_id):
    """create a new scan entry and return the scan_id"""
    conn = get_connection()
    
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO scans (camera_id, shelf_id,)
            VALUES (%s, %s,)
            RETURNING scan_id
        ''', (camera_id, shelf_id))
        
        scan_id = cur.fetchone()[0]
        conn.commit()
        
        return scan_id
    
    finally:
        conn.close()
        
def save_detection(scan_id, class_name, count, avg_confidence):
    """save detection linked to a scan."""
    conn = get_connection()
    
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO detections (scan_id, class_name, count, avg_confidence)
            VALUES (%s, %s, %s, %s)
        ''', (scan_id, class_name, count, avg_confidence))
        
        conn.commit()
        
    finally:
        conn.close()
        
def get_all_scans():
    '''Return all scans from the database'''
    conn = get_connection()
    
    try:
        cur = conn.cursor()
        
        cur.execute('''
            SELECT
                s.id,
                 s.timestamp,
                 s.camera_id,
                 s.shelf_id,
                 d.class_name,
                 d.count,
                 d.avg_confidence
             FROM scans s
             LEFT JOIN detections d ON s.id = d.scan_id
             ORDER BY s.timestamp DESC
             ''')
        
        return cur.fetchall()
    
    finally:
        conn.close()