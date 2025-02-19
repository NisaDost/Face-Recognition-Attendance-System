from flask import Flask, jsonify
import subprocess, os

app = Flask(__name__)

# Attendance alma komutu
@app.route('/take_attendance', methods=['GET'])
def take_attendance():
    try:
        subprocess.run(["python", "face_recognition_attendance.py"])  # Python scriptini çalıştır
        return jsonify({"message": "Attendance alındı!"})
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

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)