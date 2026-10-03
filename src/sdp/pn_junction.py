"""PN junction physics: Vbi, depletion width, Shockley I-V, capacitances.

Equations follow Sze & Ng Ch.2 and Pierret Ch.5-6 (abrupt junction).
All doping in cm^-3, lengths in cm internally, areas in cm^2.
"""
import numpy as np
from .constants import q, eps0, EPS_SI, Vt, ni_si, T0

EPS = EPS_SI  # F/m

def built_in_potential(Na, Nd, T=T0):
    """Vbi = Vt*ln(Na*Nd/ni^2) [V]."""
    ni = ni_si(T)
    return Vt(T) * float(np.log(Na * Nd / ni**2))

def depletion_width(Na, Nd, V=0.0, T=T0):
    """Abrupt-junction depletion width W [um] at applied bias V (V>0 fwd)."""
    Vbi = built_in_potential(Na, Nd, T)
    eps_cm = EPS * 100.0  # F/cm (1 F/m = 100 F/cm? careful: 1m=100cm so F/m /100 = F/cm)
    # Actually: eps [F/m] -> [F/cm] divide by 100.
    eps_cm = EPS / 100.0
    denom = q * (Na + Nd) / (2 * eps_cm) * 0  # placeholder unused
    # Standard: W = sqrt(2*eps/q * (Na+Nd)/(Na*Nd) * (Vbi - V))
    Na_m = Na * 1e6  # cm^-3 -> m^-3
    Nd_m = Nd * 1e6
    W_m = np.sqrt(2 * EPS / q * (Na_m + Nd_m) / (Na_m * Nd_m) * max(Vbi - V, 1e-6))
    return float(W_m * 1e6)  # um

def depletion_edges(Na, Nd, V=0.0, T=T0):
    """Return (xp, xn) in um."""
    W = depletion_width(Na, Nd, V, T)
    xp = W * Nd / (Na + Nd)
    xn = W * Na / (Na + Nd)
    return xp, xn

def saturation_current(Na, Nd, Dn=25.0, Dp=10.0, Ln=10e-4, Lp=5e-4, Area=1e-4, T=T0):
    """Ideal reverse saturation current Is [A] (long-base diode).

    Dn,Dp in cm^2/s; Ln,Lp in cm; Area in cm^2.
    Is = q*A*(Dp*pn0/Lp + Dn*np0/Ln), pn0=ni^2/Na, np0=ni^2/Nd.
    Defaults give Is ~ 1e-14..1e-12 A for Si at 300K (textbook range).
    """
    ni = ni_si(T)
    pn0 = ni**2 / Na
    np0 = ni**2 / Nd
    Is = q * Area * (Dp * pn0 / Lp + Dn * np0 / Ln)
    return float(Is)

def shockley_iv(V, Is=1e-14, n=1.0, T=T0):
    """Shockley diode I = Is*(exp(V/(n*Vt))-1). V scalar or array -> A."""
    V = np.asarray(V, dtype=float)
    return Is * (np.exp(V / (n * Vt(T))) - 1.0)

def depletion_capacitance(Na, Nd, Area=1e-4, V=0.0, T=T0):
    """Zero/reverse-bias depletion capacitance Cj [F]: Cj = Cj0/sqrt(1-V/Vbi)."""
    Vbi = built_in_potential(Na, Nd, T)
    eps_cm = EPS / 100.0  # F/cm
    Na_cm, Nd_cm = Na, Nd
    W_cm = depletion_width(Na, Nd, V, T) * 1e-4  # um -> cm
    W_cm = max(W_cm, 1e-9)
    return float(eps_cm * Area / W_cm)

def diffusion_capacitance(I, tau=1e-7, n=1.0, T=T0):
    """Diffusion capacitance Cd = (tau*I)/(n*Vt) for forward current I [A]."""
    I = np.asarray(I, dtype=float)
    return tau * np.maximum(I, 0) / (n * Vt(T))

def ideality_from_iv(V, I, T=T0):
    """Extract ideality n from slope of ln(I) vs V in forward region.

    n = 1/(Vt * d lnI/dV). Uses linear least squares on provided points.
    Returns (n, Is_fit).
    """
    V = np.asarray(V, dtype=float); I = np.asarray(I, dtype=float)
    m = I > 0
    V, I = V[m], I[m]
    slope, intercept = np.polyfit(V, np.log(I), 1)
    n = 1.0 / (slope * Vt(T))
    Is = float(np.exp(intercept))
    return float(n), Is

def schottky_barrier_current(V, phi_B=0.7, Area=1e-4, T=T0, A_star=112.0):
    """Thermionic-emission Schottky I = A*A**T^2 exp(-q phi_B/kT)(exp(qV/kT)-1)."""
    A = Area  # cm^2
    J0 = A_star * T**2 * np.exp(-phi_B / Vt(T))  # A/cm^2
    V = np.asarray(V, dtype=float)
    return A * J0 * (np.exp(V / Vt(T)) - 1.0)
