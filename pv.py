import streamlit as st
import pandas as pd
import cv2
import numpy as np
import tempfile
import os

st.title("Video Personalization App")

# File uploaders
video_file = st.file_uploader("Choose a video file", type=["mp4"])
csv_file = st.file_uploader("Choose a CSV file")

if video_file and csv_file:
    # Read CSV file
    df = pd.read_csv(csv_file)
    first_names = df['FirstName'].tolist()

    # Save the uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(video_file.read())
        video_path = tmp.name  # Temporary video file path

    # Process the video for each name
    with st.spinner('Processing videos... Please wait.'):
        for name in first_names:
            cap = cv2.VideoCapture(video_path)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # Define the codec and create VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'MP4V')
            output_filename = f"personalized_{name}.mp4"
            out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Place text on each frame
                font = cv2.FONT_HERSHEY_SIMPLEX
                text = f"{name}, please enroll at ABC College"
                textsize = cv2.getTextSize(text, font, 1, 2)[0]
                textX = (width - textsize[0]) // 2
                textY = (height + textsize[1]) // 2
                cv2.putText(frame, text, (textX, textY), font, 1, (255, 255, 255), 2)

                out.write(frame)

            cap.release()
            out.release()

            # Provide a download link for the processed video
            with open(output_filename, "rb") as file:
                st.download_button(
                    label=f"Download {name}'s Video",
                    data=file,
                    file_name=output_filename,
                    mime="video/mp4"
                )

            # Optionally, remove the processed video file to save space
            os.remove(output_filename)

    # Cleanup: Remove the temporary source video file
    os.unlink(video_path)
