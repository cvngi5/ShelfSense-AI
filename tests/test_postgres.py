print("🔥 NEW TEST FILE IS RUNNING")
from database import init_db, create_scan, save_detection, get_scans

print("Initializing database...")
#create the tables if they don't exist
init_db()

print("\nCreating a new scan...") #create one scan event and return its id
scan_id = create_scan(camera_id='CAM_A1', shelf_id='SHELF_1')
print("scan ID:", scan_id)


print("\nSaving detections...")
#save some detectiobs under that scan.
save_detection(scan_id,'bottle', 10, 0.95)
save_detection(scan_id,'can', 5, 0.90)
print("Detections saved.")

print("\nReading data from PostgreSQL...\n")
rows = get_scans() #reads everything back from PostgreSQL.

for row in rows:
    print(row)
    
print("\nDatabase test completed successfully.")  