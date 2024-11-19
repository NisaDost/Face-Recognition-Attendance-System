dependencies:
---------------
dont forget to work in a venv


### MUST BE GLOBAL! |
------------------- v
cmake 
dlib

## either in venv or global |
--------------------------- v
face_recognition
face_recognition_models 
opencv-python
pandas

execution codes
---------------
python3 -m venv face_recognition_env        //creates venv
activate/ deactivate                        //enables or disables venv

1- add faces manually to the faces folder
2- run encode_faces.py                      //python encode_faces.py
3- run face_recognition_attendance.py       //python face_recognition_attendance.py
4- to export the attendance list,           //python export_attendance.py
run export_attendance.py