from flask import Flask, jsonify
import subprocess, os, sys

app = Flask(__name__)

# Attendance alma komutu
@app.route('/take_attendance', methods=['GET'])
def take_attendance():
    try:
        # Start face recognition script and wait for it to close
        python_executable = sys.executable
        process = subprocess.Popen([python_executable, "face_recognition_attendance.py"], shell=True)
        process.wait()  # Wait for the user to close the face recognition app

        # After closing, run export_attendance.py
        export_process = subprocess.run([python_executable, "export_attendance.py"], capture_output=True, text=True)

        return jsonify({"message": "Attendance taken and exported!", "export_output": export_process.stdout})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Attendance raporunu al
@app.route('/get_attendance_report', methods=['GET'])
def get_attendance_report():
    try:
        with open("attendance_report.csv", "r", encoding="utf-8") as file:
            data = file.read()
        return jsonify({"report": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_students', methods=['GET'])
def get_students():
    faces_dir = "faces"
    students = []

    if not os.path.exists(faces_dir):
        return jsonify({"error": "Faces directory not found"}), 404  # JSON hata döndür

    for filename in os.listdir(faces_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            absolutePath = os.path.abspath(faces_dir)
            name_parts = filename.rsplit('.', 1)[0].split('_')
            if len(name_parts) == 2:
                first_name = name_parts[0]
                last_name = name_parts[1]
            else:
                first_name = name_parts[0]
                last_name = ""

            students.append({
                "first_name": first_name.capitalize(),
                "last_name": last_name.capitalize(),
                "photo_url": f"{absolutePath}/{filename}"
            })

    return jsonify(students)

@app.route('/encode_faces', methods=['GET'])
def encode_faces():
    try:
        python_executable = sys.executable
        process = subprocess.run([python_executable, "encode_faces.py"], capture_output=True, text=True)
        
        if process.returncode != 0:
            return jsonify({"error": process.stderr}), 500
        
        return jsonify({"message": "Face encoding completed!", "output": process.stdout})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)