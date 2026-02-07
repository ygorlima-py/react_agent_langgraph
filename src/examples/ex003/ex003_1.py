from typing import TypedDict, Annotated
from langgraph.graph import StateGraph
from rich import print
import operator
from dataclasses import dataclass


# def reducer(a: list[str], b:list[str]) -> list[str]:
#     return a + b

# 1 - Definir o meu estado
@dataclass
class State(TypedDict):
    nodes_path: Annotated[list[str], operator.add]

# 2- Definir o node:
def node_a(state:State) -> State: 
    output_state: State = State(nodes_path=['A'])
    print("> node_a",f'{state=}', f'{output_state=}')
    return output_state


def node_b(state: State) -> State:
    output_state: State = State(nodes_path=['B'])
    print('> node_b', f'{state=}', f'{output_state=}')
    return output_state


# Definir o builder do grafo
builder = StateGraph(State)

builder.add_node("A", node_a)
builder.add_node("B", node_b)

# Conectar as edges (ou arestas)
builder.add_edge("__start__", "A")
builder.add_edge("A", "B")
builder.add_edge("B", "__end__")

# compilar grafo
graph = builder.compile()

# Para gerar um PPNG do Grafo
# graph.get_graph().draw_mermaid_png(output_file_path="file.png")

# Para printar o código do grafo e colocar no mermaid
# print(graph.get_graph().draw_mermaid())

# Pegar o resultado
response = graph.invoke(State(nodes_path=[]))
print()
print(f'{response=}')
print()