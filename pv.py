import streamlit as st
import pandas as pd
from moviepy.config import change_settings
import os
import tempfile

# After setting the ImageMagick path, import VideoFileClip and other moviepy functionalities
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

st.title("Video Personalization App")

# File uploaders for video and CSV
video_file = st.file_uploader("Choose a video file", type=["mp4"])
csv_file = st.file_uploader("Choose a CSV file")

if video_file is not None and csv_file is not None:
    # Read CSV file
    df = pd.read_csv(csv_file)
    first_names = df['FirstName'].tolist()

    # Temporary directory to save personalized videos
    output_dir = 'temp_videos'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Process each name in the CSV
    with st.spinner('Processing videos... Please wait.'):
        # Save the uploaded video file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
            temp_video_file.write(video_file.getvalue())
            temp_video_path = temp_video_file.name  # Path to the temporary video file
        
        for name in first_names:
            # Create a personalized video for each name
            output_filename = os.path.join(output_dir, f"personalized_{name}.mp4")
            clip = VideoFileClip(temp_video_path)
            txt_clip = TextClip(f"{name}, please enroll at ABC College", fontsize=24, color='white', font="Arial-Bold", size=(clip.size[0],50)).set_pos('center').set_duration(10)
            video = CompositeVideoClip([clip, txt_clip.set_start(1).set_end(9)], size=clip.size)
            video.write_videofile(output_filename, codec="libx264", fps=24)
            
            # Provide download links
            with open(output_filename, "rb") as file:
                st.download_button(
                    label=f"Download {name}'s Video",
                    data=file,
                    file_name=f"personalized_{name}.mp4",
                    mime="video/mp4"
                )

        # Cleanup: Remove the temporary source video file
        os.unlink(temp_video_path)

    st.success('Videos processed successfully!')
