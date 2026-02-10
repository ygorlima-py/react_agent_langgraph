from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import END, START
from langgraph.graph.state import CompiledStateGraph, StateGraph
from langchain_core.messages import AIMessage, ToolMessage
from examples.ex006.state import State
from examples.ex006.utils import load_llm
from examples.ex006.tools import TOOLS, TOOLS_BY_NAME
from pydantic import ValidationError
from typing import Literal

def call_llm(state: State) -> State:
    print('>Call LLM')

    llm_with_tools = load_llm().bind_tools(TOOLS) # carrego a llm com as ferramentas tools
    result = llm_with_tools.invoke(state["messages"]) # Aqui ja tenho a llm com as ferramentas carregadas
    return {'messages': [result]}

def tool_node(state: State) -> State:
    print(">Tool Node")
    llm_response = state["messages"][-1]

    if isinstance(llm_response, AIMessage) or not getattr(
        llm_response, "tool_calls", None
        ):
        return state
    call = llm_response.tool_calls[-1]
    name, args, id_ = call['name'], call['args'], call['id']

    try:
        content = TOOLS_BY_NAME[name].invoke(args) # Chamando LLM novamente 
        status = 'success'

    except (KeyError, IndexError, TypeError, ValueError, ValidationError) as error:
        content = f'Please, fix your mistakes: {error}'
        status = 'error'

    tool_message = ToolMessage(content=content, tool_call_id=id_, status=status)
    
    return {'messages': [tool_message]}

def router(state: State) -> Literal["tool_node", "__end__", None]:
    print("> Router")
    llm_response = state["messages"][-1]

    if getattr(llm_response, "tool_calls", None):
        return "tool_node"
    return "__end__"

def build_graph() -> CompiledStateGraph[State, None]:
    builder = StateGraph(State)

    builder.add_node('call_llm', call_llm)
    builder.add_node("tool_node", tool_node)
    
    builder.add_edge(START, 'call_llm')
    builder.add_conditional_edges('call_llm', router, ["tool_node", "__end__"])
    builder.add_edge("tool_node", "call_llm")

    return builder.compile(checkpointer=InMemorySaver())
