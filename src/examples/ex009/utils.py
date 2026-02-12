from langchain_openai import ChatOpenAI
import os
import requests
from rich import print
from langchain.chat_models import init_chat_model, BaseChatModel
from typing import cast

def load_llm_google() -> BaseChatModel:

    model = cast(BaseChatModel, init_chat_model(
        model="gemini-2.5-flash",
        model_provider="google_genai",
        temperature=0.2, 
        configurable_fields=("temperature", ),
    ))

    assert hasattr(model, "bind_tools")
    assert hasattr(model, "invoke")
    assert hasattr(model, "with_config")

    return model

def load_llm() -> ChatOpenAI:
    
    return  ChatOpenAI(
            model="openrouter/aurora-alpha",
            api_key=os.getenv("OPENROUTER_API_KEY"), #type:ignore
            base_url="https://openrouter.ai/api/v1",
            temperature=0.2,
            )


def get_yahoo_cookie():
    cookie = None

    user_agent_key = "User-Agent"
    user_agent_value = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

    headers = {user_agent_key: user_agent_value}
    response = requests.get(
        "https://fc.yahoo.com", headers=headers, allow_redirects=True
    )

    if not response.cookies:
        raise Exception("Failed to obtain Yahoo auth cookie.")

    cookie = list(response.cookies)[0]

    return cookie

def get_yahoo_crumb(cookie):
    crumb = None

    user_agent_key = "User-Agent"
    user_agent_value = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"

    headers = {user_agent_key: user_agent_value}

    crumb_response = requests.get(
        "https://query1.finance.yahoo.com/v1/test/getcrumb",
        headers=headers,
        cookies={cookie.name: cookie.value},
        allow_redirects=True,
    )
    crumb = crumb_response.text

    if crumb is None:
        raise Exception("Failed to retrieve Yahoo crumb.")

    return crumb

def get_yahoo_values(symbol, cookie, crumb):
    r = requests.get(
                url=f'https://query2.finance.yahoo.com/v7/finance/quote?symbols={symbol}&crumb={crumb}',
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                cookies={cookie.name: cookie.value}
                )
    return r.json()


if __name__ == "__main__":
    cookie = get_yahoo_cookie()
    crumb = get_yahoo_crumb(cookie)
    result = get_yahoo_values("NVDA", cookie, crumb)
    print(result)

