# DarkGPT TradeLocker Bot

Automated trading bot for **TradeLocker** (Atlas Funded Accounts).

## Strategy

| Component | Detail |
|-----------|--------|
| Signal | EMA(9) crosses EMA(21) |
| Confirmation | RSI(14) momentum filter |
| Stop-Loss | 1.5 × ATR(14) |
| Take-Profit | 2.5 × ATR(14) — R:R ≈ 1.67 |
| Timeframe | 15-minute bars |
| Sessions | London (07-12 UTC) + New York (13-17 UTC) |

## Atlas Risk Rules Built-In

- Max **0.5% risk per trade** (configurable)
- Max **2% daily loss** — bot stops for the day if hit
- Max **4% total drawdown** — bot stops if hit
- Max **2 concurrent positions**

## Setup

```bash
pip install -r requirements.txt
```

Edit `config.py`:

```python
TRADELOCKER_BASE_URL = "https://live.tradelocker.com"   # live account
API_EMAIL    = "you@email.com"
API_PASSWORD = "yourpassword"
API_SERVER   = "YOUR-BROKER-SERVER"
```

## Run

```bash
python bot.py
```

Logs are written to `bot.log` and stdout.

## Files

```
bot.py              — main loop
config.py           — all settings in one place
tradelocker_api.py  — TradeLocker REST wrapper (auth, orders, candles)
indicators.py       — EMA, RSI, ATR, signal logic
risk_manager.py     — position sizing, daily/total drawdown guards
session_filter.py   — London/NY session gate
```

## Tips for Atlas

- Keep `RISK_PER_TRADE_PCT` at **0.5 %** or lower
- Never widen the `MAX_DAILY_LOSS_PCT` beyond your Atlas daily limit
- Use the **demo** URL first to paper-trade and verify signals
- Monitor `bot.log` daily
