import face_recognition
import os
import pickle

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

known_encodings, known_names = encode_faces()
with open('encodings.pkl', 'wb') as f:
    pickle.dump((known_encodings, known_names), f)
