

## Join the Community
[Join Curious PM Community](https://curious.pm) to connect, share, and learn with others!

Explore the capabilities of speech-to-text conversion through an interactive application built with Streamlit and Google Cloud Speech-to-Text API.

## Streamlit Speech-to-Text App

This application demonstrates how audio recordings can be transcribed into text using Google Cloud’s Speech-to-Text API. Users can record audio, transcribe it in real time, and support multiple languages.

It leverages **Streamlit** for the user interface, **Google Cloud Speech-to-Text API** for transcription, and tools like **pydub** for audio processing.

---

# Speech-to-Text 

This project provides an interactive playground to record, process, and transcribe audio files using Google Cloud Speech-to-Text API.

## What the Code Does

This application enables users to:

- **Record Audio:** Capture audio using the microphone.
- **Transcribe Speech:** Convert the recorded audio into text.
- **Multi-Language Support:** Select different language codes for transcription.
- **Real-Time Interaction:** Start and stop recordings dynamically.
- **Educational Content:** Learn how audio processing and transcription APIs work.

### Features:
- **Customizable Options:** Modify recording duration and language preferences.
- **Simple Integration:** Uses Google Cloud APIs with easy configuration.
- **Interactive UI:** Built with Streamlit for user-friendly interaction.

---

## What is Speech-to-Text?

**Speech-to-Text** technology converts spoken language into written text using advanced machine learning algorithms. It allows computers to:

- Recognize spoken words in real-time.
- Support accessibility through transcription.
- Enable applications like voice assistants, call analysis, and more.

For example:
- Saying "How’s the weather today?" can be transcribed into text for further analysis or response.

---

## Applications of Speech-to-Text

Here are some real-world use cases:

1. **Accessibility Tools:** Generate subtitles for videos or transcriptions for audio.
2. **Voice Assistants:** Enable interactions with devices through voice commands.
3. **Customer Support Analysis:** Analyze recorded calls for insights.
4. **Meeting Notes:** Automatically transcribe meeting audio into text for records.

---

## How to Implement It (Step by Step)

### 1. Set Up Your Environment
Start by creating a new project directory and setting up a Python virtual environment.
```bash
mkdir speech_to_text_app
cd speech_to_text_app
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

### 2. Install Required Dependencies
Create a `requirements.txt` file with the following content:
```
streamlit
google-cloud-speech
pyaudio
```
Then install the dependencies using:
```bash
pip install -r requirements.txt
```

### 3. Create the Main App File
Inside your project directory, create a file called `app.py`. Add the following code to set up the Streamlit interface:

```python
import streamlit as st
import pyaudio
import wave
import io
from google.cloud import speech
from google.oauth2 import service_account

# Set up Google Cloud credentials
client_file = "creds.json"  # Change this to your actual service account file
credentials = service_account.Credentials.from_service_account_file(client_file)
client = speech.SpeechClient(credentials=credentials)

# Streamlit UI setup
st.title("Speech-to-Text Converter using Google Cloud")
st.write("Click the button below to record audio from your microphone and get the transcription.")

# Audio recording function
def record_audio(file_path, record_seconds=5):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    audio = pyaudio.PyAudio()
    st.info("Recording... Speak now!")

    stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    frames = []

    for _ in range(0, int(rate / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    st.success("Recording completed!")

# Transcribe audio using Google Cloud
def transcribe_audio(file_path):
    with io.open(file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcriptions = [result.alternatives[0].transcript for result in response.results]
    return " ".join(transcriptions)

# File path for recorded audio
audio_file_path = "recorded_audio.wav"

if st.button("🎤 Start Recording"):
    record_audio(audio_file_path, record_seconds=5)

if st.button("📜 Transcribe Audio"):
    if audio_file_path:
        st.info("Transcribing audio...")
        transcription = transcribe_audio(audio_file_path)
        if transcription:
            st.success("Transcription complete!")
            st.write("**Transcribed Text:**")
            st.text_area("Transcription", transcription, height=150)
        else:
            st.warning("No speech detected. Try recording again.")
    else:
        st.error("No audio recorded. Please record first.")
```

### 4. Configure Google Cloud Credentials
Place your service account file (`creds.json`) in the root directory.
Make sure the Google Cloud Speech-to-Text API is enabled for your project.

---

## Folder Structure

```
streamlit_speech_to_text/
├── README.md             # Documentation explaining the project and usage.
├── app.py                # Main Streamlit application script that handles UI and logic.
├── requirements.txt      # List of required Python libraries to run the application.
└── sample_audio.wav      # Temporary audio file for transcription.
```

### Explanation of Files
- **README.md**
  - Contains details about the project, setup instructions, and usage guide.
- **app.py**
  - Core application script containing the Streamlit UI and logic for audio recording and transcription.
- **requirements.txt**
  - Lists all dependencies required to run the app.
- **sample_audio.wav**
  - Placeholder for audio files recorded during testing.

---

## Expected Output Example

**Input:** Audio recorded saying "Hello, world!"

**Output:**

```
Transcribed text:
Hello, world!
```

---

## Technologies Used

1. **Backend**:
   - **Google Cloud Speech-to-Text API**: For transcribing speech.
   - **pydub**: For audio processing and format conversion.

2. **Frontend**:
   - **Streamlit**: For the user interface.

3. **Audio Management**:
   - **wave**: To handle audio file formats.
   - **pyaudio**: For recording audio from the microphone.

---

## Security Considerations

- **Do not share your API keys.**
- Use environment variables for sensitive configurations.
- Regularly update API keys for security.

---

## Link to Hosted Version
[View Live App](#) *(Insert actual deployment link here)*

---

## Screenshots

### Main Interface:
<img src="https://github.com/user-attachments/assets/48c5a8d1-50db-4e12-9269-0ccbe4e811dd" style="width: 400px;" alt="Main Interface">

---

## Video Overview
*A short video walkthrough will be provided explaining the app's features and usage.*
