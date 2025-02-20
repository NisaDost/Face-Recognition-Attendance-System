import face_recognition
import os
import pickle
import cv2
import numpy as np
from fer import FER
import csv
from datetime import datetime

def encode_faces(image_folder='faces'):
    known_encodings = []
    known_names = []
    for filename in os.listdir(image_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(image_folder, filename)
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            known_encodings.append(encoding)
            known_names.append(os.path.splitext(filename)[0])
    return known_encodings, known_names

def recognize_faces(video_source=0):
    known_encodings, known_names = encode_faces()
    emotion_detector = FER()
    
    video_capture = cv2.VideoCapture(video_source)
    
    attendance = set()
    
    if not os.path.exists('emotion_results.csv'):
        with open('emotion_results.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Name", "Emotion"])
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"
            
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
            
            if name != "Unknown" and name not in attendance:
                attendance.add(name)
                
                face_crop = frame[top:bottom, left:right]
                emotion_result = emotion_detector.detect_emotions(face_crop)
                emotion = "No Face Detected"
                
                if emotion_result:
                    dominant_emotion = max(emotion_result[0]['emotions'], key=emotion_result[0]['emotions'].get)
                    emotion = dominant_emotion
                
                with open('emotion_results.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, emotion])
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, f"{name}: {emotion}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces()
