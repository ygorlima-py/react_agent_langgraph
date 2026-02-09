from langchain.tools import tool, BaseTool
from rich import print
from langchain.chat_models import init_chat_model
from langchain_core.messages import (
    BaseMessage,
    SystemMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
    )
from pydantic import ValidationError
from langchain_openai import ChatOpenAI
import os 

@tool
def multiply(a: float, b: float) -> float:
   """
   Multiply a * b and returns the result

   Args:
   a: float multiplicand
   b: float multiplier

   Returns
    The resulting float of the equation a * b
   """ 
   return a * b

llm = ChatOpenAI(
    model="openrouter/pony-alpha",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

system_message = SystemMessage(
   'You are a helpful assistant. You have access to tools. When the user asks'
    'for something, first look if you have a tool that solves that problem'
)

human_message = HumanMessage("Oi, sou Ygor Lima. Pode me falar quanto é 20 vezes 17.4")
# human_message = HumanMessage("Oi, sou Ygor Lima.")
messages: list[BaseMessage] = [system_message, human_message]

tools: list[BaseTool] = [multiply]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

llm_response = llm_with_tools.invoke(messages) # Chamando LLM com system_messages e human_messages
messages.append(llm_response) # Adicionando a resposta apos a chamada em messages

print(messages)
# Verifico se na instância AIMessage possui o atributo tools_calls
if isinstance(llm_response, AIMessage) and getattr(llm_response, "tool_calls"):
    call = llm_response.tool_calls[-1]
    name, args, id_ = call['name'], call['args'], call['id']

    try:
        content = tools_by_name[name].invoke(args) # Chamando LLM novamente 
        status = 'success'
    except (KeyError, IndexError, TypeError, ValueError, ValidationError) as error:
        content = f'Please, fix your mistakes: {error}'
        status = 'error'
    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)
    messages.append(tool_message)

    llm_response = llm_with_tools.invoke(messages)
    messages.append(llm_response)
    print(messages)

