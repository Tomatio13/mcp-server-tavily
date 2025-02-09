# tavily-search MCP server

A MCP server project

## Components

このサーバは、TavilyのAPIを使用して、指定されたクエリに基づいて検索を行います。
- 検索結果は、テキスト形式で返されます。
- 検索結果には、AIによる回答と、検索結果のURI、タイトルが含まれます。

### Tools

このサーバは、以下のツールを実装しています。
- search: 指定されたクエリに基づいて検索を行います
  - 必須の引数: "query"
  - オプションの引数: "search_depth" (basic or advanced)"

### Install

1. リポジトリをダウンロードしてください。
```bash
git clone https://github.com/Tomatio13/mcp-server-tavily.git
``` 
2. Claude Desktopの設定ファイルを開いてください。
```
On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `C:\Users\[ユーザ名]\AppData\Roaming\Claude\claude_desktop_config.json`
```

3. 以下のように設定ファイルを編集してください。
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

4. Claude Desktopを再起動してください。

## 使用方法

Claude Desktopで、`なになにを検索して下さい`と話しかけると、検索結果が返されます。

検索例:
```
今日の鎌倉のイベントを詳しく検索してください
```
回答例:
```
検索結果によると、今日12月1日から以下のイベントが始まります：
「鎌倉プロモーションフォトコンテスト2025」
期間：2024年12月1日～2025年1月31日
鎌倉を愛する方々を対象とした写真コンテスト
応募受付が本日からスタート
また、近日開催される関連イベントとして：
12月7日に鎌倉の12人のアーティストによる作品展示が、西武プレスイン鎌倉大船駅東口ラウンジにて開催される予定です。
```

## ログの格納場所

以下にログが格納されます。

Windowsの場合:
```
C:\Users\[ユーザ名]\AppData\Roaming\Claude\logs\mcp-server-tavily-search
```

## Cursorでの実行

1. 以下のようなシェルスクリプト(例.script.sh)を作成してください。

```bash
#!/bin/bash
TARGET_DIR=/path/to/mcp-server-tavily
cd "${TARGET_DIR}"
export TAVILY_API_KEY="your-api-key"
export PYTHONIOENCODING=utf-8
uv --directory $PWD run tavily-search
```

2. CurosorのMCP Serverの設定画面で以下のように設定してください。

```
Name: tavily-search
Type: command
Command: /path/to/your/script.sh
```

3. 設定を保存してください。

4. 設定を保存したら、CursorのComposer-Agentで`なになにを検索して下さい`と話しかけると、検索結果が返されます。

## Docker composeを使用したローカル環境での実行

### 目的
Windows/MacOS以外の場合、Claude Desktopを使用できないため、
Docker composeを使用してローカル環境でMCPサーバとクライアントを構築するための
環境を構築・実行します。

### 手順
1. Dockerをインストールしてください。
2. リポジトリをダウンロードしてください。
```bash
git clone https://github.com/Tomatio13/mcp-server-tavily.git
``` 
3. Docker composeを実行してください。
```bash
docker compose up -d
``` 
4. クライアントを実行します。
```bash
docker exec mcp_server uv --directory /usr/src/app/mcp-server-tavily/src run client.py
```
5. 実行結果
6. 以下のようにあ利用可能なツールを検索した後、tavilyに対してqueryが発行され、応答が返されます。
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
