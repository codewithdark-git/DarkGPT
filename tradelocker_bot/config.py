"""
TradeLocker Bot Configuration
Atlas Funded Account - Conservative high win-rate settings
"""

# ─── TradeLocker API ──────────────────────────────────────────────────────────
TRADELOCKER_BASE_URL = "https://demo.tradelocker.com"  # change to live: https://live.tradelocker.com
API_EMAIL    = "your_email@example.com"
API_PASSWORD = "your_password"
API_SERVER   = "OSP-DEMO"   # your broker server name

# ─── Account / Risk ───────────────────────────────────────────────────────────
ACCOUNT_ID            = None        # auto-fetched on login
RISK_PER_TRADE_PCT    = 0.5         # 0.5 % of balance per trade  (Atlas safe)
MAX_DAILY_LOSS_PCT    = 2.0         # hard stop for the day       (Atlas rule)
MAX_TOTAL_DRAWDOWN_PCT = 4.0        # absolute drawdown ceiling   (Atlas rule)
MAX_OPEN_TRADES       = 2           # never stack more than 2 positions

# ─── Instruments to trade ─────────────────────────────────────────────────────
# Stick to the most liquid, tightest-spread pairs for best execution
SYMBOLS = ["EURUSD", "GBPUSD", "USDJPY"]

# ─── Timeframe ────────────────────────────────────────────────────────────────
TIMEFRAME       = "15"   # 15-minute bars  (best signal/noise for intraday)
CANDLES_NEEDED  = 100    # history bars to fetch per cycle

# ─── Strategy Parameters ──────────────────────────────────────────────────────
EMA_FAST   = 9
EMA_SLOW   = 21
RSI_PERIOD = 14
RSI_LONG   = 55     # RSI must be > this to take a long  (momentum filter)
RSI_SHORT  = 45     # RSI must be < this to take a short
ATR_PERIOD = 14
ATR_SL_MULT   = 1.5  # stop-loss  = ATR * this
ATR_TP_MULT   = 2.5  # take-profit = ATR * this   (R:R ≈ 1.67)

# ─── Session Filter ───────────────────────────────────────────────────────────
# Only trade during the two most liquid windows (UTC)
TRADE_SESSIONS = [
    (7, 12),   # London open
    (13, 17),  # New York open
]

# ─── Loop timing ─────────────────────────────────────────────────────────────
POLL_INTERVAL_SECONDS = 30   # check every 30 s
