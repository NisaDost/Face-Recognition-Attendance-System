import cv2
import face_recognition
import pickle
import sqlite3
from datetime import datetime, timedelta

# Load face encodings
with open('encodings.pkl', 'rb') as f:
    known_encodings, known_names = pickle.load(f)

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

# Initialize the last attendance mark time for each person
last_mark_time = {}

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        # Check for matches
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        best_match_index = face_distances.argmin() if matches.count(True) > 0 else None
        if best_match_index is not None and matches[best_match_index]:
            name = known_names[best_match_index]

            # Get current time and check last marked time for this person
            now = datetime.now()
            if name not in last_mark_time or (now - last_mark_time[name]) > timedelta(seconds=30):
                mark_attendance(name)
                last_mark_time[name] = now

        # Draw rectangle around the face
        top, right, bottom, left = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # Display the name below the face
        cv2.putText(frame, name, (left + 6, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Recognition Attendance System', frame)

    # Check for 'q' key press or window close event
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Face Recognition Attendance System', cv2.WND_PROP_VISIBLE) < 1:
        break

# Release resources
video_capture.release()
cv2.destroyAllWindows()