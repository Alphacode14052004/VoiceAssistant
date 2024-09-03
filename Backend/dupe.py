import speech_recognition as sr
import noisereduce as nr
import numpy as np
from pydub import AudioSegment
from flask import Flask, jsonify, send_file
import pyttsx3
from index import handle_order,calculate_total
from test import creation_FAQ_chain
app = Flask(__name__)

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
    with sr.Microphone() as source:
        print("Recording")
        audio_data = r.listen(source)
        print("Preprocessing audio...")
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
        print("Transcribing audio...")
        recognizer_audio = sr.AudioData(
            processed_audio.raw_data, 
            sample_rate=processed_audio.frame_rate, 
            sample_width=processed_audio.sample_width
        )
        try:
            recognized_text = r.recognize_google(recognizer_audio)
            return recognized_text
        except sr.UnknownValueError:
            return "Google Speech Recognition could not understand the audio"
        except sr.RequestError as e:
            return f"Could not request results from Google Speech Recognition service; {e}"

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    



@app.route('/activate_voice_assistant', methods=['GET'])
def activate_voice_assistant():
    op = 1
    result = record_audio()
    qns= {}
    # final_res = res["query"]
    
    ans = creation_FAQ_chain()
    res = ans(result)
    a = res['answer']
    b = res['query']
    # qns['result'] = a
    # qns['query'] = b
    fg = handle_order(b)
    if result == "final order":
        calculate_total(fg)
    print(a)

    return jsonify({"message": result})
   

if __name__ == '__main__':
    app.run(debug=True)
