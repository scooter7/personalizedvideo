import streamlit as st
import pandas as pd
import cv2
import numpy as np
import tempfile
import os
from moviepy.editor import AudioFileClip, VideoFileClip

st.title("Video Personalization App")

video_file = st.file_uploader("Choose a video file", type=["mp4"])
csv_file = st.file_uploader("Choose a CSV file")

if video_file and csv_file:
    # Read names from CSV
    df = pd.read_csv(csv_file)
    first_names = df['FirstName'].tolist()

    # Save the uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(video_file.getvalue())
        video_path = tmp.name  # Path to the temp video file

    # Extract audio from the original video
    original_clip = VideoFileClip(video_path)
    audio = original_clip.audio

    for name in first_names:
        # Initialize OpenCV VideoCapture
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # Define codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_video_path = tempfile.mktemp(suffix='.mp4')  # Temp file for video without audio
        out = cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Insert OpenCV text overlay operation here

            out.write(frame)

        # Cleanup
        cap.release()
        out.release()

        # Combine video with audio
        processed_clip = VideoFileClip(temp_video_path)
        final_clip = processed_clip.set_audio(audio)
        final_output_filename = f"personalized_{name}.mp4"
        final_clip.write_videofile(final_output_filename, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)

        # Provide download link
        with open(final_output_filename, "rb") as file:
            st.download_button(f"Download {name}'s Video", file, file_name=final_output_filename, mime="video/mp4")

        # Clean up temporary files
        os.remove(temp_video_path)
        os.remove(final_output_filename)

    # Remove the original temporary video file
    os.unlink(video_path)
