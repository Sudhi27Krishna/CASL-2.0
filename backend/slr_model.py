import cv2
import mediapipe as mp
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, lh, rh])

def sign_to_text():
    actions2 = np.array(['hello', 'how', 'you', 'good', 'morning', 'i', 'fine', 'what', 'your', 'name', 'hungry', 'want', 'water', 'my', 'a', 'n', 'very', 'cold', 'hot'])  #words nte list

    model_1 = Sequential()
    model_1.add(LSTM(units=128, return_sequences=True, activation='sigmoid', input_shape=(30, 258))) # 30 frames
    model_1.add(Dropout(0.2))
    model_1.add(LSTM(units=64, return_sequences=False))
    model_1.add(Dense(units=19, activation='softmax'))

    model_1.load_weights('new_model1.h5')

    sequence = []
    sentence = []
    threshold = 0.60

    cap = cv2.VideoCapture(0)
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while cap.isOpened():
            ret, frame = cap.read()
            image, results = mediapipe_detection(frame, holistic)
            draw_landmarks(image, results)
            image = cv2.flip(image, 1)
            keypoints = extract_keypoints(results)
            if np.all(keypoints[132:257] == 0):
                pass
            else:
                sequence.append(keypoints)
                sequence = sequence[-30:]

            if len(sequence) == 30:
                res1 = model_1.predict(np.expand_dims(sequence, axis=0))[0]
                print(actions2[np.argmax(res1)], max(res1))

                if res1[np.argmax(res1)] > threshold:
                    if len(sentence) > 0:
                        if actions2[np.argmax(res1)] != sentence[-1]:
                            sentence.append(actions2[np.argmax(res1)])
                    else:
                        sentence.append(actions2[np.argmax(res1)])

                if len(sentence) > 5:
                    sentence = sentence[-5:]

            cv2.rectangle(image, (0, 0), (640, 40), (245, 117, 16), -1)
            cv2.putText(image, ' '.join(sentence), (3, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # cv2.imshow('OpenCV Feed', image)
            yield image, sentence

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()