import asyncio
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage, AIMessage
from langgraph.graph.state import RunnableConfig
from langchain_core.tracers.stdout import FunctionCallbackHandler
from rich import print
from rich.prompt import Prompt
from rich.markdown import Markdown
from examples.ex010.checkpointer import build_checkpointer
from examples.ex010.prompts import SYSTEM_PROMPT
from examples.ex010.graph import build_graph
from examples.ex010.context import Context
from examples.ex010.utils import Connection, async_lifespan, sync_lifespan


print()

async def init_graph(connection: Connection) -> None:
    checkpointer = build_checkpointer(connection)
    graph = build_graph(checkpointer=checkpointer)

    context = Context(user_type='plus')
    
    config = RunnableConfig(
        # Fix Me user_type
        configurable={"thread_id": 1, },
        )

    all_messages: list[BaseMessage] = []

    prompt = Prompt()
    Prompt.prompt_suffix = ""

    while True:
        user_input = prompt.ask("[bold cyan]Você: \n")
        print(Markdown("\n\n --- \n\n"))

        if user_input.lower() in ['q', 'quit', 'exit', 'sair']:
            break

        human_message = HumanMessage(user_input)
        current_loop_message = [human_message]

        if len(all_messages) == 0:
            current_loop_message = [SystemMessage(SYSTEM_PROMPT), human_message]

        result = graph.invoke({'messages': current_loop_message}, config=config, context=context)

        model_name = ""
        last_message = result["messages"][-1]
        if isinstance(last_message, AIMessage ):
            model_name = last_message.response_metadata.get("model_name", "")

        print(f"[bold cyan]RESPOSTA ({model_name}): \n")
        print(Markdown(last_message.text))
        print(last_message)
        print(Markdown("\n\n --- \n\n"))

        all_messages = result["messages"]
    
    print(graph.get_state(config=config))


async def main() -> None:
   async with async_lifespan() as connection:      
        await init_graph(connection)
    

if __name__ == "__main__":
    asyncio.run(main())