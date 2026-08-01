from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_objects(image_path):
    results = model(image_path)
    detection = results[0]
    
    output = []
    for box in detection.boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])
        
        output.append({
            "class_name": class_name,
            "confidence": confidence,
        })
    return output
