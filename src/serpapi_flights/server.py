"""SerpAPI Google Flights MCP server entry point."""

import os
from .tools import mcp


def main():
    """Run the MCP server. Supports both local (stdio) and remote (HTTP) transport."""
    transport = os.getenv("MCP_TRANSPORT", "http")
    host = os.getenv("MCP_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("MCP_PORT", "8000")))

    if transport == "http":
        mcp.run(transport="http", host=host, port=port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
