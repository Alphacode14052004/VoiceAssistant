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
The source document contains details about KFC menu items, order statuses, and common customer inquiries. Each entry represents specific 
information about menu items, order statuses, or typical customer questions and their responses.
Now, you are order managing chatbot use the details of menu items and solve the user problems accodring it, Ensure the response is 
interactive and user-friendly. Also recommend them on add ons after ordering.after conforming order and saying everything finally reply 
menu and price and also the total
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
    # chain = ConversationalRetrievalChain.from_llm(llm,
    #                                        retriever=retriever, 
    #                                        memory=memory,
    #                                         get_chat_history=lambda h : h,
    #                                         combine_docs_chain_kwargs={'prompt': prompt},
    #                                        verbose=True,return_source_documents = True
    #                                       )
    
    return chain

if __name__ == "__main__":

    

    ans = creation_FAQ_chain()
    con = 'You are a KFC chatbot'
    while True:
        q = input()
        if q == 'Exit':
            break
        else:   
            res = ans({"context":con,"question":q,"query": q})
            print(res['answer'])

 