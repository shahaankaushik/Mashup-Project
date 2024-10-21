# YouTube Audio Processor

This Streamlit application allows users to download audio from YouTube videos, process them, and send the results via email.

## Features

- Download audio from multiple YouTube videos
- Trim audio files to a specified duration
- Merge multiple audio files into a single file
- Zip the merged audio file
- Send the zipped file via email

## Requirements

- Python 3.7+
- Streamlit
- yt-dlp
- moviepy
- imageio-ffmpeg
- Other dependencies listed in `requirements.txt`

## Setup

1. Clone this repository:
   ```
   git clone https://github.com/shahaankaushik/Mashup-Project
   cd youtube-audio-processor
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create the necessary directories:
   ```
   mkdir audio trimmed_audio
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and go to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Enter the number of YouTube videos you want to process and provide their URLs.

4. Click "Download and Process" to start the audio processing pipeline.

5. Once processing is complete, you can send the result via email by entering the required information in the "Send the final audio file via email" section.

## Important Notes

- This application uses the Gmail SMTP server for sending emails. Make sure to allow less secure apps in your Google account settings or use an app-specific password.
- The email sending feature is set up for Gmail. If you're using a different email provider, you may need to modify the SMTP settings in the code.
- Be aware of YouTube's terms of service when using this tool. It's intended for personal use only.

## Troubleshooting

- If you encounter issues with ffmpeg, make sure it's properly installed and accessible in your system PATH.
- For any other issues, please check the error messages in the Streamlit interface and ensure all dependencies are correctly installed.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the web app framework
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for YouTube video downloading
- [MoviePy](https://zulko.github.io/moviepy/) for audio processing
