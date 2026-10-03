"""Optoelectronics: photodiode, solar detailed-balance (SQ), LED."""
import numpy as np
from .constants import q, h, c

# Shockley-Queisser single-junction limit (AM1.5G, 300K) sampled from
# Rühle 2016 / Shockley & Queisser 1961 tables (see docs/SOURCES.md).
# Eg[eV] -> max efficiency fraction.
SQ_TABLE = np.array([
    [0.8, 0.22], [1.0, 0.304], [1.12, 0.337], [1.34, 0.337],
    [1.4, 0.331], [1.5, 0.317], [1.6, 0.300], [1.8, 0.262], [2.0, 0.216],
])

# NREL-certified single-junction records (2024, see docs/SOURCES.md)
NREL_RECORDS = {
    "Si": {"Eg": 1.12, "eta": 0.267, "note": "26.7% Kaneka heterojunction IBC"},
    "GaAs": {"Eg": 1.42, "eta": 0.291, "note": "29.1% Alta Devices thin-film"},
    "Perovskite": {"Eg": 1.53, "eta": 0.261, "note": "26.1% single-junction record 2024"},
    "Tandem_perovskite_Si": {"Eg": None, "eta": 0.339, "note": "33.9% tandem exceeds SQ single-junction"},
}

def sq_limit(Eg):
    """Interpolate SQ efficiency for bandgap Eg [eV]."""
    Eg = np.asarray(Eg, float)
    return float(np.interp(Eg, SQ_TABLE[:,0], SQ_TABLE[:,1])) if Eg.ndim==0 else np.interp(Eg, SQ_TABLE[:,0], SQ_TABLE[:,1])

def responsivity(wavelength_nm, qe=1.0):
    """Photodiode responsivity R = qe*q*lambda/(h*c) [A/W]."""
    lam = np.asarray(wavelength_nm, float)*1e-9
    return qe*q*lam/(h*c)

def solar_iv(V, Jsc=40e-3, J0=1e-12, n=1.0, T=300.0, Rs=0.0, Rsh=1e9):
    """Ideal solar-cell J(V) [A/cm^2] (single-diode, V in volts)."""
    from .constants import Vt
    vt = Vt(T)
    V = np.asarray(V, float)
    return Jsc - J0*(np.exp((V)/ (n*vt))-1.0) - V/Rsh

def led_wallplug(iv_watts, optical_watts):
    """LED wall-plug efficiency = P_opt / P_in."""
    return float(np.asarray(optical_watts)/np.asarray(iv_watts))
