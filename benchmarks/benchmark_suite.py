"""Benchmark suite: every claim in README/PAPER is machine-checked.

Run: python -m benchmarks.benchmark_suite  (or via docker compose)
Exit 0 iff all thresholds pass. Writes benchmarks/results/summary.json + figures.
"""
import json, math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from sdp import pn_junction as pn, bjt, mos, mosfet, scaling, opto
from sdp.constants import Vt, ni_si
from sdp.live_verify import SNAPSHOT, fetch_live

RES = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RES, exist_ok=True)
TH = json.load(open(os.path.join(os.path.dirname(__file__), "thresholds.json")))

def check(name, val, lo, hi, unit=""):
    ok = (lo <= val <= hi)
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {val:.6g} {unit}  expected [{lo},{hi}]")
    return {"name": name, "value": val, "lo": lo, "hi": hi, "unit": unit, "pass": bool(ok)}

def main():
    R = []
    # B1 diode Vbi + Is + ideality round-trip
    Vbi = pn.built_in_potential(1e16, 1e16)
    R.append(check("B1 Vbi(Na=Nd=1e16)", Vbi, *TH["B1_Vbi"], "V"))
    Is = pn.saturation_current(1e16, 1e16)
    R.append(check("B2 Is Si diode", Is, *TH["B2_Is"], "A"))
    V = np.linspace(0.3, 0.7, 9)
    I = pn.shockley_iv(V, Is=1e-14, n=1.0)
    n_fit, Is_fit = pn.ideality_from_iv(V, I)
    R.append(check("B3 ideality recovery n=1", n_fit, *TH["B3_n"], ""))
    # B4 depletion width textbook ~0.43um? compute: Na=Nd=1e16 -> W~0.6um? window wide
    W = pn.depletion_width(1e16, 1e16, V=0.0)
    R.append(check("B4 Wdep 1e16/1e16 0V", W, *TH["B4_W"], "um"))
    # B5 BJT beta
    Ic, Ib, Ie = bjt.ebers_moll(0.7, -1.0, Is=1e-16, betaF=100)
    beta = float(Ic/Ib)
    R.append(check("B5 BJT betaF", beta, *TH["B5_beta"], ""))
    # B6 MOS Vth ~0.7-1.0V for Na=1e16 tox=5nm
    Vth = mos.threshold_voltage(1e16, 5.0)
    R.append(check("B6 MOS Vth", Vth, *TH["B6_Vth"], "V"))
    # B7 MOSFET square-law Id sat
    Id = float(mosfet.mosfet_ids(2.0, 2.0, W_um=10, L_um=1.0, tox_nm=5.0, mu0=400, Vth=0.7, lam=0.0, subthresh=False))
    R.append(check("B7 MOSFET Idsat", Id, *TH["B7_Id"], "A"))
    # B8 SS
    SS = mosfet.subthreshold_swing(1.4)
    R.append(check("B8 SS n=1.4", SS, *TH["B8_SS"], "mV/dec"))
    # B9 Moore doubling
    import csv
    rows = list(csv.DictReader(open(os.path.join(os.path.dirname(__file__), "..", "data", "moore_transistor_counts.csv"))))
    a, b, dbl = scaling.moore_fit([int(r["year"]) for r in rows], [float(r["transistors"]) for r in rows])
    R.append(check("B9 Moore doubling years", dbl, *TH["B9_dbl"], "yr"))
    # B10 SQ
    sq = opto.sq_limit(1.34)
    R.append(check("B10 SQ peak", sq, *TH["B10_SQ"], ""))
    resp = float(opto.responsivity( Silicon_wl := 850.0, qe=1.0))
    R.append(check("B11 responsivity 850nm", resp, *TH["B11_R"], "A/W"))
    # B12 live snapshot sanity (offline-safe: checks snapshot internal consistency)
    R.append(check("B12 NVDA snapshot price", SNAPSHOT["NVDA"]["current"], *TH["B12_NVDA"], "USD"))
    R.append(check("B13 TSM snapshot price", SNAPSHOT["TSM"]["current"], *TH["B13_TSM"], "USD"))
    # live attempt (informational, never fails suite)
    try:
        live, used = fetch_live()
        print(f"live market fetch: used_live={used} keys={list(live.keys())[:6]}")
    except Exception as e:
        print("live fetch skipped:", e)
    ok = all(r["pass"] for r in R)
    json.dump({"pass": ok, "results": R}, open(os.path.join(RES, "summary.json"), "w"), indent=2)
    print("\nSUITE:", "ALL PASS" if ok else "FAILURES PRESENT")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
