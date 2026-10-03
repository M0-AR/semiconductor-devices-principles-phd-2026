import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from sdp.pn_junction import *
from sdp.bjt import *
from sdp.mos import *
from sdp.mosfet import *
from sdp.scaling import *
from sdp.opto import *
import numpy as np

def test_Vbi_range():
    from sdp.pn_junction import built_in_potential
    v = built_in_potential(1e16, 1e16)
    assert 0.6 < v < 0.85, v

def test_Is_range():
    from sdp.pn_junction import saturation_current
    Is = saturation_current(1e16, 1e16)
    assert 1e-16 < Is < 1e-10, Is

def test_ideality_roundtrip():
    from sdp.pn_junction import shockley_iv, ideality_from_iv
    V = np.linspace(0.3, 0.7, 9)
    n, _ = ideality_from_iv(V, shockley_iv(V, 1e-14, 1.0))
    assert abs(n-1.0) < 0.05, n

def test_bjt_beta():
    from sdp.bjt import ebers_moll
    Ic, Ib, Ie = ebers_moll(0.7, -1.0, Is=1e-16, betaF=100)
    assert 90 < float(Ic/Ib) < 115

def test_mos_vth():
    from sdp.mos import threshold_voltage
    assert 0.4 < threshold_voltage(1e16, 5.0) < 1.2

def test_mosfet_idsat():
    from sdp.mosfet import mosfet_ids
    Id = float(mosfet_ids(2.0, 2.0, W_um=10, L_um=1.0, tox_nm=5.0, mu0=400, Vth=0.7, lam=0.0, subthresh=False))
    assert 1e-4 < Id < 5e-3, Id

def test_SS():
    from sdp.mosfet import subthreshold_swing
    assert 80 < subthreshold_swing(1.4) < 90

def test_SQ():
    from sdp.opto import sq_limit
    assert 0.32 < sq_limit(1.34) < 0.35
