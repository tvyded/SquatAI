from flask import Flask, render_template, Response, jsonify
import cv2
from squat_tracker import SquatTracker
from deadlift_tracker import DeadliftTracker

app = Flask(__name__)

squat_tracker = SquatTracker()
deadlift_tracker = DeadliftTracker()

# ---- Приседания ----
def generate_squat_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        processed_frame = squat_tracker.process_frame(frame)
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/squat')
def squat():
    return render_template('squat.html')

@app.route('/squat_video_feed')
def squat_video_feed():
    return Response(generate_squat_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/squat_stats')
def squat_stats():
    return jsonify(squat_tracker.get_stats())

@app.route('/squat_reset')
def squat_reset():
    squat_tracker.reset()
    return jsonify(squat_tracker.get_stats())

# ---- Становая тяга ----
def generate_deadlift_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        processed_frame = deadlift_tracker.process_frame(frame)
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    cap.release()

@app.route('/deadlift')
def deadlift():
    return render_template('deadlift.html')

@app.route('/deadlift_video_feed')
def deadlift_video_feed():
    return Response(generate_deadlift_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/deadlift_stats')
def deadlift_stats():
    return jsonify(deadlift_tracker.get_stats())

@app.route('/deadlift_reset')
def deadlift_reset():
    deadlift_tracker.reset()
    return jsonify(deadlift_tracker.get_stats())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)