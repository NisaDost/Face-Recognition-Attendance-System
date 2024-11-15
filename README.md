# Face Recognition Attendance System

This project is a Face Recognition Attendance System built with Python. The system uses OpenCV and the `face_recognition` library to recognize faces through a webcam and mark attendance in a local database. It is an ideal application for real-time attendance monitoring in schools, workplaces, and events.

## Features

- **Face Recognition**: Detects and recognizes faces in real time using a webcam.
- **Attendance Logging**: Records the name, date, and time of recognized faces in an SQLite database.
- **Data Export**: Attendance data can be exported to a CSV file for easy viewing and analysis.

## Technologies Used

- **Python**: Main programming language.
- **OpenCV**: For video capture and image processing.
- **face_recognition**: For facial detection and recognition.
- **SQLite**: Local database for storing attendance records.
- **pandas**: For exporting attendance records to CSV.

## Prerequisites

- **Python 3.x** installed on your system.
- **CMake** (required to install `dlib`, which is a dependency of `face_recognition`).

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/face-recognition-attendance-system.git
   cd face-recognition-attendance-system


2. **Create a Virtual Environment**:
  ```bash
  python3 -m venv face_recognition_env
  source face_recognition_env/bin/activate
  ```

3. **Install Required Packages**:
- First, ensure **CMake** is installed on your system:
  ```bash
  brew install cmake
  ```
- Then, install the necessary Python packages:
  ```bash
  pip install face_recognition opencv-python pandas
  ```

4. **Set Up Database**:
- Run the `setup_database.py` script to create the SQLite database:
  ```bash
  python setup_database.py
  ```

5. **Create a Folder for Face Images**:
- In the project directory, create a folder named `faces`. This folder will store images of individuals to be recognized.
  ```bash
  mkdir faces
  ```

6. **Encode Face Images**:
- Place images of the individuals in the `faces` folder. Ensure each image file is named with the person's name (e.g., `John_Doe.jpg`).
- Run the encoding script to generate facial encodings:
  ```bash
  python encode_faces.py
  ```

## Usage

### Run the Attendance System
- Start the face recognition and attendance logging system by running:
  ```bash
  python face_recognition_attendance.py
  ```

### Mark Attendance
- The system will detect faces and display the recognized names on the screen. If a person is recognized, their attendance (name, date, and time) is automatically logged in the `attendance.db` SQLite database.

### Export Attendance Records
- To export attendance records to a CSV file, run:
  ```bash
  python export_attendance.py
  ```
- This will create an `attendance_report.csv` file with all attendance records.

## Project Structure

```plaintext
├── faces                    # Folder containing images of individuals
├── attendance.db            # SQLite database storing attendance records
├── encodings.pkl            # File with precomputed face encodings
├── face_recognition_attendance.py  # Main script for face recognition and attendance logging
├── encode_faces.py          # Script to encode faces from images in 'faces' folder
├── setup_database.py        # Script to set up the SQLite database
├── export_attendance.py     # Script to export attendance records to CSV
├── README.md                # Project documentation
```

## Troubleshooting

- **Camera Access Issue**: Ensure the Terminal or IDE has camera access in **System Preferences** > **Security & Privacy** > **Camera** on macOS.
- **dlib Installation Issues**: Make sure CMake is installed. You can install it with `brew install cmake`.

## Future Improvements

- **Real-time Notification**: Add a feature to send notifications for marked attendance.
- **Face Registration**: Allow adding new faces directly through the webcam.
- **Web Interface**: Develop a web interface for easier access and management of attendance data.

## License

This project is open-source and available under the MIT License.

## Acknowledgements

- This project uses the [face_recognition](https://github.com/ageitgey/face_recognition) library by Adam Geitgey.
- Thanks to the OpenCV team for their powerful image processing library.

