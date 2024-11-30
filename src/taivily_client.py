from tavily import AsyncTavilyClient
import asyncio
from typing import List, Dict, Optional
import os

class SearchClient:
    def __init__(self,api_key: str):
        """
        Tavily検索クライアントの初期化
        
        Args:
            api_key: TavilyのAPIキー
        """
        self.client = AsyncTavilyClient(api_key)

    async def search(self, 
               query: str, 
               search_depth: str = "basic",
               include_images: bool = False,
               include_answer: bool = True,
               max_results: int = 5) -> Dict:
        """
        検索を実行します
        
        Args:
            query: 検索クエリ
            search_depth: 検索の深さ ("basic" or "advanced")
            include_images: 画像結果を含めるかどうか
            include_answer: AI生成の回答を含めるかどうか
            max_results: 返す結果の最大数
            
        Returns:
            検索結果を含む辞書
        """
        try:
            response = await self.client.search(
                query=query,
                search_depth=search_depth,
                include_images=include_images,
                include_answer=include_answer,
                max_results=max_results
            )
            return response
        except Exception as e:
            print(f"検索エラーが発生しました: {e}")
            raise RuntimeError(f"回答生成エラーが発生しました: {e}")

    async def qna_search(self,
                        query: str,
                        search_depth: str = "advanced",
                        topic: str = "general",
                        max_results: int = 5) -> str:
        """
        検索を実行し、質問に対する直接的な回答を返します
        
        Args:
            query: 質問文
            search_depth: 検索の深さ ("basic" or "advanced")
            topic: 検索カテゴリ ("general" or "news")
            max_results: 返す結果の最大数
            
        Returns:
            質問に対する回答の文字列
        """
        try:
            answer = await self.client.qna_search(
                query=query,
                search_depth=search_depth,
                topic=topic,
                max_results=max_results
            )
            return answer
        except Exception as e:
            print(f"QnA検索エラーが発生しました: {e}")
            raise RuntimeError(f"QnA検索エラーが発生しました: {e}")

async def main():
    # APIキーを設定
    API_KEY = os.getenv("TAVILY_API_KEY")
    if not API_KEY:
        print("TAVILY_API_KEY environment variable not found")
        raise ValueError("TAVILY_API_KEY environment variable required")
    client = SearchClient(API_KEY)
    
    # 検索例
    query = "量工知能は社会にどのような影響を与えますか？"
    
    # 基本的な検索
    print("基本的な検索結果:")
    results = await client.search(query)
    if results:
        # AI生成の回答を表示
        if 'answer' in results:
            print("\nAI回答:")
            print(results['answer'])
        
        # 検索結果を表示
        print("\n検索結果:")
        for i, result in enumerate(results.get('results', []), 1):
            print(f"\n{i}. {result.get('title', 'タイトルなし')}")
            print(f"URL: {result.get('url', 'URLなし')}")
            print(f"概要: {result.get('snippet', '概要なし')}")
    
    # qna_searchの使用例
    print("\n\nQnA検索:")
    answer = await client.qna_search(
        "気候変動対策として何ができますか？"
    )
    print(f"回答: {answer}")

if __name__ == "__main__":
    asyncio.run(main())
