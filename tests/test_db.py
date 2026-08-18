from database import init_db, save_detection, get_all_detections

init_db()
save_detection('bottle', 9, 0.72)
save_detection('bottle', 8, 0.88)

results = get_all_detections()
for row in results:
    print(row)