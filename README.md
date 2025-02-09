# tavily-search MCP server

A MCP server project

<a href="https://glama.ai/mcp/servers/s0hka6zney"><img width="380" height="200" src="https://glama.ai/mcp/servers/s0hka6zney/badge" alt="tavily-search MCP server" /></a>

## Components

This server uses the Tavily API to perform searches based on specified queries.
- Search results are returned in text format.
- Search results include AI responses, URIs, and titles of the search results.

### Tools

This server implements the following tools:
- search: Performs searches based on specified queries
  - Required argument: "query"
  - Optional argument: "search_depth" (basic or advanced)

### Installing via Smithery

To install Tavily Search for Claude Desktop automatically via [Smithery](https://smithery.ai/server/tavily-search):

```bash
npx -y @smithery/cli install tavily-search --client claude
```

### Install

1. Download the repository.
```bash
git clone https://github.com/Tomatio13/mcp-server-tavily.git
``` 
2. Open the Claude Desktop configuration file.
```
On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `C:\Users\[username]\AppData\Roaming\Claude\claude_desktop_config.json`
```

3. Edit the configuration file as follows:
  ```yaml
  "mcpServers": {
    "tavily-search": {
      "command": "uv",
      "args": [
        "--directory",
        "C:\\your_path\\mcp-server-tavily",
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

4. Restart Claude Desktop.

## Usage

In Claude Desktop, when you ask "Please search for something", you will receive search results.

Search example:
```
Please search in detail for today's events in Kamakura
```
Response example:
```
According to the search results, the following events start today, December 1st:
"Kamakura Promotion Photo Contest 2025"
Period: December 1, 2024 - January 31, 2025
A photo contest for those who love Kamakura
Applications start accepting from today
Also, as a related upcoming event:
On December 7th, an exhibition by 12 Kamakura artists will be held at the Seibu Press Inn Kamakura Ofuna Station East Exit Lounge.
```

## Log Storage Location

Logs are stored in the following location:

For Windows:
```
C:\Users\[username]\AppData\Roaming\Claude\logs\mcp-server-tavily-search
```
## Execution with Cursor

1. Create a shell script (e.g., `script.sh`) as shown below:

```bash
#!/bin/bash
TARGET_DIR=/path/to/mcp-server-tavily
cd "${TARGET_DIR}"
export TAVILY_API_KEY="your-api-key"
export PYTHONIOENCODING=utf-8
uv --directory $PWD run tavily-search
```

2. Configure Cursor's MCP Server settings as follows:

```
Name: tavily-search
Type: command
Command: /path/to/your/script.sh
```

3. Save the settings.

4. Once the settings are saved, you can ask Cursor's Composer-Agent to "search for something," and it will return the search results.

## Running in Local Environment Using Docker Compose

### Purpose
For operating systems other than Windows/MacOS where Claude Desktop cannot be used,
this section explains how to set up and run an MCP server and client in a local environment
using Docker compose.

### Steps
1. Install Docker.
2. Download the repository.
```bash
git clone https://github.com/Tomatio13/mcp-server-tavily.git
``` 
3. Run Docker compose.
```bash
docker compose up -d
``` 
4. Execute the client.
```bash
docker exec mcp_server uv --directory /usr/src/app/mcp-server-tavily/src run client.py
```
5. Execution Results
6. After searching for available tools as shown below, a query will be issued to Tavily and a response will be returned:
```bash
2024-12-01 11:21:56,930 - tavily-search-server - INFO - Starting Tavily search server
2024-12-01 11:21:56,932 - tavily-search-server - INFO - Server initialized, starting main loop
2024-12-01 11:21:56,936 - mcp.server - INFO - Processing request of type ListToolsRequest
2024-12-01 11:21:56,936 - tavily-search-server - INFO - Listing available tools
利用可能なツール: nextCursor=None tools=[Tool(name='search', description='Search the web using Tavily API', inputSchema={'type': 'object', 'properties': {'query': {'type': 'string', 'description': 'Search query'}, 'search_depth': {'type': 'string', 'description': 'Search depth (basic or advanced)', 'enum': ['basic', 'advanced']}}, 'required': ['query']})]
2024-12-01 11:21:56,937 - mcp.server - INFO - Processing request of type CallToolRequest
2024-12-01 11:21:56,937 - tavily-search-server - INFO - TOOL_CALL_DEBUG: Tool called - name: search, arguments: {'query': '今日の東京タワーのイベントを教えて下さい'}
2024-12-01 11:21:56,937 - tavily-search-server - INFO - Executing search with query: '今日の東京タワーのイベントを教えて下さい'
2024-12-01 11:22:00,243 - httpx - INFO - HTTP Request: POST https://api.tavily.com/search "HTTP/1.1 200 OK"
2024-12-01 11:22:00,243 - tavily-search-server - INFO - Search successful - Answer generated
2024-12-01 11:22:00,243 - tavily-search-server - INFO - Search successful - Results available
ツール実行結果: content=[TextContent(type='text', text='AI Answer:\n今日の東京タワーのイベントは以下の通りです：\n1. Candlelight: エド・シーランとコールドプレイのヒットメドレー - 12月01日\n2. チームラボプラネッツ TOKYO - 12月01日から1月21日\n\n他にもイベントがある可能性がありますので、公式ウェブサイト等で最新情報をご確認ください。\n\n\n\nSearch Results:\n\n1. 東京タワー (東京): 現在のイベントとチケット | Fever\nURL: https://feverup.com/ja/tokyo/venue/tokyo-tower\nSummary: Summary not found\n\n\n2. 東京タワー(東京都)の施設で開催するイベント一覧｜ウォーカープラス\nURL: https://www.walkerplus.com/spot/ar0313s03867/e_list.html\nSummary: Summary not found\n\n\n3. 東京タワー - Tokyo Tower\nURL: https://www.tokyotower.co.jp/event/\nSummary: Summary not found\n')] isError=False
``` 
