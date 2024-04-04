import cv2
import pandas as pd
import streamlit as st
import tempfile
import os

# Streamlit file uploaders
source_video = st.file_uploader("Upload your source video", type=["mp4"])
csv_file = st.file_uploader("Upload your CSV file of names", type=["csv"])

if source_video and csv_file:
    # Temporarily save the uploaded video
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(source_video.read())
        video_path = tmp.name
    
    df = pd.read_csv(csv_file)
    names = df['FirstName'].unique()

    for name in names:
        # Read the video file
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
        output_path = f"{name}_personalized.mp4"
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Put text on the frame
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, f"Hello, {name}!", (50, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Write the frame with text
            out.write(frame)

        # Release everything if job is finished
        cap.release()
        out.release()

        # Provide download link
        with open(output_path, 'rb') as f:
            st.download_button(f"Download {name}'s Video", f, file_name=output_path, mime="video/mp4")

        # Optional: Remove the processed file to save space
        os.remove(output_path)

    # Cleanup: remove the source video temporary file
    os.remove(video_path)
