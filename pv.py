import streamlit as st
import pandas as pd
import cv2
import numpy as np
import tempfile
import os
from moviepy.editor import AudioFileClip

st.title("Video Personalization App")

video_file = st.file_uploader("Choose a video file", type=["mp4"])
csv_file = st.file_uploader("Choose a CSV file")

if video_file and csv_file:
    df = pd.read_csv(csv_file)
    first_names = df['FirstName'].tolist()

    with tempfile.NamedTemporaryFile(delete=True, suffix='.mp4') as tmp:
        tmp.write(video_file.getvalue())
        video_path = tmp.name

        for name in first_names:
            cap = cv2.VideoCapture(video_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            output_filename = f"personalized_{name}.mp4"
            out = cv2.VideoWriter(output_filename, fourcc, fps, (640, 360))  # Reduced frame size

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.resize(frame, (640, 360))  # Resize frame
                # Add text to frame here as before
                
                out.write(frame)

            cap.release()
            out.release()

            # Attach audio using moviepy
            final_output_filename = f"final_{output_filename}"
            clip = AudioFileClip(video_path)
            clip.write_audiofile(final_output_filename, codec='aac')
            
            # Provide download link for final video
            # Similar to before, but using `final_output_filename`
            
            os.remove(output_filename)  # Cleanup immediately after use

# Note: Detailed audio handling is simplified for brevity; adjust as per your specific requirements.
