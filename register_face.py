import face_recognition
import cv2
import numpy as np
import os

# Make sure the database directory exists
os.makedirs('database', exist_ok=True)

# Capture from webcam
video_capture = cv2.VideoCapture(0)
print("Capturing image... Please look at the camera.")
ret, frame = video_capture.read()
video_capture.release()

if not ret:
    print("Failed to capture image.")
    exit()

# Convert and detect face
rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
face_locations = face_recognition.face_locations(rgb_frame)
face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

if face_encodings:
    encoding = face_encodings[0]
    name = input("Enter your name: ")
    encodings_data = {'encodings': [encoding], 'names': [name]}

    np.save('database/encodings.npy', encodings_data)
    print(f"Face encoding saved successfully for {name}!")
else:
    print("No face detected. Try again in good lighting.")
