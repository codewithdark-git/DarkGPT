"""
TradeLocker REST API wrapper
Handles auth, candle fetching, order placement, position management.
"""

import time
import logging
import requests
from typing import Optional

import config

log = logging.getLogger(__name__)


class TradeLockerAPI:
    """Thin wrapper around TradeLocker REST v1."""

    # Refresh access token 5 min before it expires
    TOKEN_REFRESH_BUFFER = 300

    def __init__(self):
        self.base      = config.TRADELOCKER_BASE_URL.rstrip("/")
        self.access_token  = None
        self.refresh_token = None
        self.token_expiry  = 0
        self.account_id    = config.ACCOUNT_ID
        self.acc_num       = None   # numeric account number used for trading routes

    # ── Auth ──────────────────────────────────────────────────────────────────

    def login(self):
        """Authenticate and store tokens."""
        url  = f"{self.base}/trade/auth/jwt/token"
        body = {
            "email":    config.API_EMAIL,
            "password": config.API_PASSWORD,
            "server":   config.API_SERVER,
        }
        r = requests.post(url, json=body, timeout=10)
        r.raise_for_status()
        data = r.json()
        self.access_token  = data["accessToken"]
        self.refresh_token = data["refreshToken"]
        self.token_expiry  = time.time() + data.get("accessTokenExpiresIn", 3600)
        log.info("Login successful.")
        self._fetch_account()

    def _refresh(self):
        url  = f"{self.base}/trade/auth/jwt/refresh"
        body = {"refreshToken": self.refresh_token}
        r = requests.post(url, json=body, timeout=10)
        r.raise_for_status()
        data = r.json()
        self.access_token = data["accessToken"]
        self.token_expiry = time.time() + data.get("accessTokenExpiresIn", 3600)
        log.debug("Token refreshed.")

    def _ensure_token(self):
        if time.time() >= self.token_expiry - self.TOKEN_REFRESH_BUFFER:
            self._refresh()

    def _headers(self) -> dict:
        self._ensure_token()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type":  "application/json",
        }

    # ── Account ───────────────────────────────────────────────────────────────

    def _fetch_account(self):
        url = f"{self.base}/trade/accounts"
        r   = requests.get(url, headers=self._headers(), timeout=10)
        r.raise_for_status()
        accounts = r.json().get("accounts", [])
        if not accounts:
            raise RuntimeError("No accounts found.")
        acc = accounts[0]
        self.account_id = acc.get("id") or acc.get("accNum")
        self.acc_num    = acc.get("accNum") or self.account_id
        log.info("Account: id=%s  accNum=%s", self.account_id, self.acc_num)

    def get_balance(self) -> dict:
        """Returns dict with 'balance', 'equity', 'usedMargin'."""
        url = f"{self.base}/trade/accounts/{self.acc_num}"
        r   = requests.get(url, headers=self._headers(), timeout=10)
        r.raise_for_status()
        return r.json()

    # ── Market data ───────────────────────────────────────────────────────────

    def get_instrument_id(self, symbol: str) -> Optional[str]:
        """Resolve a symbol like 'EURUSD' to its TradeLocker instrument id."""
        url    = f"{self.base}/trade/instruments"
        params = {"locale": "en", "routeId": self.acc_num}
        r      = requests.get(url, headers=self._headers(), params=params, timeout=10)
        r.raise_for_status()
        for inst in r.json().get("d", {}).get("instruments", []):
            if inst.get("name", "").upper() == symbol.upper():
                return str(inst["tradableInstrumentId"])
        log.warning("Instrument not found: %s", symbol)
        return None

    def get_candles(self, instrument_id: str, timeframe: str, count: int) -> list[dict]:
        """
        Fetch the last `count` OHLCV bars.
        Returns list of dicts: {time, open, high, low, close, volume}
        """
        url    = f"{self.base}/trade/history"
        params = {
            "tradableInstrumentId": instrument_id,
            "routeId":              self.acc_num,
            "resolution":          timeframe,
            "limit":               count,
        }
        r = requests.get(url, headers=self._headers(), params=params, timeout=15)
        r.raise_for_status()
        raw = r.json().get("d", {}).get("bars", [])
        candles = [
            {
                "time":   bar[0],
                "open":   float(bar[1]),
                "high":   float(bar[2]),
                "low":    float(bar[3]),
                "close":  float(bar[4]),
                "volume": float(bar[5]) if len(bar) > 5 else 0,
            }
            for bar in raw
        ]
        return candles

    def get_price(self, instrument_id: str) -> dict:
        """Get current bid/ask."""
        url    = f"{self.base}/trade/quotes"
        params = {"tradableInstrumentId": instrument_id, "routeId": self.acc_num}
        r      = requests.get(url, headers=self._headers(), params=params, timeout=10)
        r.raise_for_status()
        q = r.json().get("d", {})
        return {"bid": float(q.get("bp", 0)), "ask": float(q.get("ap", 0))}

    # ── Orders / Positions ────────────────────────────────────────────────────

    def place_market_order(
        self,
        instrument_id: str,
        side: str,          # "buy" or "sell"
        qty: float,
        sl: float,
        tp: float,
    ) -> dict:
        url  = f"{self.base}/trade/orders"
        body = {
            "tradableInstrumentId": instrument_id,
            "routeId":              self.acc_num,
            "type":                "market",
            "side":                side,
            "qty":                 qty,
            "stopLoss":            round(sl, 5),
            "takeProfit":          round(tp, 5),
        }
        r = requests.post(url, json=body, headers=self._headers(), timeout=10)
        r.raise_for_status()
        log.info("Order placed: %s %s qty=%.4f  SL=%.5f  TP=%.5f", side, instrument_id, qty, sl, tp)
        return r.json()

    def get_open_positions(self) -> list[dict]:
        url = f"{self.base}/trade/positions"
        params = {"routeId": self.acc_num}
        r   = requests.get(url, headers=self._headers(), params=params, timeout=10)
        r.raise_for_status()
        return r.json().get("d", {}).get("positions", [])

    def close_position(self, position_id: str, qty: float):
        url  = f"{self.base}/trade/positions/{position_id}"
        body = {"routeId": self.acc_num, "qty": qty}
        r    = requests.delete(url, json=body, headers=self._headers(), timeout=10)
        r.raise_for_status()
        log.info("Closed position %s", position_id)
