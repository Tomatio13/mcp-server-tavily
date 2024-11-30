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

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

3. 以下のように設定ファイルを編集してください。
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