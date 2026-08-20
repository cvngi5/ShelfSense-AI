import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="shelfsense",
    user="postgres",
    password="POSTGRES0305"
)
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS scans (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
        camera_id VARCHAR(50),
        shelf_id VARCHAR(50)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS detections (
        id SERIAL PRIMARY KEY,
        scan_id INTEGER NOT NULL,
        class_name VARCHAR(100),
        count INTEGER,
        avg_confidence REAL,
        FOREIGN KEY (scan_id) REFERENCES scans(id)
    )
''')

conn.commit()

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
print("Tables in this database:", cur.fetchall())

conn.close()