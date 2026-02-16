from langchain_openai import OpenAIEmbeddings
from examples.ex014.env import get_env

OPENROUTER_API_KEY: str = get_env("OPENROUTER_API_KEY")

def embeddings_model() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model="sentence-transformers/all-minilm-l6-v2",
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        tiktoken_enabled=False,
    )