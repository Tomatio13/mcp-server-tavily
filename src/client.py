from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import os
async def main():
    # サーバーパラメータの設定
    server_params = StdioServerParameters(
        command="/usr/local/bin/uv",  # server.pyへのパス
        args=[
            "--directory",
            "/usr/src/app/mcp-server-tavily",
            "run",
            "tavily-search"
        ],  # コマンドライン引数（必要に応じて）
        env={
            "TAVILY_API_KEY": os.getenv("TAVILY_API_KEY"),
            "PYTHONIOENCODING": "utf-8"
        }  # 環境変数（必要に応じて）
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # セッションの初期化
            await session.initialize()

            try:
                # 利用可能なツールの一覧を取得
                tools = await session.list_tools()
                print(f"利用可能なツール: {tools}")

                # ツールの呼び出し例
                tool_result = await session.call_tool(
                    "search",
                    arguments={"query": "今日の東京タワーのイベントを教えて下さい"}
                )
                print(f"ツール実行結果: {tool_result}")

            except Exception as e:
                print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    asyncio.run(main())
