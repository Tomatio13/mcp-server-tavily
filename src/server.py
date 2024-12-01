import os
import json
import logging
from datetime import datetime
from collections.abc import Sequence
from typing import Any, Optional
from tavily import AsyncTavilyClient
from dotenv import load_dotenv
from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    EmptyResult
)
from pydantic import AnyUrl
import asyncio

# 環境変数の読み込み
load_dotenv()

# ログの準備
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("tavily-search-server")

# APIキーの準備
API_KEY = os.getenv("TAVILY_API_KEY")
if not API_KEY:
    logger.error("TAVILY_API_KEY environment variable not found")
    raise ValueError("TAVILY_API_KEY environment variable required")

# サーバの準備
app = Server("tavily-search-server")

@app.list_resources()
async def list_resources() -> list[Resource]:
    logger.info("Listing available resources")
    resources = [
        Resource(
            uri=AnyUrl(f"websearch://query=`who is current Prime Minister of Japan 2024`,search_depth=`basic`"),
            name="Web Search about `who is current Prime Minister of Japan 2024`.\
                There are two types of search_depth: 'basic' and 'advanced', with 'advanced' searching deeper.'",
            mimeType="application/json",
            description="General web search using Tavily API"
        )
    ]
    logger.debug(f"Returning resources with full content: {resources}")
    return resources
    

# 利用可能なツール一覧の取得
@app.list_tools()
async def list_tools() -> list[Tool]:
    """利用可能なツールの一覧を返す"""
    logger.info("Listing available tools")
    tools = [
        Tool(
            name="search",
            description="Search the web using Tavily API",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "search_depth": {
                        "type": "string",
                        "description": "Search depth (basic or advanced)",
                        "enum": ["basic", "advanced"]
                    }
                },
                "required": ["query"]
            }
        )
    ]
    logger.debug(f"Returning tools: {tools}")
    return tools

# 検索結果を処理する関数
async def process_search_results(results: dict) -> TextContent:
    """検索結果を処理してTextContentを返す"""
    if not results:
        logger.warning("Empty search results received")
        return TextContent(
            type="text",
            text="No results were found for your query. Please try a different search term."
        )

    # 結果を格納する文字列を作成
    response_text = []

    # AI回答を追加
    if 'answer' in results and results['answer']:
        logger.info("Search successful - Answer generated")
        response_text.append("AI Answer:")
        response_text.append(results['answer'])
        response_text.append("\n")

    # 検索結果を追加
    if 'results' in results and results['results']:
        logger.info("Search successful - Results available")
        response_text.append("\nSearch Results:")
        for i, result in enumerate(results['results'], 1):
            response_text.append(f"\n{i}. {result.get('title', 'Title not found')}")
            response_text.append(f"URL: {result.get('url', 'URL not found')}")
            response_text.append(f"Summary: {result.get('snippet', 'Summary not found')}\n")

    if response_text:
        return TextContent(type="text", text="\n".join(response_text))
    
    logger.warning("No answer or results found in search results")
    return TextContent(
        type="text",
        text="The search was completed but no relevant information was found. Please try refining your query."
    )

# ツールの呼び出し
@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    """ツールを呼び出して結果を返す"""
    logger.info(f"TOOL_CALL_DEBUG: Tool called - name: {name}, arguments: {arguments}")
    
    if name != "search":
        logger.error(f"Unknown tool requested: {name}")
        return [TextContent(
            type="text",
            text=f"Error: Unknown tool '{name}'. Only 'search' is supported."
        )]

    if not isinstance(arguments, dict) or "query" not in arguments:
        logger.error(f"Invalid arguments provided: {arguments}")
        return [TextContent(
            type="text",
            text="Error: Invalid arguments. A 'query' parameter is required."
        )]

    try:
        client = AsyncTavilyClient(API_KEY)
        query = arguments["query"]
        
        logger.info(f"Executing search with query: '{query}'")

        search_task = client.search(
            query=query,
            search_depth=arguments.get("search_depth", "basic"),
            include_images=False,
            include_answer=True,
            max_results=3,
            topic="general"
        )

        try:
            # タイムアウトを設定して検索を実行
            results = await asyncio.wait_for(search_task, timeout=30.0)
            logger.debug(f"Raw search results: {results}")
            
            # 結果の処理
            return [await process_search_results(results)]

        except asyncio.TimeoutError:
            logger.error("Search operation timed out after 30 seconds")
            return [TextContent(
                type="text",
                text="The search operation timed out. Please try again with a more specific query or check your internet connection."
            )]
            
    except Exception as e:
        error_message = str(e)
        logger.error(f"Search failed: {error_message}", exc_info=True)
        
        # エラーメッセージをユーザーフレンドリー形式に変換
        if "api_key" in error_message.lower():
            return [TextContent(
                type="text",
                text="Authentication error occurred. Please check the API key configuration."
            )]
        elif "rate limit" in error_message.lower():
            return [TextContent(
                type="text",
                text="Rate limit exceeded. Please wait a moment before trying again."
            )]
        else:
            return [TextContent(
                type="text",
                text=f"An unexpected error occurred during the search. Please try again later. Error: {error_message}"
            )]

# メイン実行部分
async def main():
    logger.info("Starting Tavily search server")
    try:
        from mcp.server.stdio import stdio_server

        async with stdio_server() as (read_stream, write_stream):
            logger.info("Server initialized, starting main loop")
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )

    except Exception as e:
        logger.error(f"Server failed to start: {str(e)}", exc_info=True)
        raise

# エントリーポイント追加
if __name__ == "__main__":
    main_entry()

def main_entry():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        raise
