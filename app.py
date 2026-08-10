from flask import Flask, render_template, request, jsonify
import os
import time

from detect import detect_objects
from database import save_detection

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
    
    for class_name, data in detections.items():
        save_detection(class_name, data['count'], data['avg_confidence'])
        
    print("DATABASE DONE:", time.time() - start)
    print("TOTAL TIME TAKEN:", time.time() - start)
        
    
    return jsonify({"status": "success", "detections": detections})


if __name__ == '__main__':
    app.run(debug=True)