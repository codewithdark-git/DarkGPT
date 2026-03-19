"""
Trading session filter — only trade during high-liquidity windows.
"""

from datetime import datetime, timezone
import config


def in_trading_session() -> bool:
    """Returns True if current UTC hour falls inside a configured session."""
    now_hour = datetime.now(timezone.utc).hour
    for start, end in config.TRADE_SESSIONS:
        if start <= now_hour < end:
            return True
    return False
