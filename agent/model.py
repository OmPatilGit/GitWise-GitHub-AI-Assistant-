from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()

API = os.getenv("OPENAI_API_KEY")
URL = os.getenv("BASE_URL")

def llm(model_name : str = "gpt-oss-20b", temp : int = 0.5):
    """Returns the instance of a LLM model.
    Args : 
    1.model_name : Name of the model to chose.(default to open source)
    2.temp : Set the temperature of the model"""
    
    llm_model = ChatOpenAI(
        model=model_name,
        api_key= API,
        base_url=URL,
        temperature= temp,
        default_headers={
        "HTTP-Referer": "http://localhost",   
        "X-Title": "Agent for project"
        },
        streaming=True
    )
    
    return llm_model