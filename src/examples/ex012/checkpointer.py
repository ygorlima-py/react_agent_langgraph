from contextlib import asynccontextmanager
from typing import AsyncGenerator
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

def build_checkpointer() -> InMemorySaver:
    return InMemorySaver()

""" 
Aqui fazemos a conexão com o banco de dados, nesse caso estamos usando Postgre.
A comunicação deve ser assincrona por isso usamos await no retorno da chamada
"""
@asynccontextmanager
async def build_checkpointer_psql(db_dsn: str) -> AsyncGenerator[AsyncPostgresSaver]:
    async with AsyncPostgresSaver.from_conn_string(db_dsn) as checkpointer:
        await checkpointer.setup() # Cria a tabela
        yield checkpointer