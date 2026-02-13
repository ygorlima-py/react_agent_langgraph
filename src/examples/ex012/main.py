import asyncio
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage, AIMessage
from langgraph.graph.state import RunnableConfig
from rich import print
from rich.prompt import Prompt
from rich.markdown import Markdown
from examples.ex012.checkpointer import build_checkpointer, build_checkpointer_psql
from examples.ex012.constants import DB_DSN
from examples.ex012.prompts import SYSTEM_PROMPT
from examples.ex012.graph import build_graph
from examples.ex012.context import Context
from examples.ex012.utils import  async_lifespan
from langgraph.checkpoint.base import BaseCheckpointSaver



print()

async def init_graph(checkpointer: BaseCheckpointSaver) -> None:
    graph = build_graph(checkpointer=checkpointer)

    context = Context(user_type='plus')
    
    config = RunnableConfig(
        # Fix Me user_type
        configurable={"thread_id": 1},
        )

    prompt = Prompt()
    Prompt.prompt_suffix = ""

    while True:
        user_input = prompt.ask("[bold cyan]Você: \n")
        print(Markdown("\n\n --- \n\n"))

        if user_input.lower() in ['q', 'quit', 'exit', 'sair']:
            break

        human_message = HumanMessage(user_input)
        current_loop_message = [human_message]

        # if len(all_messages) == 0:
        #     current_loop_message = [SystemMessage(SYSTEM_PROMPT), human_message]

        result = await graph.ainvoke({'messages': current_loop_message}, config=config, context=context)

        model_name = ""
        last_message = result["messages"][-1]
        if isinstance(last_message, AIMessage ):
            model_name = last_message.response_metadata.get("model_name", "")

        print(f"[bold cyan]RESPOSTA ({model_name}): \n")
        print(Markdown(last_message.text))
        print(last_message)
        print(Markdown("\n\n --- \n\n"))

        all_messages = result["messages"]
    
    print(await graph.aget_state(config=config))


async def main() -> None:
   async with (
       async_lifespan(),
       build_checkpointer_psql(DB_DSN) as checkpointer 
       ):
       await init_graph(checkpointer)
      

if __name__ == "__main__":
    asyncio.run(main())