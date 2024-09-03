from langchain.memory import ConversationBufferMemory
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate


from langchain.chains import RetrievalQA

from langchain_community.utilities import SQLDatabase

from langchain_community.document_loaders import CSVLoader

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.agent_toolkits import create_sql_agent
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("API key not found in environment variables. Please check your .env file.")

os.environ["OPENAI_API_KEY"] = openai_api_key

 
db = SQLDatabase.from_uri("sqlite:///Chinook.db")
# print(db.dialect)
# print(db.get_usable_table_names())
db.run("SELECT * FROM Artist LIMIT 10;")

def sql_loadeer(db,llm): 
    loader = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    
    return loader

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
    # llm = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.2) 
    template = """
    Given the following context and a query, generate an interactive and friendly response to manage the KFC order or answer the user's question about the order. 

    The source document contains details about KFC menu items, order statuses, and common customer inquiries. Each entry represents specific information about menu items, order statuses, or typical customer questions and their responses.

    Now, using the provided context and query, generate an answer based on the information provided in the context section. Ensure the response is interactive and user-friendly. If no other previous orders then dont hallucinate and just say there is no orders.

CONTEXT: {context}
QUESTION: {question}
"""

    prompt = PromptTemplate(input_variables=["prompt","chat_history"], template=template)
    memory = ConversationBufferMemory(memory_key="chat_history")

    chain = RetrievalQA.from_chain_type(llm=llm,chain_type="stuff", 
                                        retriever=retriever, 
                                        input_key="query", 
                                        return_source_documents=False,
                                        chain_type_kwargs={"prompt" : prompt},memory=memory)
    
    return chain

# if __name__ == "__main__":
    
#     ans = creation_FAQ_chain()
    
#     # final_res = res["query"]
#     while True:
#         query=input().strip()
#         res = ans(query)
#         if query == "exit":
#               break
#         a = res['result']
#         b = res['query']
#         # print(a)