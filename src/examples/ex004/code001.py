from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, START, StateGraph, add_messages
from rich import print
from langchain.chat_models import init_chat_model
from rich.markdown import Markdown
import time

llm = init_chat_model("google_genai:gemini-2.5-flash")

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
graph = builder.compile()

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
        current_messages = [*current_messages, human_message]

        result = graph.invoke({'messages': current_messages})
        current_messages = result["messages"]

        print(Markdown(str(result['messages'][-1].content)))
        print(Markdown('---'))
