import streamlit as st
import yt_dlp
from moviepy.editor import AudioFileClip, concatenate_audioclips
import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import imageio_ffmpeg as ffmpeg

# Get the ffmpeg path from imageio-ffmpeg
ffmpeg_path = ffmpeg.get_ffmpeg_exe()

# Function to download YouTube audio
def download_youtube_audio(url_list):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio/video_%(index)s.%(ext)s',  # Template for the output file names
        'ffmpeg_location': ffmpeg_path  # Use the path provided by imageio-ffmpeg
    }

    if not os.path.exists('audio'):
        os.makedirs('audio')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for index, url in enumerate(url_list):
            try:
                ydl_opts['outtmpl'] = f'audio/video_{index}.%(ext)s'  # Update output template with index
                ydl = yt_dlp.YoutubeDL(ydl_opts)
                ydl.download([url])
            except yt_dlp.utils.DownloadError as e:
                st.error(f"Error downloading {url}: {str(e)}")
                continue


# Function to trim audio files
def trim_audio_files(directory, output_directory, duration=30):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.endswith(".mp3"):
            file_path = os.path.join(directory, filename)
            output_path = os.path.join(output_directory, filename)

            try:
                audio = AudioFileClip(file_path)
                trimmed_audio = audio.subclip(0, duration)
                trimmed_audio.write_audiofile(output_path)
                st.success(f"Trimmed {filename} and saved to {output_path}")
            except Exception as e:
                st.error(f"Error processing {filename}: {e}")

# Function to merge audio files
def merge_audio_files(input_directory, output_file):
    audio_clips = []
    for filename in os.listdir(input_directory):
        if filename.endswith(".mp3"):
            file_path = os.path.join(input_directory, filename)
            try:
                audio = AudioFileClip(file_path)
                audio_clips.append(audio)
                st.info(f"Loaded {filename}")
            except Exception as e:
                st.error(f"Error loading {filename}: {e}")

    if audio_clips:
        final_audio = concatenate_audioclips(audio_clips)
        final_audio.write_audiofile(output_file)
        st.success(f"All audio files merged into {output_file}")
    else:
        st.error("No audio files found to merge.")

# Function to zip the merged audio file
def zip_file(file_to_zip, zip_file_name):
    with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_to_zip, os.path.basename(file_to_zip))
        st.success(f"Zipped {file_to_zip} into {zip_file_name}")

# Function to send the final audio file via email
def send_email(to_email, subject, body, attachment_path, smtp_server, smtp_port, from_email, from_password):
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(part)
    else:
        st.error(f"Attachment file {attachment_path} not found.")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
            st.success(f"Email sent to {to_email}")
    except Exception as e:
        st.error(f"Error sending email: {e}")

# Streamlit app
st.title("YouTube Audio Processing")

# User inputs
num_videos = st.number_input("How many YouTube videos?", min_value=1, max_value=10, step=1)
urls = []
for i in range(num_videos):
    url = st.text_input(f"Enter YouTube URL #{i+1}", key=f"url_{i}")
    urls.append(url)

if st.button("Download and Process"):
    st.info("Downloading audio from YouTube videos...")
    download_youtube_audio(urls)
    
    input_directory = 'audio'
    output_directory = 'trimmed_audio'
    output_file = 'merged_audio.mp3'
    zip_file_name = 'merged_audio.zip'
    
    st.info("Trimming audio files...")
    trim_audio_files(input_directory, output_directory)
    
    st.info("Merging audio files...")
    merge_audio_files(output_directory, output_file)
    
    st.info("Zipping the merged audio file...")
    zip_file(output_file, zip_file_name)

    st.session_state['zip_file_name'] = zip_file_name  # Store in session state
    st.success("All operations completed!")

# Email sending section
st.header("Send the final audio file via email")
to_email = st.text_input("Recipient email address")
from_email = st.text_input("Your email address", value="your_email@gmail.com")
from_password = st.text_input("Your email password", type="password")
if st.button("Send Email"):
    zip_file_name = st.session_state.get('zip_file_name')  # Retrieve from session state
    if zip_file_name:
        subject = "Here is your merged audio file"
        body = "Please find the attached merged audio file."
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        send_email(to_email, subject, body, zip_file_name, smtp_server, smtp_port, from_email, from_password)
    else:
        st.error("Please run the 'Download and Process' step first.")
