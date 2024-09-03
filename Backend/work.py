import openai
from langchain_openai import ChatOpenAI


import os
from langchain.prompts import PromptTemplate

from langchain.chains import LLMChain
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("API key not found in environment variables. Please check your .env file.")

os.environ["OPENAI_API_KEY"] = openai_api_key

template = """
        Read the string the and reply as a general assistant
       {query}"""
prompt = PromptTemplate(input_variables=['query'],template=template)
llm = ChatOpenAI(model="gpt-3.5-turbo-0125",temperature=0)
tweet_chain = LLMChain(llm=llm, prompt=prompt, verbose=True)
query = 'I want to open a restaurant for Indian food. Suggest a fancy name for this.'
a = tweet_chain.run(query)
print(a)
# return a
    