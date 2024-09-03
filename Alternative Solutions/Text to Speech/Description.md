# Text-to-Speech (TTS) using SpeechT5 with HiFi-GAN Vocoder
This Python script demonstrates a Text-to-Speech (TTS) system using the SpeechT5 model from Hugging Face's Transformers library. It loads the model and vocoder, processes text input, generates speech, and saves the output to a WAV file. The script uses logging to track module loading and model loading times for performance monitoring.

## Key Components:
- Module Loading: Imports necessary libraries (torch, soundfile, transformers, datasets) and logs the time taken for module importation.
- Model Loading: Loads the SpeechT5 model and HiFi-GAN vocoder from the Hugging Face model hub, logging the time taken for model initialization.
- Text Processing: Converts input text into speech using the loaded model and vocoder.
- Logging: Utilizes logging to record detailed information about module loading, model loading, and speech generation processes.

## Dependencies:
- torch: PyTorch library for tensor computations.
- soundfile: Library for reading and writing sound files.
- transformers: Hugging Face's library for NLP and deep learning.
- datasets: Hugging Face's library for accessing and managing datasets.

## Usage:
- **Install Dependencies:** Ensure dependencies are installed by running the following command:
```
pip install -r requirements.txt
```
- **Python Version:** This script is compatible with Python version 3.8.10.
- **Run Script:** Execute the script to record, preprocess, and transcribe audio:
```
python TTS.py
```
- **Logging Setup:** Configure logging to tts_log.txt file with timestamps (%(asctime)s), log levels (%(levelname)s), and detailed messages (%(message)s).
- **Run Script:** Execute the script (python script.py) to generate speech from the provided text input and save it as speech.wav.

This script provides a streamlined approach to convert text into speech using state-of-the-art neural network models, offering flexibility for various TTS applications.
