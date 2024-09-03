import speech_recognition as sr
import noisereduce as nr
import numpy as np
from pydub import AudioSegment
from flask import Flask, jsonify, send_file
import pyttsx3
from index import handle_order,calculate_total

from langchain.memory import ConversationBufferMemory
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import streamlit as st
from langchain.chains import ConversationChain
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain 
from langchain.chains import LLMChain

from langchain_community.document_loaders import CSVLoader

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import SystemMessagePromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os


import time


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
    

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("API key not found in environment variables. Please check your .env file.")

os.environ["OPENAI_API_KEY"] = openai_api_key

def csv_loader(tmp_file_path):
                loader=CSVLoader(file_path=tmp_file_path)

                return loader

loadw = csv_loader(r'kfc_data.csv')


db_file_path='FAISS_Indexkfc'
embeddings = HuggingFaceEmbeddings()


def creation_of_vectorDB_in_local(loader):
    data = loader.load()
    db =FAISS.from_documents(data, embeddings)
    db.save_local(db_file_path)

creation_of_vectorDB_in_local(loadw)

def creation_FAQ_chain():
    db=FAISS.load_local(db_file_path, embeddings,allow_dangerous_deserialization=True)
    retriever =db.as_retriever(score_threshold=0.7)
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125",temperature=0.2)

    template = """
    Given the following context and a query, generate an interactive and friendly response to manage the KFC order or answer the user's
    question about the order. 
The source document contains details about KFC combo pack, menu items ,price, order statuses, and common customer inquiries. Each entry represents specific 
information about menu items, order statuses, or typical customer questions and their responses. Every time When user asking about the food items you should always mention 
the price also the price details given in the CSV file 
Now, you are order managing chatbot use the details of menu items and solve the user problems accodring it, Ensure the response is 
interactive and user-friendly. Also recommend them on add ons after ordering.after conforming order and saying everything finally reply 
menu and price and also the total price
{context}
Current conversation: {chat_history}
Human: {query}
AI:
"""

    prompt = PromptTemplate(input_variables=["chat_history","query","context"], template=template)
    memory = ConversationBufferMemory(memory_key="chat_history",input_key="query",output_key='answer')

    chain = ConversationalRetrievalChain.from_llm(llm,
                                           retriever=retriever, 
                                           memory=memory, 
                                           chain_type="stuff",
                                            get_chat_history=lambda h : h,
                                            combine_docs_chain_kwargs={'prompt': prompt},
                                           verbose=True,return_source_documents = True
                                          )
    return chain


def llmchain(str):
    template = """
        Read the string the string contains item name, quantity and its price so that you need to covert into dictionary and append and give the result
Create a dictionary like the following format 
     ["item_name": "", "quantity": , "price": ],
    ["item_name": "", "quantity": , "price": ],

if nothing is found don't create anything
       {query}"""
    prompt = PromptTemplate(input_variables=['query'],template=template)
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125",temperature=0)
    tweet_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
    query = str
    a = tweet_chain.run(query)
    # print(a)
    return a
    
@app.route('/activate_voice_assistant', methods=['GET'])
def activate_voice_assistant():
    # op = 1
    # result = record_audio()
    # qns= {}
    # # final_res = res["query"]
    # # ans = creation_FAQ_chain()
    # res = ans(result)
    # a = res['answer']
    # b = res['query']
    # # qns['result'] = a
    # # qns['query'] = b
    # fg = handle_order(b)
    # if result == "final order":
    #     calculate_total(fg)
    # print(a)

    ans = creation_FAQ_chain()
    con = 'You are a KFC chatbot'
    while True:
        # if input():
             
        q = record_audio()
        if 'exit' in q:
            break
        else:   
            res = ans({"context":con,"question":q,"query": q})
            print(res['answer'])
            text_to_speech(res['answer'])
            time.sleep(3)
            
            yu = llmchain(res['answer'])

            print(llmchain(res['answer']))
            with open("example.txt", "w") as file:
                file.write(yu)

            with open('example.txt', 'r') as file:
                content = file.read()

            # Remove square brackets
            content = content.replace('[', '').replace(']', '')

            with open('example.txt', 'w') as file:
                file.write(content)

            # print(type(dictre))
            # print(dictre)

    return jsonify({"message": q})
   


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
