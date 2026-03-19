"""
Risk manager for Atlas funded accounts.
Enforces:
  - Per-trade risk % of balance
  - Daily loss limit
  - Total drawdown ceiling
  - Max concurrent open trades
"""

import logging
from datetime import date

import config

log = logging.getLogger(__name__)


class RiskManager:
    def __init__(self):
        self.starting_balance: float = 0.0
        self.daily_start_balance: float = 0.0
        self.daily_date: date = date.today()
        self.initialised = False

    # ── Initialise ────────────────────────────────────────────────────────────

    def initialise(self, balance: float):
        self.starting_balance    = balance
        self.daily_start_balance = balance
        self.daily_date          = date.today()
        self.initialised         = True
        log.info("RiskManager initialised. Starting balance: %.2f", balance)

    def _refresh_day(self, balance: float):
        today = date.today()
        if today != self.daily_date:
            self.daily_start_balance = balance
            self.daily_date          = today
            log.info("New trading day. Daily balance reset to %.2f", balance)

    # ── Guard checks ──────────────────────────────────────────────────────────

    def can_trade(self, balance: float, open_trade_count: int) -> tuple[bool, str]:
        """Returns (True, '') if trading is allowed, else (False, reason)."""
        if not self.initialised:
            return False, "Risk manager not initialised."

        self._refresh_day(balance)

        # 1. Too many open positions
        if open_trade_count >= config.MAX_OPEN_TRADES:
            return False, f"Max open trades reached ({config.MAX_OPEN_TRADES})."

        # 2. Daily loss limit
        daily_loss_pct = (self.daily_start_balance - balance) / self.daily_start_balance * 100
        if daily_loss_pct >= config.MAX_DAILY_LOSS_PCT:
            return False, f"Daily loss limit hit ({daily_loss_pct:.2f}% >= {config.MAX_DAILY_LOSS_PCT}%)."

        # 3. Total drawdown
        total_dd_pct = (self.starting_balance - balance) / self.starting_balance * 100
        if total_dd_pct >= config.MAX_TOTAL_DRAWDOWN_PCT:
            return False, f"Total drawdown limit hit ({total_dd_pct:.2f}% >= {config.MAX_TOTAL_DRAWDOWN_PCT}%)."

        return True, ""

    # ── Position sizing ───────────────────────────────────────────────────────

    def calculate_lot_size(
        self,
        balance: float,
        sl_distance_price: float,
        pip_value: float = 10.0,    # approximate USD pip value for 1 lot on most majors
        min_lot: float = 0.01,
        max_lot: float = 1.0,
    ) -> float:
        """
        Risk $ = balance * RISK_PCT / 100
        Lot    = Risk$ / (sl_distance_pips * pip_value_per_lot)
        """
        risk_usd   = balance * config.RISK_PER_TRADE_PCT / 100
        sl_pips    = sl_distance_price / 0.0001   # 1 pip = 0.0001 for most pairs
        if sl_pips <= 0:
            return min_lot
        lot = risk_usd / (sl_pips * pip_value)
        lot = max(min_lot, min(max_lot, round(lot, 2)))
        log.debug(
            "Sizing: balance=%.2f  risk=%.2f$  sl_pips=%.1f  lot=%.2f",
            balance, risk_usd, sl_pips, lot,
        )
        return lot
