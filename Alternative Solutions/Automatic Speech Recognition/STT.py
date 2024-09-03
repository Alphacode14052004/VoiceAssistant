import time
# module_import_start = time.time()
import os
# import logging
import speech_recognition as sr
import noisereduce as nr
import numpy as np
from pydub import AudioSegment

def preprocess_audio(audio_data):
    
    audio_array = np.array(audio_data.get_array_of_samples())
    
    
    reduced_noise = nr.reduce_noise(y=audio_array, sr=audio_data.frame_rate)

    
    processed_audio = AudioSegment(
        reduced_noise.tobytes(), 
        frame_rate=audio_data.frame_rate,
        sample_width=audio_data.sample_width,
        channels=audio_data.channels
    )

    return processed_audio

def record_audio():
    r = sr.Recognizer()
    record_start = time.time()
    with sr.Microphone() as source:
          
        print("Recording")
      
        audio_data = r.listen(source)
        record_end = time.time()
        print("Preprocessing audio...")
        preprocess_start = time.time()
       
        raw_audio = audio_data.get_raw_data()
        audio_segment = AudioSegment(
            raw_audio, 
            frame_rate=source.SAMPLE_RATE, 
            sample_width=2, 
            channels=1
        )
        audio_segment.export("original_audio.wav", format="wav")
        processed_audio = preprocess_audio(audio_segment)
        
        processed_audio.export("processed_audio.wav", format="wav")
        preprocess_end = time.time()
        # logging.debug(f"Audio preprocessed in {preprocess_end - preprocess_start:.2f} seconds")
        
        # logging.info("Transcribing audio")
        print("Transcribing audio...")
        transcribe_start = time.time()
        
        recognizer_audio = sr.AudioData(
            processed_audio.raw_data, 
            sample_rate=processed_audio.frame_rate, 
            sample_width=processed_audio.sample_width
        )
        
        try:
            recognized_text = r.recognize_google(recognizer_audio)
            print("Text: " + recognized_text)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio")
            # logging.debug("Google Speech Recognition could not understand the audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            # logging.debug(f"Could not request results from Google Speech Recognition service; {e}")
        
        transcribe_end = time.time()
        # logging.debug(f"Audio transcribed in {transcribe_end - transcribe_start:.2f} seconds")

def main():
    record_audio()

if __name__ == '__main__':
    main()
