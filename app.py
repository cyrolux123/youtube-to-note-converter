import streamlit as st
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv() 

# Get the Google API key from the environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the prompt for Google Gemini API
prompt = """You are YouTube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 300 words. Please provide the summary of the text given here:  """

# Function to extract transcript from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        
        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]
            
        return transcript

    except TranscriptsDisabled:
        st.error("Transcripts are disabled or unavailable for this video.")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to generate summary using Google Gemini API
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

# Streamlit app interface
st.title("YouTube Video to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[-1] 
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/0.jpg"
    st.image(thumbnail_url, caption="YouTube Video Thumbnail", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)

    if transcript_text:
        summary = generate_gemini_content(transcript_text, prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
