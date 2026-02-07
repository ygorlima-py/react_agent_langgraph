# Aprendizado de LangChain e LangGraph

## Estrutura do repositório

```
.
├── docs/               # Textos de apoio (um por aula)
│   ├── 001-*.md
│   ├── 002-*.md
│   └── ...
├── src/examples/       # Exemplos de código (um por aula)
│   ├── ex001/
│   ├── ex002/
│   └── ...
├── pyproject.toml      # Dependências (uv)
└── uv.lock
```

## Como rodar os exemplos

Este projeto usa [uv](https://docs.astral.sh/uv/) para gerenciar dependências.

### Instalar dependências

```bash
uv sync
```

### Rodar exemplos

Você precisa criar o seu arquivo `.env`.

```bash
uv run --env-file=".env" src/examples/ex001/main.py
```
