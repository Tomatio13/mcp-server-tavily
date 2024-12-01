from . import server
import asyncio

def main():
    """パッケージのエントリポイント"""
    try:
        asyncio.run(server.main())
    except KeyboardInterrupt:
        server.logger.info("Server shutdown requested")
    except Exception as e:
        server.logger.error(f"Server error: {e}", exc_info=True)
        raise

__all__ = ['main', 'server']