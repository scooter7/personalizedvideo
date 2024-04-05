import streamlit as st
import pandas as pd
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import os
import tempfile  # Import tempfile to create temporary files

st.title("Video Personalization App")

# File uploaders
video_file = st.file_uploader("Choose a video file", type=["mp4"])
csv_file = st.file_uploader("Choose a CSV file")

if video_file is not None and csv_file is not None:
    # Read CSV file
    df = pd.read_csv(csv_file)
    first_names = df['FirstName'].tolist()

    # Temporary directory to save personalized videos
    if not os.path.exists('temp_videos'):
        os.makedirs('temp_videos')

    # Save the uploaded video file to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video_file:
        temp_video_file.write(video_file.getvalue())
        temp_video_path = temp_video_file.name  # This is the path to the temporary file

    with st.spinner('Processing videos... Please wait.'):
        for name in first_names:
            # Load the video file from the temporary file
            clip = VideoFileClip(temp_video_path)
            
            # Create a text clip
            txt_clip = TextClip(f"{name}, please enroll at ABC College", fontsize=24, color='white')
            txt_clip = txt_clip.set_position('center').set_duration(10)
            
            # Overlay the text on the original video clip
            video = CompositeVideoClip([clip, txt_clip])
            
            # Output file name
            output_filename = f"temp_videos/personalized_{name}.mp4"
            
            # Write the result to a file
            video.write_videofile(output_filename, codec="libx264", fps=24)

        # Optionally, delete the temporary video file if it's no longer needed
        os.unlink(temp_video_path)

    st.success('Videos processed successfully!')

    # Provide download links
    for name in first_names:
        output_filename = f"temp_videos/personalized_{name}.mp4"
        with open(output_filename, "rb") as file:
            st.download_button(
                label=f"Download {name}'s Video",
                data=file,
                file_name=output_filename,
                mime="video/mp4"
            )
