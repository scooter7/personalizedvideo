import streamlit as st
import pandas as pd
import cv2
import numpy as np
import tempfile
import os
from moviepy.editor import AudioFileClip, VideoFileClip

st.title("Video Personalization App")

# Initialize session state variables if they don't exist
if 'processing_done' not in st.session_state:
    st.session_state.processing_done = False

video_file = st.file_uploader("Choose a video file", type=["mp4"])
csv_file = st.file_uploader("Choose a CSV file")

# Button to start processing
start_processing = st.button('Start Processing')

if start_processing:
    st.session_state.processing_done = False  # Reset the flag when button is pressed

if video_file and csv_file and not st.session_state.processing_done:
    df = pd.read_csv(csv_file)
    first_names = df['FirstName'].tolist()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(video_file.getvalue())
        video_path = tmp.name

    original_clip = VideoFileClip(video_path)
    audio = original_clip.audio

    for name in first_names:
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        temp_video_path = tempfile.mktemp(suffix='.mp4')
        out = cv2.VideoWriter(temp_video_path, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f"{name}, please enroll at ABC College"
            text_position = (50, height - 50)
            font_scale = 1
            font_color = (255, 255, 255)
            line_type = 2

            cv2.putText(frame, text, text_position, font, font_scale, font_color, line_type)
            out.write(frame)

        cap.release()
        out.release()

        processed_clip = VideoFileClip(temp_video_path)
        final_clip = processed_clip.set_audio(audio)
        final_output_filename = f"personalized_{name}.mp4"
        final_clip.write_videofile(final_output_filename, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)

        with open(final_output_filename, "rb") as file:
            st.download_button(f"Download {name}'s Video", file, file_name=final_output_filename, mime="video/mp4")

        os.remove(temp_video_path)
        os.remove(final_output_filename)

    os.unlink(video_path)
    st.session_state.processing_done = True  # Set flag to True after processing
