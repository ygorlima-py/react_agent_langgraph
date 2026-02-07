from typing import TypedDict, Annotated, Literal
from langgraph.graph import StateGraph
from rich import print
import operator
from dataclasses import dataclass


# def reducer(a: list[str], b:list[str]) -> list[str]:
#     return a + b

# 1 - Definir o meu estado
@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add]
    current_number: int = 0

# 2- Definir o node:
def node_a(state:State) -> State: 
    output_state: State = State(nodes_path=['A'], current_number=state.current_number)
    print("> node_a",f'{state=}', f'{output_state=}')
    return output_state

def node_b(state: State) -> State:
    output_state: State = State(nodes_path=['B'], current_number=state.current_number)
    print('> node_b', f'{state=}', f'{output_state=}')
    return output_state

def node_c(state: State) -> State:
    output_state: State = State(nodes_path=['C'], current_number=state.current_number)
    print('> node_c', f'{state=}', f'{output_state=}')
    return output_state

def the_conditional(state: State) -> Literal["goes_to_b", "goes_to_c"]:
    if state.current_number >= 50:
        return 'goes_to_c'
    return 'goes_to_b'

# Definir o builder do grafo
builder = StateGraph(State)

builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)

# Conectar as edges (ou arestas)
builder.add_edge('__start__', "A")
builder.add_conditional_edges(
    "A", the_conditional, {'goes_to_b': 'B', 'goes_to_c': 'C'}
    )
builder.add_edge('B', '__end__')
builder.add_edge('C', '__end__')

# compilar grafo
graph = builder.compile()

# Para gerar um PPNG do Grafo
# graph.get_graph().draw_mermaid_png(output_file_path="file.png")

# Para printar o código do grafo e colocar no mermaid
print(graph.get_graph().draw_mermaid())

# Pegar o resultado
print()
response = graph.invoke(State(nodes_path=[]))
print(f'{response=}')
print()


print()
response2 = graph.invoke(State(nodes_path=[], current_number=52))
print(f'{response2=}')
print()