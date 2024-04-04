import streamlit as st
import pandas as pd
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import tempfile
import os

# Upload CSV with names
df = pd.read_csv('people_videos.csv')  # This assumes the CSV is in the same directory as the app

# File uploader for the source video
source_video = st.file_uploader("Upload a source video", type=["mp4"])

if source_video is not None:
    # Use tempfile to create a temporary file on disk
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp:
        tmp.write(source_video.getvalue())
        source_video_path = tmp.name  # Path to the uploaded video file saved temporarily

    selected_name = st.selectbox('Select a name:', df['FirstName'])

    if selected_name:
        # Generate personalized video for the selected name
        output_filename = f'personalized_{selected_name}.mp4'
        output_filepath = os.path.join('temp_videos', output_filename)
        
        if not os.path.exists('temp_videos'):
            os.makedirs('temp_videos')

        if not os.path.exists(output_filepath):  # Check if the video was already generated
            # Load the base video from the temporary file
            clip = VideoFileClip(source_video_path)
            
            # Generate a text clip
            txt_clip = TextClip(f'Hello, {selected_name}!', fontsize=70, color='white', font='Arial-Bold')
            txt_clip = txt_clip.set_pos('center').set_duration(10)
            
            # Overlay the text on the base video
            video = CompositeVideoClip([clip, txt_clip.set_start(1).set_end(9)], size=clip.size)
            
            # Write the result to a file in the temp_videos directory
            video.write_videofile(output_filepath, codec='libx264', fps=24)

        # Provide a download link
        with open(output_filepath, 'rb') as file:
            st.download_button(
                label=f'Download video for {selected_name}',
                data=file,
                file_name=output_filename,
                mime='video/mp4'
            )
