# MCP-Server-Implementations

Custom Model Context Protocol (MCP) server implementations that expose MongoDB database operations and Tavily web search as tools consumable by any MCP-compatible LLM client, including Claude Desktop.

## Overview

The Model Context Protocol establishes a standard for connecting AI systems to local data sources and external services without requiring custom REST integrations per application. This repository contains two MCP server implementations built with `FastMCP` (stdio transport), demonstrating how to expose database operations and web search capabilities as native LLM tools. Both servers are designed to be consumed by the `ADK_Multi_Agent` system in the companion `AI-Agentic-Workflows` repository and by Claude Desktop.

## Modules

### `MongodbMCP/`

A fully-featured FastMCP server for MongoDB. Exposes the following MCP tools:

*   `list_databases`: List all databases on the connected MongoDB server.
*   `list_collections`: List all collections within a specified database.
*   `set_database`: Dynamically switch the active database at runtime.
*   `set_collection`: Set the active collection within the current database.
*   `collection_operations`: A unified CRUD tool supporting `find`, `insert`, `update`, `delete`, `count`, and `distinct` operations with query and document arguments.
*   `tavily`: A web search tool backed by the Tavily REST API, allowing the connected LLM to perform internet searches from within the same MCP session.

The server connects to a local MongoDB instance (`mongodb://localhost:27017/`) with the `car` database and `car_data` collection as defaults, switchable at runtime via `set_database` and `set_collection`.

### `claudemcp/`

A lightweight FastMCP server serving as the foundational starter template and integration reference for Claude Desktop MCP configuration. Contains the minimal `add` tool and commented-out MongoDB integration scaffolding showing the initial prototype before the full `MongodbMCP` server was built. The `mcp-server-basic/` subdirectory contains the minimal single-file prototype.

## Technology Stack

*   **Language:** Python 3.10+
*   **Protocol:** Model Context Protocol — FastMCP (`mcp.server.fastmcp`)
*   **Transport:** stdio (standard for Claude Desktop and ADK integrations)
*   **Database:** MongoDB (`pymongo`)
*   **Web Search:** Tavily REST API
*   **Package Manager:** `uv` (pyproject.toml-based)

## Prerequisites

1.  Python 3.10 or higher.
2.  A running local MongoDB instance (`mongod` on default port 27017).
3.  Claude Desktop installed with MCP host configuration enabled (if integrating via Claude).
4.  `uv` package manager for dependency resolution.

## Setup and Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/AbinashBalaraman/MCP-Server-Implementations.git
    cd MCP-Server-Implementations
    ```

2.  Install dependencies using `uv`:
    ```bash
    cd MongodbMCP
    uv sync
    ```

3.  Configure environment variables:
    ```env
    MONGODB_URI="mongodb://localhost:27017/"
    TAVILY_API_KEY="your_tavily_key_here"
    ```

4.  Claude Desktop Configuration:
    Update your `claude_desktop_config.json` to register the MCP server:
    ```json
    {
      "mcpServers": {
        "MongodbMCP": {
          "command": "python",
          "args": ["path/to/MongodbMCP/main.py"]
        }
      }
    }
    ```

## Usage

To start the MongoDB MCP server manually:

```bash
cd MongodbMCP
python main.py
```

The server initializes its stdio transport layer and waits for MCP initialization payloads from the connected client. It is typically spawned automatically by Claude Desktop or the ADK runtime, not run interactively.

## Security Considerations

These servers execute real database operations based on LLM-generated queries. In production environments, apply strict MongoDB read-only RBAC on connection credentials and validate all `collection_operations` inputs to prevent unintended destructive operations.

## License

Standard MIT License applies.
