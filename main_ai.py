# ---
# DETAILS:
#   title: AI Agent
#   author: Andrew Seamana
#   date: 2026-09-23
# ---



# ---
# Copied from: 'https://byuidatascience.github.io/agentic_ai_course/lessons/lesson1_4.html'
#
# def get_response(prompt: str) -> str:
#     return prompt

# def main():
#     while True:
#         try:
#             prompt = input("Input: ")
#             if prompt == "exit": break
#             response = get_response(prompt)
#         except EOFError:
#             break
#         print(response)

# if __name__ == "__main__":
#     main()
# ---

# ---
# Copied from: Took code (commented out) from `Example1_2.ipynb` and AI changed.
#
# import os
# from google.colab import userdata
# os.environ["GOOGLE_API_KEY"] = userdata.get("GOOGLE_API_KEY")
# ---



# --- Imports
import json
import os
import asyncio
from datetime import date
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY is not set")
# ---



# --- Tools
# Idea: Perhaps I could set up a function called `pull_weather_data` or something and provide to the tool as a function call it can use to pull the data for the user provided city (input) and restate the data as a more user-friendly output.

def get_weather(city_state: str, forecast_date: str | None = None) -> str:
    """Get the weather for a US city and state, optionally on YYYY-MM-DD."""
    if forecast_date is None:
        forecast_date = date.today().isoformat()

    try:
        date.fromisoformat(forecast_date)
    except ValueError as exc:
        raise ValueError("forecast_date must use YYYY-MM-DD format") from exc

    geocode_query = urlencode({
        "name": city_state,
        "count": 1,
        "language": "en",
        "format": "json",
        "countryCode": "US",
    })
    with urlopen(
        f"https://geocoding-api.open-meteo.com/v1/search?{geocode_query}"
    ) as response:
        locations = json.load(response).get("results", [])

    if not locations:
        return f"I could not find a US location matching {city_state}."

    location = locations[0]
    forecast_query = urlencode({
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "temperature_unit": "fahrenheit",
        "timezone": "auto",
        "start_date": forecast_date,
        "end_date": forecast_date,
    })
    with urlopen(
        f"https://api.open-meteo.com/v1/forecast?{forecast_query}"
    ) as response:
        forecast = json.load(response)

    daily = forecast.get("daily", {})
    if not daily.get("time"):
        return f"No forecast is available for {forecast_date}."

    return (
        f"Weather for {location['name']}, {location.get('admin1', 'US')} on {forecast_date}: "
        f"high {daily['temperature_2m_max'][0]}°F, "
        f"low {daily['temperature_2m_min'][0]}°F, "
        f"precipitation chance {daily['precipitation_probability_max'][0]}%."
    )
# ---



# --- Agent Construction and Execution
from langchain.mcp import MCPAdapter
from langchain.agents import create_agent # Copied from: 'https://docs.langchain.com/oss/python/langchain/overview'
from langchain.messages import HumanMessage # (Line copied from `Example1_2.ipynb`)


async def main() -> None:
    async with MCPAdapter(Path("weather_server.py")) as adapter:
        tools = await adapter.list_tools()
        print(len(tools), "MCP tools")
        for tool in tools:
            print(tool.name)

        agent = create_agent(
            model="google_genai:gemini-3.6-flash",
            tools=[get_weather, *tools],
            system_prompt="You are a helpful assistant",
        )

        prompt = HumanMessage(input("Input (city, state): "))
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": prompt.content}]}
        )

        print(result["messages"][-1].text)


if __name__ == "__main__":
    asyncio.run(main())
# ---




