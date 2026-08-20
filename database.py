import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,  # INTEGER, not string
    "database": "shelfsense",
    "user": "postgres",
    "password": "POSTGRES0305"
}

def get_connection():
    """Create a PostgreSQL database connection"""
    return psycopg2.connect(**DB_CONFIG)

def create_scan(camera_id, shelf_id):
    """Create a new scan entry and return the scan_id"""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO scans (camera_id, shelf_id)
            VALUES (%s, %s)
            RETURNING id
        ''', (camera_id, shelf_id))
        scan_id = cur.fetchone()[0]
        conn.commit()
        return scan_id
    finally:
        conn.close()

def save_detection(scan_id, class_name, count, avg_confidence):
    """Save detection linked to a scan"""
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
    """Return all scans from the database"""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute('''
            SELECT s.id, s.timestamp, s.camera_id, s.shelf_id,
                   d.class_name, d.count, d.avg_confidence
            FROM scans s
            LEFT JOIN detections d ON s.id = d.scan_id
            ORDER BY s.timestamp DESC
        ''')
        return cur.fetchall()
    finally:
        conn.close()