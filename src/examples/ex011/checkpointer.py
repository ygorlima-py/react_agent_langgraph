from langgraph.checkpoint.memory import InMemorySaver
from examples.ex011.utils import Connection


def build_checkpointer(connection: Connection) -> InMemorySaver:
    connection.use()
    return InMemorySaver()