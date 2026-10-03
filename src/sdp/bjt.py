"""BJT: Ebers-Moll, gain, Early effect, switching charge (Gummel-Poon lite)."""
import numpy as np
from .constants import Vt, T0

def ebers_moll(Vbe, Vbc, Is=1e-16, betaF=100.0, betaR=1.0, T=T0):
    """Static Ebers-Moll: returns (Ic, Ib, Ie) for NPN [A].

    Ic = Is*(exp(Vbe/Vt)-1) - (Is/betaR... ) full coupled form:
      IF = Is*(exp(Vbe/Vt)-1); IR = Is*(exp(Vbc/Vt)-1)
      Ic = alphaF*IF - IR ; Ib = (1-alphaF)*IF + (1-alphaR)*IR ; Ie = IF - alphaR*IR
    with alphaF = betaF/(betaF+1).
    """
    vt = Vt(T)
    IF = Is * (np.exp(np.asarray(Vbe)/vt) - 1.0)
    IR = Is * (np.exp(np.asarray(Vbc)/vt) - 1.0)
    aF = betaF/(betaF+1.0); aR = betaR/(betaR+1.0)
    Ic = aF*IF - IR
    Ib = (1-aF)*IF + (1-aR)*IR
    Ie = IF - aR*IR
    return Ic, Ib, Ie

def ic_vs_vce(Vce, Vbe=0.7, Is=1e-16, betaF=100.0, VA=50.0, T=T0):
    """Forward-active Ic with Early effect: Ic = betaF*Ib0*(1+Vce/VA)."""
    vt = Vt(T)
    Ib0 = Is/betaF * (np.exp(np.asarray(Vbe)/vt)-1.0) * betaF  # = Is*(exp-1)
    # Simpler: Ic0 = Is*betaF/(betaF+1)... use standard: Ic = Is*exp(Vbe/Vt)*(1+Vce/VA)
    Ic = Is * np.exp(np.asarray(Vbe)/vt) * (1.0 + np.asarray(Vce)/VA)
    return Ic

def beta_vs_ic(Ic, beta_max=120.0, Ic_knee=1e-3, Ic_fall=1e-1):
    """Illustrative beta roll-off (low-current recombination + high-current crowding)."""
    Ic = np.asarray(Ic, dtype=float)
    low = 1.0/(1.0 + Ic_knee/np.maximum(Ic,1e-15))
    high = 1.0/(1.0 + np.maximum(Ic,0)/Ic_fall)
    return beta_max*low*high + 1e-9

def gummel_plot(Vbe, Is=1e-16, betaF=100.0, nF=1.0, nR=1.0, T=T0):
    """Return (Ic, Ib) Gummel characteristics."""
    vt = Vt(T)
    Ic = Is*np.exp(np.asarray(Vbe)/(nF*vt))
    Ib = Ic/betaF
    return Ic, Ib

def cutoff_freq(gm, Cpi, Cmu):
    """fT = gm/(2 pi (Cpi+Cmu))."""
    return gm/(2*np.pi*(Cpi+Cmu))
