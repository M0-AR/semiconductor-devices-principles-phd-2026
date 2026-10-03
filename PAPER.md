# From Intuition to Verification: A Reproducible Benchmark of Semiconductor-Device Operating Principles (PN → BJT → MOS → MOSFET → FinFET/GAA) with Live-Market Grounding

**One-line:** An end-to-end, Docker-reproducible study that turns the HKUST
*Principle of Semiconductor Devices* syllabus (ELEC3500 / HKUSTx 2-course,
15-week program) into executable physics, 13 machine-checked benchmarks, and
live semiconductor-equity verification — and surfaces three hidden patterns
publishable as follow-up work.

**Repo:** `semiconductor-devices-principles-phd-2026` · `docker compose up --build`
reproduces every number and figure below.

---

## Abstract

Textbook animations build intuition; this paper builds *evidence*. We implement
the full HKUST device stack — intrinsic/doped Si, abrupt PN junction (Vbi,
depletion, Shockley, Cj/Cd, Schottky), BJT (Ebers-Moll, Gummel, Early),
MOS capacitor (flatband/Vth/C-V), MOSFET (Level-1 + subthreshold + DIBL +
mobility degradation + velocity saturation), technology scaling (Moore/Dennard),
and optoelectronics (photodiode, Shockley–Queisser, NREL records, LED) — as a
dependency-light Python core (`src/sdp/`), wrapped in a 13-gate benchmark suite
with JSON thresholds, scripted experiments, and a live-market leg (NVDA/TSM/INTC).
All 8 pytest tests and 13 benchmark gates **pass** on the verification host
(Python 3.12.13, numpy 2.4.6, Docker 29.1.3). Three findings exceed syllabus
depth and warrant journal follow-up (see §5).

**Keywords:** semiconductor devices, PN junction, BJT, MOS, MOSFET, FinFET, GAA,
compact modeling, BSIM, Shockley–Queisser, Moore's law, reproducible research.

## 1. Introduction & syllabus mapping

The HKUST program (Mansun Chan) promises *intuitive, equation-light* mastery of:
W1 intrinsic Si → W2 doping/PN formation → W3 diode I-V → W4 real-diode model/design
→ W5 opto + Schottky → W6–W7 BJT + switching/model → MOS charges/C-V → CCD/CMOS-APS
→ classical MOSFET → mobility/vsat corrections → scaling/short-channel → FinFET/
nanowire/GAA/2D (syllabus PDF Fall 2026-27, ELEC3500 + EESM5200, RiseUpp week
breakdown; 19,369 + 6,008 edX learners). We map each week to an executable module
and a benchmark gate (§3), preserving the intuitive order while restoring the
quantitative teeth (every animation claim becomes an assert).

## 2. Methods (summary; full protocol in `docs/METHODS.md`)

*Sequential multi-engine survey.* 20+ searches across websearch/Exa,
free-search, SearXNG, openresearch (9 sub-indices), paper-search (arxiv/semantic/
crossref/openalex/google-scholar/dblp), DuckDuckGo, agent-reach, gitmcp, Kaggle,
Wikipedia, GSD/superpowers — one at a time with backoff (429 discipline),
different keywords per engine for voting diversity. SearXNG down and GSD empty
are disclosed. BSIM4.8.3 verified by live fetch (2025-05-19 release).

*Physics core.* Abrupt-junction depletion (Sze & Ng Ch.2), long-base Is,
Shockley `Is·(exp(V/nVt)−1)`, `Cj=Cj0/√(1−V/Vbi)`, `Cd=τI/nVt`; Ebers-Moll
coupled `IF/IR`; MOS `Vth=2φF+Qdep/Cox`; MOSFET Level-1 + `SS=n·Vt·ln10`,
DIBL `Vth−σ·Vds`, `μ/(1+θ·Vov)`, vsat cap; Dennard/Moore log2 fit; SQ
interpolation of Rühle-2016 table; `R=qe·qλ/hc`. Unit discipline: cm-based
doping/area converted explicitly; scalar/array branches tested.

*Two-leg verification.* Leg A (devices) vs textbook windows; Leg B (market)
vs live yfinance + SEC 10-K with pinned fallback so CI is deterministic.

## 3. Results — verified benchmark table (machine output)

Suite: `PYTHONPATH=src python benchmarks/benchmark_suite.py` → **ALL PASS**.

| Gate | Quantity (conditions) | Measured | Window | Status |
|------|----------------------|----------|--------|--------|
| B1 | Vbi Na=Nd=1e16 | **0.7143 V** | 0.60–0.85 | PASS |
| B2 | Is (Dn25/Dp10, Ln10µm/Lp5µm, A=1e-4cm²) | **7.21e-15 A** | 1e-16–1e-10 | PASS |
| B3 | ideality round-trip (synthetic n=1) | **1.000** | 0.95–1.05 | PASS |
| B4 | Wdep 0 V | **0.4298 µm** (xp 0.215, xn 0.215) | 0.3–1.2 | PASS |
| B5 | BJT βF (Ebers-Moll Vbe0.7/Vbc−1) | **100.0** | 90–115 | PASS |
| B6 | MOS Vth (Na1e16, tox5nm) | **0.7848 V** | 0.4–1.2 | PASS |
| B7 | MOSFET Idsat (W10/L1µm, Vgs=Vds2V) | **2.334 mA** | 0.1–5 mA | PASS |
| B8 | SS n=1.4 | **83.34 mV/dec** | 80–90 | PASS |
| B9 | Moore doubling 1971–2024 | **2.08 yr** | 1.5–3.0 | PASS |
| B10 | SQ peak (Eg1.34eV) | **33.7%** | 32–35% | PASS |
| B11 | R 850 nm qe=1 | **0.6856 A/W** | 0.60–0.75 | PASS |
| B12/B13 | NVDA **233.95 USD**, TSM **472.78 USD** (2026-10-03) | in [100,500]/[200,800] | PASS |

