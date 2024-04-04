import streamlit as st
import pandas as pd
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
import tempfile

st.title("Video Personalization App")

video_file = st.file_uploader("Choose a video file", type=["mp4"])
csv_file = st.file_uploader("Choose a CSV file")

if video_file is not None and csv_file is not None:
    df = pd.read_csv(csv_file)
    first_names = df['FirstName'].tolist()

    if not os.path.exists('temp_videos'):
        os.makedirs('temp_videos')

    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
        temp_video.write(video_file.getvalue())
        temp_video_path = temp_video.name

    with st.spinner('Processing videos... Please wait.'):
        for name in first_names:
            clip = VideoFileClip(temp_video_path)
            txt_clip = TextClip(f"{name}, please enroll at ABC College", fontsize=24, color='white')
            txt_clip = txt_clip.set_position('center').set_duration(10)
            video = CompositeVideoClip([clip, txt_clip])
            output_filename = f"temp_videos/personalized_{name}.mp4"
            video.write_videofile(output_filename, codec="libx264", fps=24)

    st.success('Videos processed successfully!')

    for name in first_names:
        output_filename = f"temp_videos/personalized_{name}.mp4"
        with open(output_filename, "rb") as file:
            st.download_button(
                label=f"Download {name}'s Video",
                data=file,
                file_name=output_filename,
                mime="video/mp4"
            )
