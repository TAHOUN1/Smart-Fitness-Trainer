# import streamlit as st
# import tempfile
# import os
# from Feedback import*
# from gym_functions import*

# # Streamlit UI
# st.title("AI Trainer App")
# st.write("Upload a video file to process and get feedback")

# # Upload video file
# uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"])

# if uploaded_file is not None:
#     # Save uploaded file to a temporary location
#     temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
#     temp_video.write(uploaded_file.read())
#     temp_video.flush()  # Ensure the content is fully written before further processing
#     temp_video.close()  # Close the temp file so it can be accessed by other processes

#     # Display uploaded video
#     st.video(temp_video.name)

#     # Process the video and get workout data
#     st.write("Processing video...")
#     output_video_path,counters, workout_class, errors = release_assistant(temp_video.name)

#     # Initialize video capture to replay the video with feedback
#     cap = cv2.VideoCapture(temp_video.name)

#     # Create a temporary file to save the processed video with feedback (using a browser-compatible format)
#     output_video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You may want to use 'avc1' codec for compatibility
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

#     # Process each frame of the video
#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             break  # Exit the loop if the video ends

#         # Write the frame without drawing feedback (only video processing here)
#         out.write(frame)

#     cap.release()
#     out.release()

#     # Reopen the processed video file to display it
#     with open(output_video_path, 'rb') as video_file:
#         st.video(video_file)

#     # Generate and display structured feedback using the function output
#     feedback_text = provide_feedback(workout_class, errors, counters)

#     # Check if feedback_text is valid and convert it to a structured format
#     if feedback_text:
#         if isinstance(feedback_text, (list, tuple)):
#             # Join list/tuple elements into a structured string
#             feedback_text = "\n".join([f"{i+1}. {item}" for i, item in enumerate(feedback_text)])
#         elif isinstance(feedback_text, dict):
#             # Join dict elements into a structured string
#             feedback_text = "\n".join([f"{key}: {value}" for key, value in feedback_text.items()])
#         else:
#             # Display the feedback text as is
#             feedback_text = str(feedback_text)

#         # Display the structured feedback
#         st.write("*** Workout Feedback ***")
#         st.text(feedback_text)
#     else:
#         st.write("No feedback available")

#     # Clean up temporary files after displaying them
#     if os.path.exists(temp_video.name):
#         os.remove(temp_video.name)  # Ensure the file is not in use before deleting

#     if os.path.exists(output_video_path):
#         os.remove(output_video_path)  # Clean up the output video file as well


import streamlit as st
import tempfile
import os
from Feedback import*
from gym_functions import*

# Streamlit UI
st.title("AI Trainer App")
st.write("Upload a video file to process and get feedback")

# Upload video file
uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    # Save uploaded file to a temporary location
    temp_video = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    temp_video.write(uploaded_file.read())
    temp_video.flush()  # Ensure the content is fully written before further processing
    temp_video.close()  # Close the temp file so it can be accessed by other processes

    # Display uploaded video
    st.video(temp_video.name)

    # Create a placeholder for real-time video processing display
    st.write("Processing video in real-time...")
    st_frame_placeholder = st.empty()  # This placeholder will update the frame in real-time

    # Process the video and get workout data
    counters, workout_class, errors = release_assistant(temp_video.name, st_frame_placeholder)

    # Generate and display structured feedback using the function output
    feedback_text = provide_feedback(workout_class, errors, counters)

    # Check if feedback_text is valid and convert it to a structured format
    if feedback_text:
        if isinstance(feedback_text, (list, tuple)):
            # Join list/tuple elements into a structured string
            feedback_text = "\n".join([f"{i+1}. {item}" for i, item in enumerate(feedback_text)])
        elif isinstance(feedback_text, dict):
            # Join dict elements into a structured string
            feedback_text = "\n".join([f"{key}: {value}" for key, value in feedback_text.items()])
        else:
            # Display the feedback text as is
            feedback_text = str(feedback_text)

        # Display the structured feedback
        st.write("*** Workout Feedback ***")
        st.text(feedback_text)
    else:
        st.write("No feedback available")

    # Clean up temporary files after displaying them
    if os.path.exists(temp_video.name):
        os.remove(temp_video.name)  # Ensure the file is not in use before deleting
