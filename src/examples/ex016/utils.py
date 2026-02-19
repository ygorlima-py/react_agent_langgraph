from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from examples.ex016.env import get_env
from dataclasses import dataclass

OPENROUTER_API_KEY: str = get_env("OPENROUTER_API_KEY")

@dataclass
class ModelsParams:
    base_url: str = "https://openrouter.ai/api/v1"
    api_key: str = get_env("OPENROUTER_API_KEY")

class Models(ModelsParams):
    
    def embedding_model(self) -> OpenAIEmbeddings:
        return OpenAIEmbeddings(
            model="intfloat/e5-large-v2",
            base_url=self.base_url,
            api_key=self.api_key,
            tiktoken_enabled=False,
        )
    
    def llm_model(self, temperature: float = 0.7) -> ChatOpenAI:
    
        return  ChatOpenAI(
                model="openrouter/aurora-alpha",
                base_url=self.base_url,
                api_key=self.api_key,
                temperature=temperature,
                )
        