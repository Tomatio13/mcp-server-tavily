from tavily import AsyncTavilyClient
import asyncio
from typing import List, Dict, Optional

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

    async def get_answer(self, query: str) -> Dict:
        """
        質問に対する直接的な回答を取得します
        
        Args:
            query: 質問文
            
        Returns:
            回答を含む辞書
        """
        try:
            response = await self.client.search(
                query=query,
                search_depth="basic",
                include_answer=True,
                max_results=3
            )
            return {
                'answer': response.get('answer', '回答が見つかりませんでした'),
                'context': response.get('context', []),
                'sources': response.get('results', [])
            }
        except Exception as e:
            print(f"回答生成エラーが発生しました: {e}")
            raise RuntimeError(f"回答生成エラーが発生しました: {e}")

async def main():
    # APIキーを設定
    API_KEY = os.getenv("TAVILY_API_KEY")
    if not API_KEY:
        logger.error("TAVILY_API_KEY environment variable not found")
        raise ValueError("TAVILY_API_KEY environment variable required")
    client = SearchClient(API_KEY)
    
    # 検索例
    query = "量子コンピュータの仕組みについて教えてください"
    
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
    
    # 詳細な回答を取得
    print("\n\n詳細な回答:")
    answer = await client.get_answer("人工知能は社会にどのような影響を与えますか？")
    if answer:
        print(f"回答: {answer['answer']}")
        print("\n参照元:")
        for source in answer['sources']:
            print(f"- {source.get('title', 'タイトルなし')}: {source.get('url', 'URLなし')}")

if __name__ == "__main__":
    asyncio.run(main())
