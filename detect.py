from ultralytics import YOLO

model = YOLO('model/yolov8n.pt')

def detect_objects(image_path):
    results = model(image_path)
    detections = results[0]
    
    class_counts = {}
    class_confidences = {}
    
    for box in detections.boxes:
        class_id = int(box.cls[0])
        class_name = model.names[class_id]
        confidence = float(box.conf[0])
        
        if class_name not in class_counts:
            class_counts[class_name] = 0
            class_confidences[class_name] = []
        
        class_counts[class_name] += 1
        class_confidences[class_name].append(confidence)
    
    output = {}
    for class_name in class_counts:
        avg_conf = sum(class_confidences[class_name]) / len(class_confidences[class_name])
        output[class_name] = {
            'count': class_counts[class_name],
            'avg_confidence': avg_conf
        }
    
    return output