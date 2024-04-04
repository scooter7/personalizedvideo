import streamlit as st
import pandas as pd
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import tempfile
import os

# Title
st.title("Personalized Video Generator")

# File uploaders for the source video and CSV file
source_video = st.file_uploader("Upload your source video", type=["mp4"])
csv_file = st.file_uploader("Upload your CSV file of names", type=["csv"])

# Directory for processed videos (ensure this exists or create it)
output_dir = "processed_videos"
os.makedirs(output_dir, exist_ok=True)

if source_video and csv_file:
    # Temporary storage for the uploaded video
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(source_video.read())
        video_path = tmp.name  # Path to the uploaded video file saved temporarily
    
    # Read names from the uploaded CSV
    df = pd.read_csv(csv_file)
    # Assuming there's a column named 'FirstName' in the CSV
    names = df['FirstName'].unique()  # Process each name once

    # Process each name
    for name in names:
        output_video_path = os.path.join(output_dir, f"{name}_personalized.mp4")
        
        # Check if the video already exists to avoid reprocessing
        if not os.path.exists(output_video_path):
            clip = VideoFileClip(video_path)
            txt_clip = TextClip(f"Hello, {name}!", fontsize=70, color='white', font="Arial-Bold", size=clip.size).set_duration(clip.duration).set_position("center").set_opacity(0.5)
            final_clip = CompositeVideoClip([clip, txt_clip])
            final_clip.write_videofile(output_video_path, codec="libx264", fps=24)
        
        # Provide download link for the processed video
        with open(output_video_path, "rb") as file:
            st.download_button(label=f"Download video for {name}", data=file, file_name=f"{name}_personalized.mp4", mime="video/mp4")

    # Cleanup: Remove the temporary uploaded video file
    os.unlink(video_path)
