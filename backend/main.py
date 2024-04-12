from flask import request, jsonify
from config import app, socketio
from slr_model import sign_to_text
import cv2, json

def generate_frames_webcam():
    for result, sentence in sign_to_text():
        ref, buffer = cv2.imencode('.jpg', result)
        frame_bytes = buffer.tobytes()
        sentence_json = json.dumps(sentence)

        yield (frame_bytes, sentence_json)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('request_frames_webcam')
def handle_request_frames():
    for frame_bytes, sentence_json in generate_frames_webcam():
        socketio.emit('update_frame', {'frame': frame_bytes, 'sentence': sentence_json})

if __name__ == "__main__":
    socketio.run(app, debug=True)