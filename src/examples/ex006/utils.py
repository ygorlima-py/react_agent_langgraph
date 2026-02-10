from langchain_openai import ChatOpenAI
import os

def load_llm() -> ChatOpenAI:
    
    return  ChatOpenAI(
            model="openrouter/pony-alpha",
            api_key=os.getenv("OPENROUTER_API_KEY"), #type:ignore
            base_url="https://openrouter.ai/api/v1",
            )