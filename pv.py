import streamlit as st
import pandas as pd
import cv2
import numpy as np
import tempfile
import os
from moviepy.editor import VideoFileClip

st.title("Video Personalization App")

video_file = st.file_uploader("Choose a video file", type=["mp4"])
csv_file = st.file_uploader("Choose a CSV file")

if video_file and csv_file:
    df = pd.read_csv(csv_file)
    first_names = df['FirstName'].tolist()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(video_file.read())
        video_path = tmp.name

    original_clip = VideoFileClip(video_path)
    audio = original_clip.audio

    for name in first_names:
        cap = cv2.VideoCapture(video_path)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_filename = f"personalized_{name}.mp4"
        out = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f"{name}, please enroll at ABC College"
            textsize = cv2.getTextSize(text, font, 1, 2)[0]
            textX = (width - textsize[0]) // 2
            textY = (height + textsize[1]) // 2
            cv2.putText(frame, text, (textX, textY), font, 1, (255, 255, 255), 2)

            out.write(frame)

        cap.release()
        out.release()

        personalized_clip = VideoFileClip(output_filename)
        personalized_clip = personalized_clip.set_audio(audio)
        personalized_clip.write_videofile(f"final_{output_filename}", codec="libx264", audio_codec="aac")
        
        with open(f"final_{output_filename}", "rb") as file:
            st.download_button(
                label=f"Download {name}'s Video",
                data=file,
                file_name=f"final_{output_filename}",
                mime="video/mp4"
            )

        os.remove(output_filename)
        os.remove(f"final_{output_filename}")

    os.unlink(video_path)
