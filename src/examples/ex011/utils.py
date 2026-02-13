from langchain_openai import ChatOpenAI
import os
import requests
from rich import print
from langchain.chat_models import init_chat_model, BaseChatModel
from typing import AsyncGenerator, Generator, cast
from contextlib import asynccontextmanager, contextmanager
from functools import lru_cache

def load_llm_google() -> BaseChatModel:

    model = cast(BaseChatModel, init_chat_model(
        model="gemini-2.5-flash",
        model_provider="google_genai",
        temperature=0.2, 
        configurable_fields=("temperature", ),
    ))

    assert hasattr(model, "bind_tools")
    assert hasattr(model, "invoke")
    assert hasattr(model, "with_config")

    return model

def load_llm() -> ChatOpenAI:
    
    return  ChatOpenAI(
            model="openrouter/aurora-alpha",
            api_key=os.getenv("OPENROUTER_API_KEY"), #type:ignore
            base_url="https://openrouter.ai/api/v1",
            temperature=0.2,
            )
    
class Connection: 
    def use(self):
        print("To usando a porra da conexão...")
        
    def open_connection(self) -> None:
        print("Open connection DataBase")
    
    def close_connection(self) -> None:
        print("Close connection DataBase")
        
@lru_cache
def get_connection() -> Connection:
    return Connection()

@contextmanager
def sync_lifespan() -> Generator[Connection]:
    print("Abri de forma Sync")
    yield get_connection()
    print("Fechei de forma Sync")

@asynccontextmanager
async def async_lifespan() -> AsyncGenerator[Connection]:
    print("Abri de forma Async")
    yield get_connection()
    print("Fechei de forma Async")