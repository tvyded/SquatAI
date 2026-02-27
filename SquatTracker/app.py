from flask import Flask, render_template, Response, jsonify
import cv2
from squat_tracker import SquatTracker

app = Flask(__name__)
tracker = SquatTracker()

def generate_frames():
    cap = cv2.VideoCapture(0)
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        processed_frame = tracker.process_frame(frame)
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    cap.release()

# МАРШРУТ ДЛЯ ГЛАВНОЙ СТРАНИЦЫ
@app.route('/')
def index():
    return render_template('index.html')

# МАРШРУТ ДЛЯ СТРАНИЦЫ ПРИСЕДАНИЙ
@app.route('/squat')
def squat():
    return render_template('squat.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/stats')
def get_stats():
    return jsonify(tracker.get_stats())

@app.route('/reset')
def reset():
    tracker.reset()
    return jsonify(tracker.get_stats())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)