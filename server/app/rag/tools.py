from langchain.tools import tool
from app.core.electricity_price import get_electricity_price

@tool("get_live_electricity_price", return_direct=True)
def get_live_electricity_price_tool(location: str = "Germany") -> str:
    """
    Returns the latest available electricity price (EUR/kWh) for the given location.
    """
    price = get_electricity_price()
    return f"The latest electricity price in {location} is €{price:.3f} per kWh."
