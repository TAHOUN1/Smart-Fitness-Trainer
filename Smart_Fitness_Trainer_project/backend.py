from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import tempfile
import os
import joblib
from gym_functions import workout_detection, extract_keypoints
import uvicorn
import mediapipe as mp

app = FastAPI()

# Add CORS middleware to allow requests from Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your Flutter app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MediaPipe pose detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Load the trained model and scaler
clf = joblib.load('workout_classifier_model.pkl')
scaler = joblib.load('scaler.pkl')

@app.post("/process-video")
async def process_video_endpoint(video: UploadFile = File(...)):
    # Create a temporary file to store the uploaded video
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        content = await video.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        # Initialize video capture
        cap = cv2.VideoCapture(temp_file_path)
        
        # Initialize counters and storage
        frames_counter = 0
        workout_for_Second = []
        current_workout = ['Neutral']
        
        # Process each frame
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            # Process the frame
            frame, frames_counter, workout_for_Second, current_workout = workout_detection(
                clf, scaler, frame, frames_counter, workout_for_Second, current_workout)
        
        # Return the final workout type
        return {"workout_type": current_workout[-1]}
    finally:
        # Clean up
        cap.release()
        os.unlink(temp_file_path)

@app.post("/process-frame")
async def process_frame_endpoint(frame: UploadFile = File(...)):
    # Create a temporary file to store the uploaded frame
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
        content = await frame.read()
        temp_file.write(content)
        temp_file_path = temp_file.name

    try:
        # Read the image using OpenCV
        frame = cv2.imread(temp_file_path)
        if frame is None:
            return {"error": "Failed to read image"}
        
        # Initialize counters and storage
        frames_counter = 0
        workout_for_Second = []
        current_workout = ['Neutral']
        
        # Process the frame
        frame, frames_counter, workout_for_Second, current_workout = workout_detection(
            clf, scaler, frame, frames_counter, workout_for_Second, current_workout)
        
        return {"workout_type": current_workout[-1]}
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 