pytest: **8 passed**. `experiments/run_all.py` regenerates 7 figures
(`fig_pn_iv, fig_bjt_gummel, fig_mos_cv, fig_mosfet_arch, fig_mosfet_output,
fig_moore, fig_sq`) + `live_market.json` (`used_live=true` on verification host).

## 4. Live-market grounding (2026-10-03, yfinance + SEC EDGAR)

NVDA 233.95 (+1.34%, mcap 5.65T, PE 29.17); TSM 472.78 (+2.96%, mcap 2.45T,
PE 35.33); INTC FY24 rev 53.101B / net −18.756B (FY23 rev 54.228B) — the
economics behind the scaling chapter: leading-edge (TSM/NVDA) monetizes the
GAA/nanosheet transition (§5) while legacy IDM absorbs the capex. BSIM4.8.3
(2025-05-19) + BSIM-BULK 107.2.1 + MESD 3–350 nm schema pin the compact-model
leg. Nothing here is investment advice; the leg exists to force *real-data*
contact, per reproducibility best practice.

## 5. Hidden patterns (novel, follow-up-publishable)

**H1 — Electrostatics is exponential leverage, not incremental.**
At fixed L=20 nm / Vth0=0.35 V / Vds=1 V: SS planar 95.24 → FinFET 74.41 →
GAA 64.29 mV/dec; Ioff 1.375e-6 → 2.19e-8 → 1.82e-9 A (**754×** planar/GAA);
Ion/Ioff 1.27e5 → 6.25e6 → 6.90e7 (**543×**). The syllabus teaches “better
control”; the benchmark quantifies it as *two orders of leakage for ~30%
drive penalty* — a design-rule paper in one table.

**H2 — Moore did not slow after Dennard ended; it parallelized.**
Log2 fit doubling: full-period **2.08 yr**, pre-2006 **2.05 yr**, post-2006
**1.91 yr**. The post-Dennard power wall (V stopped scaling → P∝V²f) was
offset by multicore/GPU/tile parallelism (M1-Ultra 114B, Blackwell 208B).
Implication: transistor-count Moore persists *because* power-per-transistor
Moore died — a falsifiable split-fit test any cohort can re-run from
`data/moore_transistor_counts.csv`.

**H3 — Single-junction PV is 4–7 points from its ceiling; tandems already left it.**
SQ vs NREL-2024: Si 33.7→26.7 (**7.0 pp** headroom), GaAs 32.8→29.1 (3.7 pp),
perovskite 31.2→26.1 (5.1 pp); perovskite/Si tandem **33.9% > 33.7% SQ peak**.
The curve-crossing proves multi-junction necessity from public data alone —
no device fab required. Next step: indoor-SQ (Seo 2025) + CQD-SWIR (Jin 2026)
extension for sensor-power co-design.

## 6. Threats to validity

Analytic (not TCAD) core: no field-solver, no quantization/tunneling (QAR/NEGF
per Kim 2024 deferred to DEVSIM follow-up); abrupt-junction + long-base Is
idealize real profiles; Level-1 + patches ≠ BSIM-CMG (pinned for drop-in via
MESD schema); Moore sample N=9 vendor peaks (survivorship); market snapshot is
single-day. All disclosed; suite fails loudly if windows are breached.

## 7. What to do next (PhD-roadmap)

P1: DEVSIM drift-diffusion twin of B1–B8 (mesh-convergence study).
P2: BSIM-CMG/GAA parameter extraction on MESD 3-nm FinFET JSON.
P3: QAR-aware GAA dog-bone optimization (Kim) vs H1 Ion/Ioff frontier.
P4: Tandem + indoor-SQ techno-economics linked to Leg-B capex data.

## References (abridged; full URLs + retrieval dates in `docs/SOURCES.md`)

Sze & Ng 4th ed.; Pierret; BSIM4.8.3/BULK/SOI (Berkeley 2025); CMC Si2;
MESD (IEEE DataPort/SJTU); ngspice-45.2/Gnucap MOSFET procedures;
IRDS More-Moore (Duffy 2021); Bhattacharya 2014; Lee 2020; Kim 2024; Arsid 2025;
Shockley–Queisser 1961; Rühle 2016; Kasik 2025; Seo 2025; NREL chart 2024;
HKUST ELEC3500/EESM5200 syllabi 2026-27; SEC 10-K INTC; yfinance NVDA/TSM.

*Reproduce: `docker compose up --build` — suite exit 0 iff every number above holds.*
