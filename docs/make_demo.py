"""Generate docs/demo.mp4 + docs/demo.gif (30s-style animated walkthrough).

Frames (verified, deterministic):
 1. Diode I-V grows with bias (Shockley n=1)
 2. BJT Gummel Ic/Ib exponential rise
 3. MOS C-V dip at depletion
 4. MOSFET planar vs FinFET vs GAA transfer (the 754x Ioff story)
 5. Moore's law 1971->2024 + SQ limit vs NREL records
Stitched into one MP4 (ffmpeg) + GIF preview for README.
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "src"))
from sdp import pn_junction as pn, bjt, mos, mosfet, scaling, opto

OUT_MP4 = os.path.join(REPO, "docs", "demo.mp4")
OUT_GIF = os.path.join(REPO, "docs", "demo.gif")

fig, axes = plt.subplots(2, 3, figsize=(12, 7))
fig.suptitle("Semiconductor Devices Principles — 60-second animated demo", fontsize=13, fontweight="bold")
axs = axes.flat

V = np.linspace(-1, 0.8, 300)
Vbe = np.linspace(0.3, 0.85, 200)
Vg_cv = np.linspace(-1, 2, 300)
Vgs_t = np.linspace(0, 1.2, 200)

def init():
    for a in axs:
        a.clear()
    return []

def frame(k):
    f = (k + 1) / 60.0  # progress 0..1 across ~60 frames
    for a in axs:
        a.clear()
    # 1. diode
    n = min(1 + f, 2.0)
    axs[0].semilogy(V, np.maximum(pn.shockley_iv(V, 1e-14, 1.0), 1e-16), label="n=1")
    axs[0].semilogy(V, np.maximum(pn.shockley_iv(V, 1e-14, n), 1e-16), "--", label=f"sweep n={n:.2f}")
    axs[0].set_title("1) Diode: one-way street"); axs[0].set_xlabel("V [V]"); axs[0].legend(fontsize=7)
    # 2. BJT gummel progressive
    m = max(10, int(len(Vbe) * f))
    Ic, Ib = bjt.gummel_plot(Vbe[:m])
    axs[1].semilogy(Vbe[:m], Ic, label="Ic"); axs[1].semilogy(Vbe[:m], Ib, label="Ib")
    axs[1].set_title("2) BJT: small base, big collector"); axs[1].legend(fontsize=7)
    # 3. MOS C-V progressive
    m3 = max(10, int(len(Vg_cv) * f))
    axs[2].plot(Vg_cv[:m3], mos.mos_cv(Vg_cv[:m3], Na=1e16, tox_nm=5.0) * 1e12)
    axs[2].set_title("3) MOS capacitor: charge bucket"); axs[2].set_xlabel("Vg [V]"); axs[2].set_ylabel("C [pF]")
    # 4. MOSFET arch
    for arch, kw, ls in [("planar", dict(n_sub=1.6, dibl=0.15), "-"), ("finfet", dict(n_sub=1.25, dibl=0.06), "--"), ("gaa", dict(n_sub=1.08, dibl=0.03), ":")]:
        Id = mosfet.mosfet_ids(Vgs_t, 1.0, W_um=10, L_um=0.02, tox_nm=1.0, mu0=300, Vth=0.35, lam=0.05, **kw)
        upto = max(10, int(len(Vgs_t) * f))
        axs[3].semilogy(Vgs_t[:upto], np.maximum(np.atleast_1d(Id)[:upto], 1e-13), ls, label=arch)
    axs[3].set_title("4) FinFET/GAA: 754x less leak"); axs[3].legend(fontsize=7)
    # 5. Moore
    import csv
    rows = list(csv.DictReader(open(os.path.join(REPO, "data", "moore_transistor_counts.csv"))))
    yrs = np.array([int(r["year"]) for r in rows]); cnt = np.array([float(r["transistors"]) for r in rows])
    upto5 = max(2, int(len(yrs) * f))
    axs[4].semilogy(yrs[:upto5], cnt[:upto5], "o-")
    axs[4].set_title("5) Moore: 2.3k to 208B"); axs[4].set_xlabel("year")
    # 6. SQ
    Eg = np.linspace(0.8, 2.0, 200)
    sq = np.array([opto.sq_limit(e) for e in Eg]) * 100
    upto6 = max(10, int(len(Eg) * f))
    axs[5].plot(Eg[:upto6], sq[:upto6], label="SQ limit")
    axs[5].plot([1.12, 1.42, 1.53], [26.7, 29.1, 26.1], "o", label="records")
    axs[5].set_title("6) Solar ceiling 33.7%"); axs[5].legend(fontsize=7)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    return []

anim = FuncAnimation(fig, frame, frames=60, init_func=init, blit=False)
anim.save(OUT_GIF, writer=PillowWriter(fps=10))
print("wrote", OUT_GIF, os.path.getsize(OUT_GIF), "bytes")

# mp4 via ffmpeg from gif (verified toolchain present)
import subprocess
r = subprocess.run(["ffmpeg", "-y", "-i", OUT_GIF, "-movflags", "faststart",
                    "-pix_fmt", "yuv420p", "-vf", "scale=1280:-2", OUT_MP4],
                   capture_output=True, text=True)
print(r.returncode, r.stderr[-500:] if r.stderr else "ffmpeg ok")
print("wrote", OUT_MP4, os.path.getsize(OUT_MP4) if os.path.exists(OUT_MP4) else "MISSING", "bytes")
