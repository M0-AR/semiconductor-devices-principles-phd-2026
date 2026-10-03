# REPRODUCIBILITY

- Python 3.12-slim Docker image, `requirements.txt` pinned floors, `PYTHONPATH=/work/src`.
- Seeds: none needed (deterministic analytics; no RNG in suite).
- Live data: `src/sdp/live_verify.py` prefers yfinance live, falls back to
  snapshot `2026-10-03T10:26Z` (NVDA 233.95, TSM 472.78). Suite never fails on
  network; `live_market.json` records which leg was used.
- Figures: matplotlib Agg backend, dpi=150, deterministic sweeps.
- Verified host: Python 3.12.13, numpy 2.4.6, matplotlib 3.11.1, scipy 1.17.1,
  pandas 3.0.3, pytest 8.3.4, yfinance 1.7.0, Docker 29.1.3 / Compose 2.40.3.
- Run order matters (cheap → expensive): pytest → run_all → benchmark_suite.
- Failure policy: any FAIL in summary.json exits non-zero; Docker propagates it.
