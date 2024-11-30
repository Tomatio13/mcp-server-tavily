# tavily-search MCP server

A MCP server project

## Components

This server uses the Tavily API to perform searches based on specified queries.
- Search results are returned in text format.
- Search results include AI-generated answers, URIs, and titles of the search results.

### Tools

This server implements the following tools:
- search: Performs searches based on specified queries
  - Required argument: "query"
  - Optional argument: "search_depth" (basic or advanced)

### Install

1. Download the repository.
```bash
git clone https://github.com/Tomatio13/mcp-server-tavily.git
```
2. Open the Claude Desktop configuration file.

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

3. Edit the configuration file as follows:
  ```yaml
  "mcpServers": {
    "tavily-search": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\your_path\\tavily_search",
        "run",
        "tavily-search"
      ],
      "env": {
        "TAVILY_API_KEY": "YOUR_TAVILY_API_KEY",
        "PYTHONIOENCODING": "utf-8"
      }
    }
  }
  ```
## Usage

In Claude Desktop, when you ask "Please search for something", it will return search results.

Search example:
```
Please search for today's events in Kamakura in detail
```
Response example:
```
According to the search results, the following events start today, December 1st:
"Kamakura Promotion Photo Contest 2025"
Period: December 1, 2024 - January 31, 2025
A photo contest for those who love Kamakura
Applications start accepting from today
Also, for upcoming related events:
On December 7th, an exhibition by 12 Kamakura artists will be held at the Seibu Press Inn Kamakura Ofuna Station East Exit Lounge.
```