from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage, AIMessage
from langgraph.graph.state import RunnableConfig
from langchain_core.tracers.stdout import FunctionCallbackHandler
from rich import print
from rich.prompt import Prompt
from rich.markdown import Markdown
from examples.ex007.prompts import SYSTEM_PROMPT
from examples.ex007.graph import build_graph
from typing import Literal

print()

def main() -> None:
    graph = build_graph()

    fn_handler_cb = FunctionCallbackHandler(function=print)
    user_type: Literal["plus", "enterprise"] = "plus"
    config = RunnableConfig(
        configurable={"thread_id": 1, "user_type": user_type },
        run_name="meu_grafo",
        tags=["enterprise"],
        max_concurrency=4,
        recursion_limit=25,
        callbacks=[fn_handler_cb],
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

        result = graph.invoke({'messages': current_loop_message}, config=config)

        model_name = ""
        last_message = result["messages"][-1]
        if isinstance(last_message, AIMessage ):
            model_name = last_message.response_metadata.get("model_name", "")

        # print(f"[bold cyan]RESPOSTA ({model_name}): \n")
        # print(Markdown(result["messages"][-1].content))
        # print(Markdown("\n\n --- \n\n"))

        all_messages = result["messages"]
    
    # print(all_messages)



if __name__ == "__main__":
    main()