import streamlit as st
import pyaudio
import wave
import io
from google.cloud import speech
from google.oauth2 import service_account

# ----------------------------------------
# Set up Google Cloud credentials
# ----------------------------------------
credentials_dict = st.secrets["google_cloud"]
credentials = service_account.Credentials.from_service_account_info(credentials_dict)
client = speech.SpeechClient(credentials=credentials)

# ----------------------------------------
# Streamlit Sidebar Explanation
# ----------------------------------------
with st.sidebar:
    st.header("ℹ️ About Google Cloud Speech-to-Text")
    st.write("Google Cloud Speech-to-Text (SST) is a powerful service that converts speech to text using machine learning.")
    st.write("### How It Works:")
    st.write(
        "1. Audio input is recorded through your microphone.\n"
        "2. The audio file is sent to Google Cloud's Speech-to-Text API.\n"
        "3. The API processes the audio and returns a transcription of the spoken content.\n"
    )
    st.write("You can adjust the recording duration and language settings to suit your needs.")
    st.markdown("---")
    st.write("**Instructions:** Use the 'Start Recording' button to capture audio and 'Transcribe Audio' to get the text output.")

# ----------------------------------------
# Streamlit app main section
# ----------------------------------------
st.title(" Speech to Text Converter using Google Cloud")
st.write("Click the button below to record audio from your microphone and get the transcription.")

# ----------------------------------------
# Function to record audio from the microphone and save it to a WAV file
# ----------------------------------------
def record_audio(file_path, record_seconds=5):
    # Audio recording settings
    chunk = 1024  # Record in chunks of 1024 samples
    format = pyaudio.paInt16  # 16-bit audio format
    channels = 1  # Mono audio
    rate = 44100  # Sample rate in Hz (CD quality)

    # Initialize PyAudio instance
    audio = pyaudio.PyAudio()

    st.info("Recording... Speak now!")  # Display a message to indicate recording has started

    # Open an audio stream for input recording
    stream = audio.open(format=format, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=chunk)

    frames = []  # To store audio frames

    # Loop to record audio for the specified duration
    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)  # Read audio data from the stream
        frames.append(data)  # Append the audio data to frames

    # Stop and close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded audio to a WAV file
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    st.success("Recording completed!")  # Indicate recording completion

# ----------------------------------------
# Function to transcribe audio using Google Cloud Speech-to-Text API
# ----------------------------------------
def transcribe_audio(file_path):
    # Read audio content from the file
    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    # Configure the Google Cloud API for audio transcription
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # WAV files use LINEAR16 encoding
        sample_rate_hertz=44100,  # Sample rate matches the recording rate
        language_code="en-US"  # Language of the audio input
    )

    # Send audio data to Google Cloud for transcription
    response = client.recognize(config=config, audio=audio)

    # Extract and combine transcriptions from all recognized segments
    transcriptions = [result.alternatives[0].transcript for result in response.results]
    return " ".join(transcriptions)  # Return the full transcription as a single string

# ----------------------------------------
# File path for recorded audio
# ----------------------------------------
audio_file_path = "recorded_audio.wav"

# ----------------------------------------
# Record Audio Button
# ----------------------------------------
if st.button("🎤 Start Recording"):
    st.write("Recording will last for 5 seconds.")
    record_audio(audio_file_path, record_seconds=5)  # Record audio for 5 seconds

# ----------------------------------------
# Transcribe Audio Button
# ----------------------------------------
if st.button("📜 Transcribe Audio"):
    if audio_file_path:  # Check if the audio file path is available
        st.info("Transcribing audio... Please wait.")
        transcription = transcribe_audio(audio_file_path)  # Call the transcription function

        if transcription:  # If transcription is successful
            st.success("Transcription complete!")
            st.write("**Transcribed Text:**")
            st.text_area("Transcription", transcription, height=150)  # Display the transcription
        else:
            st.warning("No speech detected. Try recording again.")
    else:
        st.error("No audio recorded. Please record first.")  # Error message if no audio is recorded
