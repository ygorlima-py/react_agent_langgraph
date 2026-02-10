# Comandos

## instalar o langgraph-cli

```
uv add "langgraph-cli[inmem]"

```

## Verificar comandos 

```
uv run langgraph --help

```

## Crie um arquivo JSON com as sequintes informações

```
{
  "$schema": "https://langgra.ph/schema.json",
  "graphs": {
    "grafo": "src/examples/ex006/graph.py:build_graph"
  },
  "env": ".env",
  "python_version": "3.13",
  "dependencies": ["."]
}
```

--> "grafo": Caminho da função que faz o build do grafo

## Configuração do LangGraph

```
uv run langgraph dev --config src/examples/ex006/langgraph.json
```


