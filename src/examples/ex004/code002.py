from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, START, StateGraph, add_messages
from langgraph.graph.state import RunnableConfig
import threading
from langgraph.checkpoint.memory import InMemorySaver
from rich import print
from langchain_openai import ChatOpenAI
from rich.markdown import Markdown
import os
import time

llm = ChatOpenAI(
    model="openrouter/pony-alpha",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

# 1 -  Defino o meu state
class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage], add_messages]

#2 - Defino os meus nodes
def call_llm(state: AgentState) -> AgentState:
    llm_result = llm.invoke(state['messages'])
    # llm_result = AIMessage("Oi como vai?")
    return {'messages': [llm_result]}

#3 - Crio o StateGraph
builder = StateGraph(
    AgentState, context_schema=None, input_schema=AgentState, output_schema=AgentState
)

# 4 - Adicionar nodes ao grafo
builder.add_node("call_llm", call_llm)
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

# 5 - Compilar o grafo
checkpointer = InMemorySaver()
config = RunnableConfig(configurable={"thread_id": threading.get_ident()})
graph = builder.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    current_messages: Sequence[BaseMessage] = []

    while True:
        user_input = input("Digite sua menssagem: ")
        print(Markdown("---"))

        if user_input.lower() in ["exit", 'q', 'quit']:
            print('Finalizando chat')
            time.sleep(3)
            print('Chat Finalizado')
            print(Markdown('---'))
            break

        human_message = HumanMessage(user_input)
        result = graph.invoke({'messages': [human_message]}, config=config)

        print(Markdown(str(result['messages'][-1].content)))
        print(Markdown('---'))
