import streamlit as st
import pymupdf
import json
import pyttsx3
import time
from pathlib import Path
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_VERSION = os.getenv("AZURE_OPENAI_VERSION")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")

SYSTEM_PROMPT = """
You are a world-class podcast producer tasked with transforming the provided input text into an engaging and informative podcast script. The input may be unstructured or messy, sourced from PDFs or web pages. Your goal is to extract the most interesting and insightful content for a compelling podcast discussion.

# Steps to Follow:

1. **Analyze the Input:**
   Carefully examine the text, identifying key topics, points, and interesting facts or anecdotes that could drive an engaging podcast conversation. Disregard irrelevant information or formatting issues.

2. **Brainstorm Ideas:**
   In the `<scratchpad>`, creatively brainstorm ways to present the key points engagingly. Consider:
   - Analogies, storytelling techniques, or hypothetical scenarios to make content relatable
   - Ways to make complex topics accessible to a general audience
   - Thought-provoking questions to explore during the podcast
   - Creative approaches to fill any gaps in the information

3. **Craft the Dialogue:**
   Develop a natural, conversational flow between the host (Jane) and the guest speaker (the author or an expert on the topic). Incorporate:
   - The best ideas from your brainstorming session
   - Clear explanations of complex topics
   - An engaging and lively tone to captivate listeners
   - A balance of information and entertainment

   Rules for the dialogue:
   - The host (Jane) always initiates the conversation and interviews the guest
   - Include thoughtful questions from the host to guide the discussion
   - Incorporate natural speech patterns, including occasional verbal fillers (e.g., "um," "well," "you know")
   - Allow for natural interruptions and back-and-forth between host and guest
   - Ensure the guest's responses are substantiated by the input text, avoiding unsupported claims
   - Maintain a PG-rated conversation appropriate for all audiences
   - Avoid any marketing or self-promotional content from the guest
   - The host concludes the conversation

4. **Summarize Key Insights:**
   Naturally weave a summary of key points into the closing part of the dialogue. This should feel like a casual conversation rather than a formal recap, reinforcing the main takeaways before signing off.

5. **Maintain Authenticity:**
   Throughout the script, strive for authenticity in the conversation. Include:
   - Moments of genuine curiosity or surprise from the host
   - Instances where the guest might briefly struggle to articulate a complex idea
   - Light-hearted moments or humor when appropriate
   - Brief personal anecdotes or examples that relate to the topic (within the bounds of the input text)

6. **Consider Pacing and Structure:**
   Ensure the dialogue has a natural ebb and flow:
   - Start with a strong hook to grab the listener's attention
   - Gradually build complexity as the conversation progresses
   - Include brief "breather" moments for listeners to absorb complex information
   - End on a high note, perhaps with a thought-provoking question or a call-to-action for listeners

IMPORTANT RULE: Each line of dialogue should be no more than 100 characters (e.g., can finish within 5-8 seconds)

Remember: Always reply in valid JSON format, without code blocks. Begin directly with the JSON output.
pydantic: fromat # Define a Pydantic model for each dialogue entry
class DialogueEntry(BaseModel):
    speaker: str
    text: str

# Define a Pydantic model for the overall podcast episode
class PodcastEpisode(BaseModel):
    host: str
    guest: str
    dialogue: List[DialogueEntry]
"""


QUESTION_MODIFIER = "PLEASE ANSWER THE FOLLOWING QN:"

TONE_MODIFIER = "TONE: The tone of the podcast should be"

LANGUAGE_MODIFIER = "OUTPUT LANGUAGE <IMPORTANT>: The the podcast should be"

LLM = AzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_VERSION,
)

# Streamlit UI for file upload
st.title("Podcast Generator from PDF")
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

def extract_text_from_pdf(pdf_path):
    doc = pymupdf.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def generate_podcast_script(input_text):
    

    response = LLM.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": input_text},
        ],
        model="jarvis-embed",
        response_format={"type": "json_object"},
    )

    dialogue_content = response.choices[0].message.content
    dialogue_json = json.loads(dialogue_content)
    return dialogue_json

def speak_dialogue(dialogue_json, output_file="podcast_episode.mp3"):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    full_text = ""
    for entry in dialogue_json['dialogue']:
        speaker = entry['speaker']
        text = entry['text']
        
        if speaker == "Jane":
            engine.setProperty('voice', voices[1].id)  # Female voice
        else:
            engine.setProperty('voice', voices[0].id)  # Male voice

        full_text += f"{text} "

    engine.save_to_file(full_text, output_file)
    engine.runAndWait()

    return output_file

# Process the uploaded PDF
if pdf_file:
    # Save the uploaded file to disk
    pdf_path = Path("uploaded_file.pdf")
    with open(pdf_path, "wb") as f:
        f.write(pdf_file.getbuffer())

    # Extract text from the PDF
    with st.spinner("Extracting text from the PDF..."):
        pdf_text = extract_text_from_pdf(pdf_path)
    
    # Display extracted text
    st.subheader("Extracted Text:")
    st.write(pdf_text[:1000])  # Show the first 1000 characters
    
    # Summarize and generate podcast script
    with st.spinner("Generating podcast script..."):
        dialogue_json = generate_podcast_script(pdf_text)
    # st.subheader("generated podcast script:")
    # st.write(dialogue_json)

    # Generate and save the podcast audio
    with st.spinner("Converting podcast script to audio..."):
        audio_file = speak_dialogue(dialogue_json)
    
    # Play the audio in the browser
    st.subheader("Generated Podcast Audio")
    audio_bytes = open(audio_file, "rb").read()
    st.audio(audio_bytes, format="audio/mp3")

