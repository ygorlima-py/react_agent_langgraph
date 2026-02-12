from langchain.tools import tool, BaseTool
from langgraph.prebuilt.tool_node import ToolRuntime
import requests
from examples.ex009.context import Context
from examples.ex009.state import State


@tool
def get_price_ticket(symbol: str, tool_runtime: ToolRuntime[Context, State]) -> dict:
    """
    this function request for api yahoo
    finance with ticket symbol and return timestamp
    and price of ticket in a period one year

    Args:
    symbol: str symbol name ticket, exp NVDA, PLTR

    Returns
    The resulting a dict with two list timestamp and price
    """ 
    

    params = {
        "range": "5y",
        "interval": "1mo",
        "modules": "price,summaryDetail,defaultKeyStatistics,financialData,assetProfile",
    }



    r = requests.get(
                url=f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}',
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
                params=params,
                )
    
    
    data = r.json()


    symbol_ticket = data['chart']['result'][0]['meta']['symbol']
    long_name = data['chart']['result'][0]['meta']['longName']
    regular_market_volume = data['chart']['result'][0]['meta']['regularMarketVolume']
    timestamp = data['chart']['result'][0]['timestamp']
    price = data['chart']['result'][0]['indicators']['quote'][0]['close']
    
    
    timestamp_clean = [x for x in timestamp if x is not None]
    price_clean = [y for y in price if y is not None]
    
    from rich import print
    
    print(tool_runtime)
    return {
        'symbol_ticket': symbol_ticket,
        'long_name': long_name,
        'regular_market_volume': regular_market_volume,
        'timestamp': timestamp_clean,
        'price': price_clean,
    }

TOOLS: list[BaseTool] = [get_price_ticket]
TOOLS_BY_NAME: dict[str, BaseTool] = {tool.name: tool for tool in TOOLS}


# if __name__ == "__main__":
    # result = get_price_ticket('PLTR')
    # print(result) 