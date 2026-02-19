from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from examples.ex015.env import get_env

OPENROUTER_API_KEY: str = get_env("OPENROUTER_API_KEY")

def embeddings_model() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(
        model="sentence-transformers/all-minilm-l6-v2",
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        tiktoken_enabled=False,
    )

def load_llm() -> ChatOpenAI:
    
    return  ChatOpenAI(
            model="openrouter/aurora-alpha",
            api_key=OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1",
            )
    

if __name__ == "__main__":
    llm = load_llm()
    response = llm.invoke("Olá chat")
    print(response)