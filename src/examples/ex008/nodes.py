from langchain_core.runnables.config import RunnableConfig
from examples.ex008.state import State
from examples.ex008.utils import load_llm, load_llm_google
from examples.ex008.tools import TOOLS
from langgraph.prebuilt.tool_node import ToolNode

tool_node = ToolNode(tools=TOOLS)

def call_llm(state: State, config: RunnableConfig) -> State:
    print('>Call LLM')
    user_type = config.get("configurable", {}).get('user_type')
    temperature = 1 if user_type == 'plus' else 0
    model_provider = "google_genai" if user_type == 'plus' else "openai"
    model = "gemini-2.0-flash" if user_type == 'plus' else "gpt-4.1-mini"
    

    llm_with_tools = load_llm().bind_tools(TOOLS) # carrego a llm com as ferramentas tools
    llm_with_config = llm_with_tools.with_config(
        config={"configurable": {
            "mdodel": model_provider,
            "model_provider": model,
            "temperature": temperature,
            }
        }
    )

    print(llm_with_config.temperature)

    result = llm_with_config.invoke(
        state["messages"],
        ) # Aqui ja tenho a llm com as ferramentas carregadas
    
    return {'messages': [result]}