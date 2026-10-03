"""Live-market verification: fetch real semiconductor equity data, fall back to
verified snapshots when offline (so benchmarks stay reproducible).

Verified snapshots (retrieved 2026-10-03 via agent-reach_stock_quote / SEC EDGAR):
  NVDA 233.95 USD (+1.34%), TSM 472.78 USD (+2.96%), INTC FY2024 rev 53.1B, net -18.8B.
Live path uses yfinance (no key) when network allows.
"""
import json, datetime

SNAPSHOT = {
    "retrieved_utc": "2026-10-03T10:26Z",
    "NVDA": {"current": 233.95, "pct": 1.33847, "mcap": 5649190617088, "pe_ttm": 29.17082, "source": "yfinance via agent-reach_stock_quote"},
    "TSM": {"current": 472.78, "pct": 2.95731, "mcap": 2452061159424, "pe_ttm": 35.334827, "source": "yfinance via agent-reach_stock_quote"},
    "INTC_SEC": {"rev_2024": 53101000000, "net_2024": -18756000000, "rev_2023": 54228000000, "assets_2024": 196485000000, "source": "SEC EDGAR 10-K via openresearch_get_company_financials"},
    "BSIM4": {"version": "4.8.3", "released": "2025-05-19", "source": "https://bsim.berkeley.edu/models/bsim4/ fetched 2026-10-03"},
}

def fetch_live(symbols=("NVDA", "TSM", "INTC", "AMD", "ASML")):
    """Try yfinance live; return (live_dict, used_live_bool). Never raises."""
    try:
        import yfinance as yf
        out = {}
        for s in symbols:
            t = yf.Ticker(s)
            fi = t.fast_info if hasattr(t, "fast_info") else {}
            price = None
            try:
                price = float(fi["last_price"]) if "last_price" in fi else None
            except Exception:
                price = None
            if price is None:
                try:
                    h = t.history(period="1d")
                    price = float(h["Close"].iloc[-1]) if len(h) else None
                except Exception:
                    price = None
            out[s] = {"current": price, "live": price is not None}
        if any(v["current"] for v in out.values()):
            return out, True
    except Exception as e:
        return {"error": str(e), "fallback": SNAPSHOT}, False
    return {"fallback": SNAPSHOT}, False

def verify_snapshot_tolerance(live, tol=0.25):
    """Check live prices within tol fraction of snapshot (sanity, not trading signal)."""
    res = {}
    for k in ("NVDA", "TSM"):
        if k in live and live[k].get("current"):
            snap = SNAPSHOT[k]["current"]
            res[k] = abs(live[k]["current"]-snap)/snap < tol
    return res

if __name__ == "__main__":
    live, ok = fetch_live()
    print(json.dumps({"used_live": ok, "live": live,
                      "snapshot": SNAPSHOT,
                      "utc": datetime.datetime.utcnow().isoformat()+"Z"}, indent=2))
