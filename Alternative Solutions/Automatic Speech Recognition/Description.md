# Speech-to-Text (STT) with Noise Reduction

This Python script demonstrates a Speech-to-Text (STT) system using the speech_recognition library combined with noise reduction techniques using noisereduce. It records audio from the microphone, reduces noise, and transcribes speech into text using Google's Speech Recognition API. Audio preprocessing includes noise reduction and volume normalization for improved accuracy.

## Key Features:
- Records audio from microphone using speech_recognition.
- Applies noise reduction using noisereduce.
- Normalizes volume to maintain voice consistency.
- Transcribes speech to text using Google's Speech Recognition API.

## Dependencies:
- speech_recognition
- noisereduce
- numpy
- pydub

## Usage:
- **Install Dependencies:** Ensure dependencies are installed by running the following command:
```
pip install -r requirements.txt
```
- **Python Version:** This script is compatible with Python version 3.8.10.
- **Run Script:** Execute the script to record, preprocess, and transcribe audio
```
python STT.py 
```
