import time
import logging
import torch
import sounddevice as sd
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset

# Configure logging
log_file_path = "tts_log.txt"
logging.basicConfig(level=logging.DEBUG, filename=log_file_path, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info("Importing modules...")
module_load_start = time.time()

module_load_end = time.time()
logging.debug(f"Modules loaded in {module_load_end - module_load_start:.2f} seconds")

def tts(text):
    logging.info("Loading Whisper model...")
    model_load_start = time.time()

    # Load the models and processor
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

    model_load_stop = time.time()
    logging.debug(f"Model loaded in {model_load_stop - model_load_start:.2f} seconds")

    # Process the text
    inputs = processor(text=text, return_tensors="pt")

    # Load speaker embeddings
    embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation")
    speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0)

    # Generate speech
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

    # Play the audio
    logging.info("Playing the audio...")
    sd.play(speech.numpy(), samplerate=16000)
    sd.wait()  # Wait until the audio is finished playing
    logging.info("Audio playback finished.")

def main():
    text = "Welcome to my repository guys!"
    tts(text)

if __name__ == "__main__":
    main()
