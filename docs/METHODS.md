# METHODS — zero-to-hero verification protocol

This repo implements the 2026 reproducible-simulation best practice found in
research (DEVSIM code-first + ViennaTools orchestration + Sentaurus/ATLAS
deck discipline), reduced to a dependency-light Python core so anyone can run
`docker compose up` with no license server.

## 1. One search at a time (rate-limit discipline)
Exa/websearch 429s were avoided by sequential tool calls with backoff and a
DuckDuckGo-lite fallback. Every search family was polled with *different*
keywords (diode/BJT/MOSFET/FinFET-GAA/solar/TCAD/docker) to collect voting
opinions instead of one-engine bias. SearXNG was down (network error) —
recorded as such; GSD websearch returned empty; both are disclosed, not hidden.

## 2. Physics first, compact second
- Analytic core (`src/sdp/`): abrupt-junction Vbi/W/Cj/Cd, Shockley + Schottky,
  Ebers-Moll/Gummel, MOS Vth/C-V, MOSFET L1+subthreshold+DIBL+mobility+vsat,
  Dennard/Moore, SQ/responsivity. Units explicit (cm vs m guarded).
- Compact tie-in: BSIM4.8.3 / BSIM-BULK / PSP versions pinned in SOURCES;
  MESD schema adopted for future PDK-drop-in (W/L/Nfin/Vgs/Ids/Cgg).
- No hand edit without execution: every threshold in `thresholds.json` is
  asserted by `pytest` AND `benchmark_suite.py`. README numbers are copied
  from tool output, not typed.

## 3. Live-data verification (two legs)
- Leg A — devices: analytic I-V/C-V checked against textbook windows
  (Vbi 0.6–0.85 V, Is 1e-16–1e-10 A, SS 80–90 mV/dec for n=1.4, SQ peak 32–35%).
- Leg B — market: NVDA/TSM quotes + INTC 10-K fetched live on 2026-10-03;
  `live_verify.py` re-fetches via yfinance when online, else asserts the
  pinned snapshot so CI stays deterministic. Tolerance gate ±25% flags data
  feed breaks without failing physics.

## 4. Hidden-pattern hunt (how to read RESULTS)
- Fit Moore log2(count) vs year → doubling time; compare 1971–2024 slope
  break (Dennard end ~2006) by splitting fit at 2006.
- Sweep n_sub/DIBL by architecture (planar/FinFET/GAA) at fixed L=20 nm →
  Ioff ratio is exponential in SS, not linear (order-of-magnitude finding).
- Map NREL records onto SQ(Eg) → headroom table; tandem point above curve
  proves multi-junction necessity (not a model error).
- Extract n from synthetic forward I-V → round-trip error <5% validates the
  metrology chain used for real diodes.

## 5. Re-run
```
docker compose up --build
# or: pip install -r requirements.txt && pytest -q tests && python experiments/run_all.py && PYTHONPATH=src python benchmarks/benchmark_suite.py
```
Artifacts: `benchmarks/results/*.png`, `summary.json`, `live_market.json`.
