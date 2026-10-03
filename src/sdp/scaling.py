"""Technology scaling: Moore's law fit, Dennard scaling, power-density wall."""
import numpy as np

# Curated public transistor-count history (vendor announcements / Wikipedia).
# year, device, transistors. Verifiable; see docs/SOURCES.md.
MOORE_DATA = [
    (1971, "Intel 4004", 2.3e3),
    (1978, "Intel 8086", 2.9e4),
    (1989, "Intel 486", 1.18e6),
    (2000, "Pentium 4", 4.2e7),
    (2011, "Sandy Bridge-E", 2.27e9),
    (2017, "Apple A11", 4.3e9),
    (2020, "Apple M1", 1.6e10),
    (2022, "Apple M1 Ultra", 1.14e11),
    (2024, "NVIDIA Blackwell B200", 2.08e11),
]

def moore_fit(years, counts):
    """Fit log2(count) = a + b*year. Returns (a, b, doubling_years)."""
    years = np.asarray(years, float); counts = np.asarray(counts, float)
    y = np.log2(counts)
    b, a = np.polyfit(years, y, 1)
    return float(a), float(b), float(1.0/b)

def dennard_scale(s=0.7):
    """Dennard scaling factors for linear shrink s (<1): dims*s, V*s, f*1/s,
    power density constant. Returns dict."""
    return {"dim": s, "voltage": s, "freq": 1/s, "cap": s,
            "power": s**2, "power_density": 1.0}

def post_dennard_power(freq_scale, v_scale=1.0):
    """Power-density multiplier when voltage stops scaling: P_dens ~ v^2*f."""
    return float(v_scale**2 * freq_scale)
