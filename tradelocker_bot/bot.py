"""
DarkGPT TradeLocker Bot — Main loop
Atlas Funded Account  |  EMA crossover + RSI + ATR

Run:
    python bot.py
"""

import time
import logging
import sys

import config
from tradelocker_api import TradeLockerAPI
from indicators      import compute_signal
from risk_manager    import RiskManager
from session_filter  import in_trading_session

# ─── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("bot.log"),
    ],
)
log = logging.getLogger(__name__)


# ─── State ────────────────────────────────────────────────────────────────────
# Track which symbols we already have an open position in (avoid re-entry)
open_symbol_ids: set[str] = set()


def run():
    api  = TradeLockerAPI()
    risk = RiskManager()

    log.info("=== DarkGPT TradeLocker Bot starting ===")
    api.login()

    # Pre-resolve instrument ids once
    instrument_map: dict[str, str] = {}
    for sym in config.SYMBOLS:
        iid = api.get_instrument_id(sym)
        if iid:
            instrument_map[sym] = iid
            log.info("Resolved %s → id=%s", sym, iid)
        else:
            log.warning("Could not resolve %s — skipping.", sym)

    if not instrument_map:
        log.error("No valid instruments. Check your symbol list and account server.")
        return

    # Initialise risk manager with current balance
    bal_data = api.get_balance()
    balance  = float(bal_data.get("balance", bal_data.get("equity", 10000)))
    risk.initialise(balance)

    log.info("Starting main loop. Polling every %ds …", config.POLL_INTERVAL_SECONDS)

    while True:
        try:
            _cycle(api, risk, instrument_map)
        except KeyboardInterrupt:
            log.info("Bot stopped by user.")
            break
        except Exception as exc:
            log.error("Cycle error: %s", exc, exc_info=True)

        time.sleep(config.POLL_INTERVAL_SECONDS)


def _cycle(api: TradeLockerAPI, risk: RiskManager, instrument_map: dict[str, str]):
    """One polling cycle: fetch data → evaluate → act."""

    # ── Get current state ────────────────────────────────────────────────────
    bal_data       = api.get_balance()
    balance        = float(bal_data.get("balance", bal_data.get("equity", 0)))
    open_positions = api.get_open_positions()
    open_count     = len(open_positions)

    # Update the set of instruments that already have a position
    open_inst_ids = {str(p.get("tradableInstrumentId", "")) for p in open_positions}

    # ── Session guard ────────────────────────────────────────────────────────
    if not in_trading_session():
        log.debug("Outside trading session — skipping.")
        return

    # ── Risk guard ───────────────────────────────────────────────────────────
    allowed, reason = risk.can_trade(balance, open_count)
    if not allowed:
        log.warning("Trading paused: %s", reason)
        return

    # ── Evaluate each symbol ─────────────────────────────────────────────────
    for sym, iid in instrument_map.items():
        if iid in open_inst_ids:
            log.debug("%s: already in a position — skip.", sym)
            continue

        candles = api.get_candles(iid, config.TIMEFRAME, config.CANDLES_NEEDED)
        if not candles:
            log.warning("%s: no candle data.", sym)
            continue

        sig = compute_signal(candles, config)

        if sig["signal"] == "none":
            log.debug("%s: no signal.", sym)
            continue

        # ── Size position ────────────────────────────────────────────────────
        price      = candles[-1]["close"]
        sl_dist    = abs(price - sig["sl"])
        lot        = risk.calculate_lot_size(balance, sl_dist)

        side = "buy" if sig["signal"] == "long" else "sell"

        log.info(
            "SIGNAL  %s  %s  @%.5f  SL=%.5f  TP=%.5f  lot=%.2f",
            sym, side.upper(), price, sig["sl"], sig["tp"], lot,
        )

        # ── Place order ──────────────────────────────────────────────────────
        try:
            api.place_market_order(
                instrument_id=iid,
                side=side,
                qty=lot,
                sl=sig["sl"],
                tp=sig["tp"],
            )
            open_inst_ids.add(iid)   # prevent double-entry this cycle
        except Exception as exc:
            log.error("Order failed for %s: %s", sym, exc)


if __name__ == "__main__":
    run()
