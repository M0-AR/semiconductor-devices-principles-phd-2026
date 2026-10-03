"""Physical constants and Si material parameters (300 K defaults).

All values SI unless noted. Sources: Sze & Ng Physics of Semiconductor
Devices (4th ed.), Pierret Semiconductor Device Fundamentals, BSIM4.8.3
manual (UC Berkeley, 2025-05-19, verified live via bsim.berkeley.edu),
NREL Best Research-Cell Efficiency Chart.
"""
import numpy as np

# Fundamental
q = 1.602176634e-19       # C
kB = 1.380649e-23         # J/K
h = 6.62607015e-34        # J s
hbar = h / (2 * np.pi)
eps0 = 8.8541878128e-12   # F/m
c = 299792458.0           # m/s

# Silicon @300K
EG_SI_300 = 1.12          # eV
NI_SI_300 = 1.0e10        # cm^-3 (accepted textbook value; measured 0.97-1.0e10)
EPS_SI = 11.7 * eps0      # F/m
EPS_OX = 3.9 * eps0       # F/m (SiO2)
NC_SI = 2.8e19            # cm^-3 effective conduction band DOS
NV_SI = 1.04e19           # cm^-3 effective valence band DOS
MU_N_SI = 1350.0          # cm^2/Vs low-field electron mobility
MU_P_SI = 480.0           # cm^2/Vs low-field hole mobility
VSAT_SI = 1.0e7           # cm/s saturation velocity

T0 = 300.0                # K

def Vt(T=T0):
    """Thermal voltage in volts."""
    return kB * T / q

def ni_si(T=T0):
    """Intrinsic carrier concentration of Si (cm^-3) with Varshni Eg(T).

    Uses Varshni: Eg(T) = 1.17 - 4.73e-4*T^2/(T+636)  [eV],
    scaled from ni(300K)=1.0e10 via ni^2 ~ T^3*exp(-Eg/kT).
    """
    Eg_T = 1.17 - 4.73e-4 * T**2 / (T + 636.0)
    Eg_300 = 1.17 - 4.73e-4 * T0**2 / (T0 + 636.0)
    ratio = (T / T0) ** 3 * np.exp(-Eg_T / Vt(T) + Eg_300 / Vt(T0))
    return NI_SI_300 * float(np.sqrt(ratio))
