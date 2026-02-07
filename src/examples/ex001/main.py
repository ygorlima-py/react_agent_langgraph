from langchain.chat_models import init_chat_model
from rich import print

llm = init_chat_model("google_genai:gemini-2.5-flash")

response = llm.invoke('Olá LLM?, eu moro na Tailândia')
print(response)