"""End-to-end experiment runner: reproduces every figure + table in README/PAPER."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sdp import pn_junction as pn, bjt, mos, mosfet, scaling, opto
from sdp.live_verify import fetch_live, SNAPSHOT

FIG = os.path.join(os.path.dirname(__file__), "..", "benchmarks", "results")
os.makedirs(FIG, exist_ok=True)

def fig_pn():
    V = np.linspace(-1, 0.8, 400)
    for n, ls in [(1.0, "-"), (1.5, "--"), (2.0, ":")]:
        plt.semilogy(V, np.maximum(pn.shockley_iv(V, 1e-14, n), 1e-16), ls, label=f"n={n}")
    plt.xlabel("V [V]"); plt.ylabel("I [A] log"); plt.legend(); plt.title("Shockley diode I-V (Is=1e-14A)")
    plt.savefig(f"{FIG}/fig_pn_iv.png", dpi=150); plt.close()

def fig_bjt():
    Vbe = np.linspace(0.3, 0.85, 200)
    Ic, Ib = bjt.gummel_plot(Vbe)
    plt.semilogy(Vbe, Ic, label="Ic"); plt.semilogy(Vbe, Ib, label="Ib")
    plt.xlabel("Vbe [V]"); plt.ylabel("I [A]"); plt.legend(); plt.title("Gummel plot betaF=100")
    plt.savefig(f"{FIG}/fig_bjt_gummel.png", dpi=150); plt.close()

def fig_mos():
    Vg = np.linspace(-1, 2, 400)
    C = mos.mos_cv(Vg, Na=1e16, tox_nm=5.0)
    plt.plot(Vg, C*1e12); plt.xlabel("Vg [V]"); plt.ylabel("C [pF]")
    plt.title("Ideal HF MOS C-V (Na=1e16, tox=5nm)")
    plt.savefig(f"{FIG}/fig_mos_cv.png", dpi=150); plt.close()

def fig_mosfet():
    Vgs = np.linspace(0, 3, 200)
    for arch, kw in [("planar", dict(n_sub=1.6, dibl=0.15)), ("finfet", dict(n_sub=1.25, dibl=0.06)), ("gaa", dict(n_sub=1.08, dibl=0.03))]:
        Id = mosfet.mosfet_ids(Vgs, 1.0, W_um=10, L_um=0.02, tox_nm=1.0, mu0=300, Vth=0.35, lam=0.05, **kw)
        plt.semilogy(Vgs, np.maximum(Id, 1e-13), label=arch)
    plt.xlabel("Vgs [V] @Vds=1V"); plt.ylabel("Id [A] log"); plt.legend(); plt.title("Planar vs FinFET vs GAA transfer (L=20nm)")
    plt.savefig(f"{FIG}/fig_mosfet_arch.png", dpi=150); plt.close()
    Vds = np.linspace(0, 1.5, 200)
    for Vg in [0.8, 1.2, 1.6]:
        Id = mosfet.mosfet_ids(Vg, Vds, W_um=10, L_um=1.0, tox_nm=5.0, mu0=400, Vth=0.7)
        plt.plot(Vds, Id*1e3, label=f"Vgs={Vg}V")
    plt.xlabel("Vds [V]"); plt.ylabel("Id [mA]"); plt.legend(); plt.title("MOSFET output characteristics")
    plt.savefig(f"{FIG}/fig_mosfet_output.png", dpi=150); plt.close()

def fig_scaling():
    import csv
    rows = list(csv.DictReader(open(os.path.join(os.path.dirname(__file__), "..", "data", "moore_transistor_counts.csv"))))
    yrs = np.array([int(r["year"]) for r in rows]); cnt = np.array([float(r["transistors"]) for r in rows])
    a, b, dbl = scaling.moore_fit(yrs, cnt)
    plt.semilogy(yrs, cnt, "o", label="public counts")
    yg = np.linspace(1971, 2030, 100)
    plt.semilogy(yg, 2**(a+b*yg), "--", label=f"fit dbl={dbl:.2f}yr")
    plt.xlabel("year"); plt.ylabel("transistors"); plt.legend(); plt.title("Moore's law fit")
    plt.savefig(f"{FIG}/fig_moore.png", dpi=150); plt.close()
    print(f"Moore doubling: {dbl:.2f} yr")

def fig_opto():
    Eg = np.linspace(0.8, 2.0, 200)
    sq = [opto.sq_limit(e) for e in Eg]
    plt.plot(Eg, np.array(sq)*100, label="SQ limit")
    import csv
    for r in csv.DictReader(open(os.path.join(os.path.dirname(__file__), "..", "data", "nrel_solar_records.csv"))):
        if r["Eg_eV"]:
            plt.plot(float(r["Eg_eV"]), float(r["eta_record_2024"])*100, "o", label=r["tech"])
    plt.xlabel("Eg [eV]"); plt.ylabel("efficiency [%]"); plt.legend(fontsize=7); plt.title("SQ limit vs NREL records")
    plt.savefig(f"{FIG}/fig_sq.png", dpi=150); plt.close()

def fig_live():
    live, used = fetch_live()
    print("live_verify used_live=", used)
    with open(f"{FIG}/live_market.json", "w") as f:
        import json
        json.dump({"used_live": used, "live": live, "snapshot": SNAPSHOT}, f, indent=2, default=str)

if __name__ == "__main__":
    fig_pn(); fig_bjt(); fig_mos(); fig_mosfet(); fig_scaling(); fig_opto(); fig_live()
    print("figures written to benchmarks/results/")
