from langchain_core.runnables.config import RunnableConfig
from examples.ex009.state import State
from examples.ex009.utils import load_llm, load_llm_google
from examples.ex009.tools import TOOLS
from langgraph.prebuilt.tool_node import ToolNode
from langgraph.runtime import Runtime
from examples.ex009.context import Context
from rich import print


tool_node = ToolNode(tools=TOOLS)

def call_llm(state: State, runtime: Runtime[Context]) -> State:
    print('>Call LLM')
    context = runtime.context
    user_type = context.user_type 
    
    print('Runtime', runtime)
    print('Contexto', context)
    print('user_type', user_type)

    model_provider = "google_genai" if user_type == 'plus' else "openai"
    model = "gemini-2.0-flash" if user_type == 'plus' else "gpt-4.1-mini"
    

    llm_with_tools = load_llm().bind_tools(TOOLS) # carrego a llm com as ferramentas tools
    llm_with_config = llm_with_tools.with_config(
        config={"configurable": {
            "mdodel": model_provider,
            "model_provider": model,
            }
        }
    )

    print(llm_with_config.temperature)

    result = llm_with_config.invoke(
        state["messages"],
        ) # Aqui ja tenho a llm com as ferramentas carregadas
    
    return {'messages': [result]}