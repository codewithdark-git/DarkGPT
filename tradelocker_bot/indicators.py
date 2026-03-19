"""
Pure-Python technical indicators (no external libs needed).
All functions accept a list of floats and return a float or list.
"""

from typing import Optional


# ─── EMA ──────────────────────────────────────────────────────────────────────

def ema(values: list[float], period: int) -> list[float]:
    """Exponential Moving Average — same as most platforms."""
    if len(values) < period:
        return []
    k   = 2.0 / (period + 1)
    out = [sum(values[:period]) / period]      # seed with SMA
    for v in values[period:]:
        out.append(v * k + out[-1] * (1 - k))
    return out


def last_ema(values: list[float], period: int) -> Optional[float]:
    e = ema(values, period)
    return e[-1] if e else None


# ─── RSI ──────────────────────────────────────────────────────────────────────

def rsi(values: list[float], period: int = 14) -> Optional[float]:
    """Wilder RSI — returns the latest value or None if not enough data."""
    if len(values) < period + 1:
        return None
    gains, losses = [], []
    for i in range(1, len(values)):
        d = values[i] - values[i - 1]
        gains.append(max(d, 0))
        losses.append(max(-d, 0))
    # Wilder smoothing
    avg_g = sum(gains[:period]) / period
    avg_l = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_g = (avg_g * (period - 1) + gains[i]) / period
        avg_l = (avg_l * (period - 1) + losses[i]) / period
    if avg_l == 0:
        return 100.0
    rs = avg_g / avg_l
    return round(100 - 100 / (1 + rs), 2)


# ─── ATR ──────────────────────────────────────────────────────────────────────

def atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> Optional[float]:
    """Average True Range (Wilder smoothing)."""
    if len(highs) < period + 1:
        return None
    trs = []
    for i in range(1, len(highs)):
        tr = max(
            highs[i]  - lows[i],
            abs(highs[i]  - closes[i - 1]),
            abs(lows[i]   - closes[i - 1]),
        )
        trs.append(tr)
    avg = sum(trs[:period]) / period
    for t in trs[period:]:
        avg = (avg * (period - 1) + t) / period
    return avg


# ─── Signal generation ────────────────────────────────────────────────────────

def compute_signal(candles: list[dict], cfg) -> dict:
    """
    Returns:
        {
          'signal': 'long' | 'short' | 'none',
          'sl':     float,
          'tp':     float,
          'atr':    float,
        }
    """
    if len(candles) < max(cfg.EMA_SLOW, cfg.RSI_PERIOD + 1, cfg.ATR_PERIOD + 1) + 5:
        return {"signal": "none"}

    closes = [c["close"] for c in candles]
    highs  = [c["high"]  for c in candles]
    lows   = [c["low"]   for c in candles]

    ema_f = ema(closes, cfg.EMA_FAST)
    ema_s = ema(closes, cfg.EMA_SLOW)

    if len(ema_f) < 2 or len(ema_s) < 2:
        return {"signal": "none"}

    cur_f,  cur_s  = ema_f[-1], ema_s[-1]
    prev_f, prev_s = ema_f[-2], ema_s[-2]

    cur_rsi = rsi(closes, cfg.RSI_PERIOD)
    if cur_rsi is None:
        return {"signal": "none"}

    cur_atr = atr(highs, lows, closes, cfg.ATR_PERIOD)
    if cur_atr is None:
        return {"signal": "none"}

    price = closes[-1]
    sl_dist = cur_atr * cfg.ATR_SL_MULT
    tp_dist = cur_atr * cfg.ATR_TP_MULT

    # Bullish crossover: fast crosses above slow + RSI confirms momentum
    if prev_f <= prev_s and cur_f > cur_s and cur_rsi > cfg.RSI_LONG:
        return {
            "signal": "long",
            "sl":     round(price - sl_dist, 5),
            "tp":     round(price + tp_dist, 5),
            "atr":    cur_atr,
        }

    # Bearish crossover: fast crosses below slow + RSI confirms
    if prev_f >= prev_s and cur_f < cur_s and cur_rsi < cfg.RSI_SHORT:
        return {
            "signal": "short",
            "sl":     round(price + sl_dist, 5),
            "tp":     round(price - tp_dist, 5),
            "atr":    cur_atr,
        }

    return {"signal": "none"}
