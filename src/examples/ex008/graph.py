from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import END, START
from langgraph.graph.state import CompiledStateGraph, StateGraph
from examples.ex008.state import State
from examples.ex008.nodes import call_llm, tool_node
from langgraph.prebuilt.tool_node import tools_condition
from rich import print

def build_graph() -> CompiledStateGraph[State, None]:
    builder = StateGraph(State)

    builder.add_node('call_llm', call_llm)
    builder.add_node("tools", tool_node)
    
    builder.add_edge(START, 'call_llm')
    builder.add_conditional_edges('call_llm', tools_condition, ["tools", END])
    builder.add_edge("tools", "call_llm")

    return builder.compile(checkpointer=InMemorySaver())
