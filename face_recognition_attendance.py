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

def mark_attendance(name, emotion):
    now = datetime.now()
    date = now.strftime('%Y-%m-%d')
    time = now.strftime('%H:%M:%S')

    conn = sqlite3.connect('attendance.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO attendance (name, date, time, emotion) VALUES (?, ?, ?, ?)", (name, date, time, emotion))
    conn.commit()
    conn.close()

    print(f"Marked attendance for {name} at {time} on {date}. Emotion: {emotion}")

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

        # Extract face ROI for emotion detection
        top, right, bottom, left = face_location
        face_roi = frame[max(0, top):min(bottom, frame.shape[0]), max(0, left):min(right, frame.shape[1])]

        if face_roi is not None and face_roi.size > 0:
            # Ensure ROI bounds are valid
            face_roi = frame[max(0, top):min(bottom, frame.shape[0]), max(0, left):min(right, frame.shape[1])]

            # Convert to grayscale (FERPlus expects single-channel input)
            gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

            # Resize to match model input (64x64)
            resized_face = cv2.resize(gray_face, (64, 64))

            # Convert to float32 (but keep range 0-255)
            processed_face = resized_face.astype(np.float32)*3  # No division by 255

            # Convert to blob for ONNX model
            blob = cv2.dnn.blobFromImage(processed_face, scalefactor=1.0, size=(64, 64), mean=0, swapRB=False, crop=False)

            # Reshape if necessary (model may expect 1x1x64x64)
            if blob.shape[1] == 1:
                blob = blob.reshape(1, 1, 64, 64)

            # Run emotion detection model
            emotion_model.setInput(blob)
            emotion_preds = emotion_model.forward()

            # Get emotion label with highest probability
            emotion_index = np.argmax(emotion_preds)
            emotion = emotion_labels[emotion_index]

            print(f"Detected Emotion: {emotion}")  # Debugging
        else:
            emotion = "Neutral"


        # Get best match
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = np.argmin(face_distances) if any(matches) else None
        if best_match_index is not None and matches[best_match_index]:
            name = known_names[best_match_index]

            # Mark attendance every 30 seconds
            now = datetime.now()
            if name not in last_mark_time or (now - last_mark_time[name]) > timedelta(seconds=30):
                mark_attendance(name, emotion)

                last_mark_time[name] = now
        # Draw face rectangle & put text
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, f"{name} ({emotion})", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

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
