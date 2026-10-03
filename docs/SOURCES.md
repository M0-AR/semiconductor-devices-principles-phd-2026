# SOURCES — every external claim, retrievable

Retrieved 2026-10-03 (UTC). Snippets are not sources; facts below were read
from the page/body itself via fetch or tool output.

## Curriculum (HKUST / edX)
1. HKUST ELEC3500 Fall 2026-27 syllabus PDF — Mansun Chan, 14 topics
   (semiconductor properties → scaling trends). `seng.hkust.edu.hk/.../ELEC3500_Fall 2026-27.pdf`
2. HKUST Research Portal — 2026-27 Fall ELEC3500 + EESM5200 (BSIM/SPICE).
   `researchportal.hkust.edu.hk/en/courses/2026-27-fall-elec3500...`
3. edX HKUSTx program pasted in task: 2 courses, 15 weeks, 19,369 + 6,008 learners.
4. RiseUpp/MOOC-List mirrors of FET course weeks 1-7 (MOS → GAA/2D).

## Device physics texts (equations implemented)
5. Sze & Ng, Physics of Semiconductor Devices 4th ed. — Vbi, Wdep, Shockley,
   Ebers-Moll, MOS Vth, Level-1 MOSFET, SS=n·Vt·ln10.
6. Pierret, Semiconductor Device Fundamentals — doping, drift-diffusion.
7. Wikipedia Shockley diode equation + MOSFET + FinFET (ideality 1–2, triode/sat).
8. Physics.SE diode ideality thread; UliEngineering Shockley examples.
9. mattwachter/extract-diode-parameters (C-V + I-V extraction pattern).

## Compact models & simulation (2026 best practice)
10. BSIM4.8.3 standard 2025-05-19 — `bsim.berkeley.edu/models/bsim4/` (fetched live).
    BSIM-BULK 107.2.1 (2025-02-11), BSIM-SOI 100.1.1, CMC Si2 standard models.
11. DEVSIM (Apache 2.0, devsim/devsim) + devsim_bjt_example/3dmos — code-first TCAD.
12. MESD dataset (IEEE DataPort, SJTU): 11 PDKs, 44 devices, 3–350 nm, Ids/Cgg JSON.
13. deutzlukas-hub/mosfet-test-procedures: ngspice 45.2 vs Gnucap BSIM4/PSP104 DC/AC/transient/noise.
14. OpenTCAD (2026-05-22), ViennaTools, Sentaurus, Silvaco ATLAS, COMSOL module (gitnux 2026-07-09 brief).
15. COMSOL p-n SPICE-extraction gallery; Sedra/Smith App B SPICE models.

## Advanced transistors & scaling
16. OpenAlex: FinFET→GAA reviews (Bhattacharya 2014; Lee et al. 2020 nanosheet Lg=22nm;
    Kim et al. 2024 QAR NEGF dog-bone optimization; Duffy IRDS More-Moore to 2025).
17. Crossref: Arsid 2025 FinFET→GAA evolution; Saini 2024 12-nm GAA high-k.
18. IRDS More-Moore forecast (via Duffy 2021): FinFET to ~2025, then lateral→vertical GAA.
19. Moore counts used here are vendor-announced (Intel/Apple/NVIDIA) via Wikipedia scale list.

## Optoelectronics
20. Shockley–Queisser 1961; Rühle 2016 table; Google Scholar 2025–2026 revisits
    (Seo et al. indoor SQ; Kasik et al. top-cells vs SQ mid-2024; Arucu 2026 perovskite SQ).
21. NREL Best Research-Cell chart: Si 26.7% (Kaneka), GaAs 29.1% (Alta), perovskite 26.1%,
    tandem 33.9% (LONGi 2024) — tandem exceeds single-junction SQ by construction.
22. EuropePMC 2026: PbS-CQD SWIR photodiode, dark-current review, CMOS multispectral+GAA.

## Live market (verification, not investment advice)
23. `agent-reach_stock_quote` 2026-10-03: NVDA 233.95 USD (+1.34%, mcap 5.65T, PE 29.17),
    TSM 472.78 USD (+2.96%, mcap 2.45T, PE 35.33) — source yfinance.
24. `openresearch_get_company_financials` INTC: FY24 rev 53.101B, net −18.756B;
    FY23 rev 54.228B — source SEC EDGAR 10-K.
25. `openresearch_search_sec_filings` TSMC/Intel/ASML scaling-risk 8-K/6-K hits.
26. GDELT/news 2026-09: SiC 6-inch, Nexstrom 12-inch 2D wafers $12M, wafer-equipment forecast.

## Reproducibility method
27. free-search research brief 2026: code-first DEVSIM + orchestration (ViennaTools)
    + deck-driven Sentaurus/ATLAS + geometry COMSOL — adopted here as
    Python-first physics + scripted sweeps + JSON thresholds + Docker pin.
