import cv2
import face_recognition
import pickle
import sqlite3
import numpy as np
from datetime import datetime, timedelta

# Load face encodings
with open('encodings.pkl', 'rb') as f:
    known_encodings, known_names = pickle.load(f)

# Load emotion detection model (OpenCV's pre-trained DNN model)
emotion_model = cv2.dnn.readNetFromONNX("emotion-ferplus-8.onnx")

# Emotion labels (FERPlus Model)
emotion_labels = ["Neutral", "Happy", "Sad", "Surprise", "Angry", "Disgust", "Fear", "Contempt"]

def mark_attendance(name):
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (name, date, time) VALUES (?, ?, ?)", (name, date, time))
    conn.commit()
    conn.close()

    print(f"Marked attendance for {name} at {time} on {date}")

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Store last attendance mark time
last_mark_time = {}

while True:
    ret, frame = video_capture.read()
    if not ret:
        print("Failed to capture frame")
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        # Get best match
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances) if any(matches) else None
        if best_match_index is not None and matches[best_match_index]:
            name = known_names[best_match_index]

            # Mark attendance every 30 seconds
            now = datetime.now()
            if name not in last_mark_time or (now - last_mark_time[name]) > timedelta(seconds=30):
                mark_attendance(name)
                last_mark_time[name] = now

        # Extract face ROI for emotion detection
        top, right, bottom, left = face_location
        face_roi = frame[top:bottom, left:right]

        if face_roi.size > 0:
            gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
            resized_face = cv2.resize(gray_face, (64, 64))  # Resize to match model input

            # Prepare image for model (Normalize & Reshape)
            blob = cv2.dnn.blobFromImage(resized_face, scalefactor=1/255.0, size=(64, 64))
            emotion_model.setInput(blob)
            emotion_preds = emotion_model.forward()

            # Get emotion with highest confidence
            emotion_index = np.argmax(emotion_preds)
            emotion = emotion_labels[emotion_index]

        else:
            emotion = "Neutral"

        # Draw face rectangle & put text
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} ({emotion} + {face_roi.size})", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Face Recognition & Emotion Analysis', frame)

    # Check for exit condition
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Check if the window is still open before checking properties
    if cv2.getWindowProperty('Face Recognition & Emotion Analysis', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()
