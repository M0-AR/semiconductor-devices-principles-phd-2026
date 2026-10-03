"""MOS capacitor: flatband, threshold, C-V (high-frequency ideal)."""
import numpy as np
from .constants import q, EPS_SI, EPS_OX, Vt, ni_si, NC_SI, T0

def fermi_potential(Na, T=T0):
    """Bulk potential phi_F = Vt*ln(Na/ni) [V] for p-substrate."""
    return Vt(T)*float(np.log(Na/ni_si(T)))

def depletion_charge(Na, phis, T=T0):
    """Depletion charge Qdep [C/cm^2] = sqrt(2 q eps_si Na * phis). Na cm^-3, phis V."""
    eps_cm = EPS_SI/100.0
    return float(np.sqrt(2*q*eps_cm*Na*np.maximum(phis,0)))

def threshold_voltage(Na, tox_nm, Qox_q=0.0, phi_ms=0.0, T=T0):
    """Vth = 2 phi_F + Qdep/Cox (+ phi_ms + Qox terms). tox in nm.

    Qox_q: oxide charge in units of q/cm^2 (positive). phi_ms: workfunction diff [V].
    """
    phi_F = fermi_potential(Na, T)
    Cox = (EPS_OX/100.0)/(tox_nm*1e-7)  # F/cm^2
    Qdep = depletion_charge(Na, 2*phi_F, T)
    Qox = Qox_q*q
    return float(phi_ms - Qox/Cox + 2*phi_F + Qdep/Cox)

def mos_cv(Vg, Na=1e16, tox_nm=5.0, Area=1e-4, T=T0):
    """Ideal high-frequency MOS C(Vg) [F] (p-sub): accum -> Cox, depl dip, inv -> Cmin.

    Piecewise textbook model anchored at Vfb=0, Vth from threshold_voltage().
    Smooth via tanh blending for differentiability.
    """
    Vg = np.asarray(Vg, dtype=float)
    Cox = (EPS_OX/100.0)/(tox_nm*1e-7)*Area
    Vth = threshold_voltage(Na, tox_nm, T=T)
    phi_F = fermi_potential(Na, T)
    # depletion min capacitance: Wdmax = sqrt(4 eps phi_F/(q Na))
    eps_cm = EPS_SI/100.0
    Wdmax_cm = np.sqrt(4*eps_cm*phi_F/(q*Na))
    Cdep_min = eps_cm*Area/Wdmax_cm
    Cmin = 1.0/(1.0/Cox+1.0/Cdep_min)
    # blend: accumulation (Vg<0): Cox; depletion (0<Vg<Vth): linear dip; inversion: Cmin
    C = np.empty_like(Vg)
    for i,v in enumerate(np.atleast_1d(Vg)):
        if v <= 0: C[i] = Cox
        elif v >= Vth: C[i] = Cmin
        else:
            f = v/Vth
            C[i] = Cox - (Cox-Cmin)*np.sin(f*np.pi/2)**0.7
    return C if C.shape != () else float(C)
