# Smart Fitness Trainer App

A Flutter application that uses computer vision and machine learning to detect and analyze workout exercises in real-time.

## Features
- Real-time workout detection using device camera
- Video upload and analysis
- Support for multiple workout types (squats, bicep curls, etc.)
- FastAPI backend for processing and analysis

## Project Structure
- `fitness_trainer_app/`: Flutter application
- `Smart_Fitness_Trainer_project/`: Backend server and ML model

## Setup Instructions

### Backend Setup
1. Navigate to `Smart_Fitness_Trainer_project`
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server:
   ```bash
   python backend.py
   ```

### Flutter App Setup
1. Navigate to `fitness_trainer_app`
2. Install dependencies:
   ```bash
   flutter pub get
   ```
3. Run the app:
   ```bash
   flutter run
   ```

## Requirements
- Python 3.8+
- Flutter SDK
- Android Studio
- Android SDK
- Required Python packages (see requirements.txt)

## Team Members
[Add your team members here]

## License
[Add your license information here]

# Smart Fitness Assistant

## Overview
The **Smart Fitness Assistant** is designed to enhance workout experiences by providing real-time feedback and performance tracking. The project flow consists of some features described as follows :

## Key Features
- **Exercise Detection:** The assistant identifies the current workout being performed by the user.
- **Body Orientation Detection:** It then assesses the user's body orientation to ensure proper form and alignment.
- **Repetition Counting:** The system counts the number of repetitions completed for each exercise.
- **Feedback Generation:** Finally, it delivers feedback to the user based on their performance, helping to improve technique and efficiency.
This comprehensive approach aims to support users in achieving their fitness goals while maintaining proper form and reducing the risk of injury.


## Features Descriptions
This section is to explain how each feature works to provide real-time feedback and assistance during your workouts.


### 1) Exercise Detection

The workout detection system is built through a structured process of data collection, processing, and model training, resulting in high-accuracy predictions. Here's an overview of how this feature works:

1. **Data Collection**: We began by collecting videos for four workout classes (biceps, squats, pushups, and a neutral state) and we have collected data as follows:
<div align="center">

| Exercise           | Total Videos         | Video Duration        | Frame Rates          |
|--------------------|----------------------|-----------------------|----------------------|
| Squats             | 45                   | 3 to 10 seconds       | 25-30 fps            |
| Bicep-Curls        | 47                   | 3 to 10 seconds       | 25-30 fps            |
| Neutral            | 246                  | 1 to 3 seconds        | 25 fps               |
| Push-Ups           | 53                   | 2 to 4 seconds        | 22-25 fps            |

</div>


2. **Keypoint Extraction**: Using the Mediapipe library, we extracted keypoints from the collected videos.

3. **Data Preparation**: The extracted keypoints were saved into a CSV file, which was then split into training and validation sets using an 80:20 ratio.

4. **Data Scaling**: To ensure consistency and improve the performance of the machine learning model, the keypoint data was scaled using a Standard Scaler.

5. **Model Training**: We employed a Random Forest model, which is known for its robustness and accuracy. The model was trained on the scaled keypoint data, achieving an impressive accuracy of 99.26%.

6. **Result**: With this trained model, the system can accurately detect the workout being performed by the user in real time.

<div align="center">
  <img src="Smart_Fitness_Trainer_project/Project_Results/Random_forest_confusion_matrex.jpg" alt="Image 1" style="width: 45%; display: inline-block; margin right: 5%;" />
  <img src="Smart_Fitness_Trainer_project/Project_Results/RF_action_detection_results.jpg" alt="Image 2" style="width: 45%; display: inline-block;" />
</div>


### 2) Body Orientation

The orientation of the body is determined by calculating the ratio between two distances:
1. **Distance between the shoulder points (left and right shoulder)**.
2. **Distance between the shoulder and elbow on the most visible side**.

If the ratio is greater than **0.6**, the system detects the body as being **front-facing**. Otherwise, it is classified as a **side view**. The side is determined based on the most visible body points from the side.

<div align="center">
  <img src="Smart_Fitness_Trainer_project/Project_Results/front_orientation_results-ezgif.com-video-to-gif-converter.gif" width="320" height="240"/>
  <img src="Smart_Fitness_Trainer_project/Project_Results/side_orientation-ezgif.com-video-to-gif-converter.gif" width="320" height="240"/>
</div>


### 3) Repetition Count

The repetition counting feature is built upon a state-based logic system, which ensures accuracy by monitoring the specific phases of each exercise. For instance, the squat workout consists of three main states:

1. **Standing (S1)**: The starting position where the user stands upright.
2. **Lowering (S2)**: The phase where the user descends into the squat position.
3. **Bottom (S3)**: The lowest point of the squat before returning to standing.

To count a valid repetition, all three states must occur sequentially: the user must start from the standing position (S1), move into the lowering position (S2), and reach the bottom position (S3). If any of these states are missed or not completed in the correct order, the repetition count is deemed inaccurate, prompting feedback to the user.

This logic applies to other workouts as well, with each exercise having its specific states defined to ensure accurate counting and feedback. The following diagram illustrates the state transitions for the squat exercise:

<div align="center">
  <img src="Smart_Fitness_Trainer_project/Project_Results/counting logic.png" alt="Repetition Count States" width="400"/>
</div>


### 4) Realtime Feedback
Each exercise is associated with common problems that can hinder effectiveness and potentially lead to injury. By utilizing MediaPipe, we can accurately analyze the user's movements and detect these issues.

#### Common Problems Detected:

1. **Squats:**
   - **Knees Caving In:** This occurs when the knees move inward during the squat, which can lead to joint strain.
   - **Insufficient Depth:** Failing to reach the proper depth can reduce the effectiveness of the squat.

2. **Push-Ups:**
   - **Incorrect Hand Placement:** Placing hands too wide or too narrow can alter the mechanics and effectiveness of the push-up.
   - **Sagging Hips:** Allowing the hips to sag towards the ground can strain the lower back.

3. **Biceps Curls:**
   - **Swinging the Body:** Using momentum instead of muscle strength to lift the weights can diminish the workout's effectiveness.
   - **Incomplete Range of Motion:** Not fully extending or flexing the arms can reduce muscle engagement.

#### Feedback Mechanism:
Using MediaPipe's pose estimation capabilities, the Smart Fitness Assistant continuously monitors the user's form during exercises. When a common problem is detected, the system provides immediate feedback, guiding users on how to correct their movements. This not only helps in improving performance but also promotes safe workout practices.

By addressing these common issues in real-time, users can achieve their fitness goals more effectively while minimizing the risk of injury.


# Here is sample output 

<p align="center">
  <img src="Smart_Fitness_Trainer_project/Project_Results/full_project_results.gif" width="400"/>
</p>


