from flask import request, jsonify
from config import app, socketio
from slr_model import sign_to_text
import cv2, json, re, os

def generate_frames_webcam():
    for result, sentence in sign_to_text():
        ref, buffer = cv2.imencode('.jpg', result)
        frame_bytes = buffer.tobytes()
        sentence_json = json.dumps(sentence)

        yield (frame_bytes, sentence_json)

def remove_punctuation(sentence):
    # Define a regex pattern to match punctuation characters
    punctuation_pattern = r'[^\w\s]'
    # Use re.sub() to replace punctuation characters with an empty string
    cleaned_sentence = re.sub(punctuation_pattern, '', sentence)
    return cleaned_sentence

def get_video_path(word_or_letter):
    video_file = f"videos\{word_or_letter}.mp4"  # Assuming the video files are named after the words or letters
    # video_path = os.path.join(video_folder, video_file)
    if os.path.exists(video_file):
        return f"{word_or_letter.upper()}.mp4"
    else:
        return None
    
def get_paths(sentence):
    video_paths = []
    for word in sentence.split():  # Split the sentence into words
        video_path = get_video_path(word)  # Retrieve video path for the word
        if video_path:
            video_paths.append(video_path)
        else:
            print(f"No video available for '{word}', displaying videos for each letter instead:")
            for letter in word:
                letter_video_path = get_video_path(letter)  # Retrieve video path for the letter
                if letter_video_path:
                    video_paths.append(letter_video_path)
                else:
                    print(f"No video available for '{letter}'")

    return video_paths

@app.route('/get-video-paths', methods=['POST'])
def send_voice_text_video_path():
    sentence = request.json.get('text')
    print(sentence)
    sentence = remove_punctuation(sentence)
    if(sentence):
        paths = get_paths(sentence)
        print(paths)
        if paths:
            return jsonify({'message': 'Paths sent successfully', 'paths': paths}), 200
        else:
            return jsonify({'message': 'No videos available to display', 'paths': []}), 404
    else:
        return jsonify({'message': 'Empty sentence', 'paths': []}), 400
    
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