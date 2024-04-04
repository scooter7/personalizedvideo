import cv2
import pandas as pd
import streamlit as st
import tempfile
import os

source_video = st.file_uploader("Upload your source video", type=["mp4"])
csv_file = st.file_uploader("Upload your CSV file of names", type=["csv"])

if source_video and csv_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp.write(source_video.read())
        video_path = tmp.name
    
    df = pd.read_csv(csv_file)
    names = df['FirstName'].unique()

    for name in names:
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = f"{name}_personalized.mp4"
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Parameters for text overlay adjusted for better visibility
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, f"Hello, {name}!", (50, height - 50), font, 1, (255, 255, 255), 3, cv2.LINE_AA)
            
            out.write(frame)

        cap.release()
        out.release()

        with open(output_path, 'rb') as f:
            st.download_button(f"Download {name}'s Video", f, file_name=output_path, mime="video/mp4")

        os.remove(output_path)

    os.remove(video_path)
