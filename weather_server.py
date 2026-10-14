### File: weather_server.py
### Date: 2026-09-30

import asyncio

from mcp.server.mcpserver import MCPServer


mcp = MCPServer("weather-server")


@mcp.tool()
def get_weather(city_state: str) -> str:
    """Return a weather lookup response for a US city and state."""
    return f"MCP server received the location: {city_state}"


if __name__ == "__main__":
    asyncio.run(mcp.run_stdio_async())