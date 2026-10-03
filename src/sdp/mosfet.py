"""MOSFET Level-1 + subthreshold + mobility degradation + velocity saturation + SCE.

NMOS convention. All voltages in V, currents in A, dimensions in um (converted).
Model hierarchy:
  L0 classical square-law (cutoff/linear/saturation)
  L1 adds lambda (channel-length modulation)
  L2 adds subthreshold exponential + DIBL + mobility degradation + velocity saturation
  FinFET/GAA: improved electrostatics via scale-length factor -> lower DIBL/SS.
"""
import numpy as np
from .constants import q, EPS_SI, EPS_OX, Vt, T0
from .mos import threshold_voltage

def Cox_per_area(tox_nm):
    """Cox' [F/cm^2]."""
    return (EPS_OX/100.0)/(tox_nm*1e-7)

def mosfet_ids(Vgs, Vds, W_um=10.0, L_um=1.0, tox_nm=5.0, mu0=400.0,
                Vth=0.7, lam=0.02, T=T0, subthresh=True, n_sub=1.4,
                vsat_on=False, theta=0.0, dibl=0.0):
    """Drain current Id [A] (scalar or array broadcast).

    mu0: cm^2/Vs. theta: mobility degradation [1/V]. dibl: Vth shift per Vds [V/V].
    vsat_on: apply velocity-saturation cap Id <= W*Cox*(Vgs-Vth)*vsat.
    """
    Vgs_a = np.atleast_1d(np.asarray(Vgs, dtype=float))
    Vds_a = np.atleast_1d(np.asarray(Vds, dtype=float))
    Vgs_a, Vds_a = np.broadcast_arrays(Vgs_a, Vds_a)
    Cox = Cox_per_area(tox_nm)  # F/cm^2
    W_cm, L_cm = W_um*1e-4, L_um*1e-4
    beta = mu0*Cox*W_cm/L_cm  # A/V^2 scalar
    Vth_eff = Vth - dibl*Vds_a
    Vov = Vgs_a - Vth_eff
    Id = np.zeros_like(Vgs_a, dtype=float)
    # above threshold
    on = Vov > 0
    Vdsat = np.minimum(Vds_a, np.maximum(Vov, 0))
    # mobility degradation: mu_eff = mu0/(1+theta*Vov)
    mu_factor = 1.0/(1.0+theta*np.maximum(Vov, 0))
    # linear-region base
    lin = beta*mu_factor*(Vov*Vdsat - 0.5*Vdsat**2)
    sat_mask = on & (Vds_a >= Vov)
    lin[sat_mask] = beta*mu_factor[sat_mask]*0.5*Vov[sat_mask]**2*(1+lam*Vds_a[sat_mask])
    Id[on] = lin[on]
    # velocity saturation cap
    if vsat_on:
        vsat = 1.0e7  # cm/s
        Id_cap = W_cm*Cox*np.maximum(Vov, 0)*vsat
        Id = np.minimum(Id, Id_cap)
    # subthreshold
    if subthresh:
        off = ~on
        I0 = beta*(Vt(T)**2)*0.5
        Id[off] = I0*(np.exp((Vgs_a[off]-Vth_eff[off])/(n_sub*Vt(T))))*(1-np.exp(-Vds_a[off]/Vt(T)))
    if np.ndim(Vgs) == 0 and np.ndim(Vds) == 0:
        return float(Id[0])
    return Id

def subthreshold_swing(n_sub=1.4, T=T0):
    """SS [mV/dec] = n*Vt*ln(10)*1000."""
    return float(n_sub*Vt(T)*np.log(10)*1000)

def finfet_advantage(L_um=0.02, tox_nm=1.0, architecture="planar"):
    """Return dict of effective SS, DIBL scale factors (textbook trend).

    Planar DIBL ~ 150 mV/V at L=20nm; FinFET ~ 60; GAA ~ 30 (representative).
    Used to parametrize mosfet_ids(n_sub, dibl) comparisons.
    """
    table = {"planar": (1.6, 0.15), "finfet": (1.25, 0.06), "gaa": (1.08, 0.03), "nanosheet": (1.05, 0.025)}
    n, d = table.get(architecture.lower(), (1.6, 0.15))
    return {"n_sub": n, "dibl_V_per_V": d,
            "SS_mV_per_dec": subthreshold_swing(n)}
