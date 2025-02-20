dont forget to work in a venv

libraries
----------
cmake 
dlib
face_recognition
face_recognition_models 
opencv-python
pandas
os
numpy
python3 -m venv face_recognition_env        //creates venv
pip install --upgrade setuptools            //after create
pip install flask
pip install fer==22.4.0
pip install face_recognition_models
python face_recognition_attendance.py
activate/ deactivate                        //enables or disables venv
face_recognition_env/Scripts/activate       //if activate does not work

execution codes
----------------
1- add faces manually to the faces folder
2- run encode_faces.py                      //python encode_faces.py
3- run face_recognition_attendance.py       //python face_recognition_attendance.py
4- to export the attendance list,           //python export_attendance.py
run export_attendance.py
5- run server.py before building website    // python server.py