from flask import Flask, render_template, request, jsonify
import os
import time

from detect import detect_objects
from database import create_scan, save_detection, get_all_scans


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    
    print("💥 ANALYZE ROUTE WAS CALLED...")
    
    start = time.time() 
    
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)
    
    print('IMAGE SAVED:', time.time() -start)
    
    detections = detect_objects(filepath)
    
    print("YOLO DONE:", time.time() - start)
    #create one scan for this image       
    scan_id = create_scan("CAMERA_A1", "SHELF_A1")
    
    #save each detected object under this scan
    for class_name, data in detections.items():
       save_detection(
              scan_id,
              class_name,
              data['count'],
              data['avg_confidence']
       )
    
    print("DATABASE DONE:", time.time() - start)
    print("TOTAL TIME TAKEN:", time.time() - start)
    
    return jsonify({
        "status": "success",
        "scan_id": scan_id,
        "detections": detections
    })
       
@app.route('/history', methods = ['GET'])
def history():
    # Implement history retrieval logic here
    
    rows = get_all_scans()
    
    data = []
    
    for row in rows:
        data.append({
            "scan_id": row[0],
            "timestamp": row[1],
            "camera_id": row[2],
            "shelf_id": row[3],
            "class_name": row[4],
            "count": row[5],
            "avg_confidence": row[6]
        })
        
    return jsonify({"history": data})
    

if __name__ == '__main__':
    app.run(debug=True)