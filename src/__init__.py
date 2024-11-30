from . import server
import asyncio

def main():
    """パッケージのエントリポイント"""
    asyncio.run(server.main())

__all__ = ['main', 'server']