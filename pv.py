from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import streamlit as st
import pandas as pd
import os
import tempfile

st.title("Personalized Video Generator")

source_video = st.file_uploader("Upload your source video", type=["mp4"])
csv_file = st.file_uploader("Upload your CSV file of names", type=["csv"])

if source_video and csv_file:
    # Read names from the uploaded CSV
    df = pd.read_csv(csv_file)
    names = df['FirstName'].unique()  # Assuming 'FirstName' column exists

    # Save the uploaded video to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(source_video.read())
        video_path = tmp.name

    for name in names:
        output_video_path = f"temp_{name}.mp4"

        clip = VideoFileClip(video_path)
        # Using default settings for TextClip to avoid triggering ImageMagick
        txt_clip = (TextClip(f"Hello, {name}!", fontsize=70, color='white')
                    .set_position("center")
                    .set_duration(10))
        
        video = CompositeVideoClip([clip, txt_clip])

        video.write_videofile(output_video_path, codec="libx264", fps=24)

        with open(output_video_path, 'rb') as file:
            st.download_button(f"Download {name}'s Video", file, file_name=output_video_path, mime="video/mp4")

        os.remove(output_video_path)  # Optional: Remove the file after downloading

    os.remove(video_path)  # Cleanup the temporary source video file
