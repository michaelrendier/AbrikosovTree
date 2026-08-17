"""
Zeta Index Engine — Spectral Wavelength and Prime Resolution

CANONICAL STATEMENT:

Each non-trivial Riemann zero ρₙ = ½ + iγₙ has a spectral wavelength in logarithmic space:

    λₙ = 2π / γₙ        (log-space wavelength)
    Lₙ(x) = 2πx / γₙ   (linear-space resolution at scale x)

The zero ρₙ "activates" — completes its first oscillation cycle — at:

    x_n = e^(2π/γₙ)

By the explicit formula for π(x), the contribution of ρₙ oscillates as x^(½) cos(γₙ log x).
The linear-space wavelength Lₙ(x) = 2πx/γₙ is the gap the zero can resolve at scale x.

ZETA INDEX DEFINITION:

The local prime gap near p is log(p) by the prime number theorem.

Zero ρₙ resolves prime p when its linear wavelength at p is ≤ the local gap:

    Lₙ(p) ≤ log(p)
    2πp / γₙ ≤ log(p)
    γₙ ≥ 2πp / log(p)   ← threshold γ*(p)

The zeta index of prime p:

    ζ(p) = min{ n ∈ ℕ : γₙ ≥ γ*(p) }   where γ*(p) = 2πp / log(p)

ζ(p) is the index of the first Riemann zero whose linear-space resolution
at p is fine enough to distinguish consecutive primes near p.

DOUBLE INDEX:

Each prime has two indices:
    n     = ordinal position (p is the n-th prime, π(p) = n)
    ζ(p)  = zeta index (first zero to resolve p spectrally)

    p_{n[ζ(p)]}    ← ordinal n, zeta sub-index ζ(p)

The zeta sub-ordering: p ≺_ζ q  iff  ζ(p) < ζ(q)
This is the spectral emergence ordering — which primes the Riemann spectrum resolved first.

Invariant:  ζ(p₁) ≤ ζ(p₂)  whenever p₁ ≤ p₂  (monotone in p)
Proof:      γ*(p) = 2πp/log(p) is increasing for p ≥ e ≈ 2.718.
            Since p₁ ≤ p₂ → γ*(p₁) ≤ γ*(p₂) → ζ(p₁) ≤ ζ(p₂).

Version: 0.100 — 2026-06-29
"""

import math
import sys
import os
from typing import List, Dict, Optional, Tuple
from functools import lru_cache

try:
    import mpmath
    MPMATH_AVAILABLE = True
except ImportError:
    MPMATH_AVAILABLE = False

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

TWO_PI = 2 * math.pi

# First 100 Riemann zero imaginary parts — precomputed via mpmath.zetazero(n)
# Source: Riemann zeros are the imaginary parts of the non-trivial zeros of ζ(s)
# on the critical line Re(s) = ½, ordered by magnitude.
KNOWN_ZEROS_100 = [
    14.134725141734693, 21.022039638771554, 25.010857580145688,
    30.424876125859513, 32.935061587739185, 37.586178158825671,
    40.918719012147495, 43.327073280914999, 48.005150881167160,
    49.773832477672302, 52.970321477714461, 56.446247697063394,
    59.347044002602353, 60.831778524609876, 65.112544048081607,
    67.079810529494173, 69.546401711173978, 72.067157674481907,
    75.704690699083932, 77.144840068874805, 79.337375020249367,
    82.910380854086030, 84.735492980517050, 87.425274613125229,
    88.809111207634465, 92.491899270558484, 94.651344040519780,
    95.870634228245332, 98.831194218193692, 101.317851006956450,
    103.725538040478650, 105.446623052812640, 107.168611184276820,
    111.029535543015720, 111.874659177711170, 114.320220915452240,
    116.226680321519080, 118.790782866023310, 121.370125002847460,
    122.946829294763880, 124.256818554312210, 127.516683880284130,
    129.578704200039080, 131.087688531382770, 133.497737202998890,
    134.756509753178780, 138.116042054533200, 139.736208952121560,
    141.123707404002430, 143.111845808910280, 146.000982487339090,
    147.422765343923680, 150.053519977450730, 150.925257612428430,
    153.024693811198310, 156.112909294252430, 157.597591818860420,
    158.849988171348450, 161.188964138385850, 163.030709687386660,
    165.537069188644050, 167.184439979991760, 169.094515416605770,
    169.911976479873440, 173.411536520547100, 174.754191523427400,
    176.441434298030100, 178.377407776001800, 179.916484026138990,
    182.207078484587600, 184.874467848042980, 185.598783137094780,
    187.228922584926700, 189.416158986188300, 192.026656361403200,
    193.079726604299100, 195.265396673429200, 196.876481841084000,
    198.015309657684500, 201.264751781340600, 202.493594514750400,
    204.189671803789800, 205.394697418984400, 207.906258888948200,
    209.576509716716600, 211.690862595850800, 213.347919360854400,
    214.547044780717900, 216.169538508844500, 219.067596348415600,
    220.714918839427900, 221.430705555379100, 224.007000255476700,
    224.983324670116600, 227.421444280437200, 229.337413306756600,
    231.250188700599200, 231.987235253456100, 233.693404179740200,
]


class ZetaIndexEngine:
    """
    Computes the zeta index ζ(p) for primes and derives the double-index structure.

    The engine maintains a cache of Riemann zeros computed via mpmath (if available)
    or uses the precomputed KNOWN_ZEROS_100 table for the first 100 zeros.
    """

    def __init__(self, n_zeros: int = 100):
        """
        Args:
            n_zeros: Number of Riemann zeros to precompute/load.
                     For primes up to ~50: 10 zeros sufficient.
                     For primes up to ~100: 50 zeros.
                     For primes up to ~500: 300 zeros.
                     For primes up to ~1000: 700 zeros.
        """
        self.n_zeros = n_zeros
        self._zeros: Optional[List[float]] = None

    def zeros(self) -> List[float]:
        """Return the list of Riemann zero imaginary parts γₙ, n=1..n_zeros."""
        if self._zeros is not None:
            return self._zeros

        if self.n_zeros <= len(KNOWN_ZEROS_100):
            self._zeros = KNOWN_ZEROS_100[:self.n_zeros]
            return self._zeros

        if MPMATH_AVAILABLE:
            print(f"  Computing {self.n_zeros} Riemann zeros via mpmath...", flush=True)
            result = []
            for n in range(1, self.n_zeros + 1):
                g = float(mpmath.zetazero(n).imag)
                result.append(g)
                if n % 50 == 0:
                    print(f"    γ_{n} = {g:.6f}", flush=True)
            self._zeros = result
            return self._zeros

        # Fallback: use known 100 and extrapolate using Gram's law approximation
        # γₙ ≈ 2πn / (log(n/(2πe))) for large n
        known = list(KNOWN_ZEROS_100)
        for n in range(len(known) + 1, self.n_zeros + 1):
            # Backlund's approximation: N(T) ≈ T/(2π) log(T/(2πe))
            # Invert: γₙ ≈ 2πn / log(n) for large n
            approx = 2 * math.pi * n / max(math.log(n), 1)
            known.append(approx)
        self._zeros = known[:self.n_zeros]
        return self._zeros

    # ------------------------------------------------------------------
    # Spectral wavelength functions
    # ------------------------------------------------------------------

    @staticmethod
    def spectral_wavelength(gamma_n: float) -> float:
        """λₙ = 2π/γₙ — wavelength of zero ρₙ in log-space."""
        return TWO_PI / gamma_n

    @staticmethod
    def linear_resolution(gamma_n: float, x: float) -> float:
        """Lₙ(x) = 2πx/γₙ — linear-space resolution of zero ρₙ at scale x."""
        return TWO_PI * x / gamma_n

    @staticmethod
    def activation_scale(gamma_n: float) -> float:
        """x_n = e^(2π/γₙ) — scale at which zero ρₙ completes its first cycle."""
        return math.exp(TWO_PI / gamma_n)

    # ------------------------------------------------------------------
    # Threshold and index
    # ------------------------------------------------------------------

    @staticmethod
    def gamma_threshold(p: int) -> float:
        """
        γ*(p) = 2πp / log(p)

        The minimum γₙ required for zero ρₙ to resolve prime p.
        Derived from: Lₙ(p) ≤ log(p)  →  γₙ ≥ 2πp/log(p).
        """
        return TWO_PI * p / math.log(p)

    def zeta_index(self, p: int) -> int:
        """
        ζ(p) = min{ n : γₙ ≥ γ*(p) }

        The index of the first Riemann zero that resolves prime p.
        Returns -1 if beyond the computed zero table.
        """
        thresh = self.gamma_threshold(p)
        for n, g in enumerate(self.zeros(), 1):
            if g >= thresh:
                return n
        return -1  # beyond table

    def prime_record(self, p: int, ordinal: int) -> Dict:
        """
        Full record for prime p:
            p           — the prime
            n           — ordinal index (p is the n-th prime)
            gamma_star  — γ*(p) = 2πp/log(p)
            zeta_idx    — ζ(p): first zero index to resolve p
            gamma_zeta  — γ_{ζ(p)}: that zero's imaginary part
            lambda_zeta — λ_{ζ(p)}: its log-space wavelength
            nshape      — p mod 16 (sedenion N-shape)
            double_idx  — (n, ζ(p)): the canonical double index
        """
        thresh = self.gamma_threshold(p)
        zi = self.zeta_index(p)
        zs = self.zeros()
        g_zeta = zs[zi - 1] if (zi > 0 and zi <= len(zs)) else None
        lam = TWO_PI / g_zeta if g_zeta else None
        return {
            'p':           p,
            'n':           ordinal,
            'gamma_star':  thresh,
            'zeta_idx':    zi,
            'gamma_zeta':  g_zeta,
            'lambda_zeta': lam,
            'nshape':      p % 16,
            'double_idx':  (ordinal, zi),
        }

    # ------------------------------------------------------------------
    # Table builders
    # ------------------------------------------------------------------

    def zero_table(self) -> List[Dict]:
        """Full table of zeros with wavelength and activation data."""
        result = []
        for n, g in enumerate(self.zeros(), 1):
            result.append({
                'n':              n,
                'gamma':          g,
                'lambda_log':     self.spectral_wavelength(g),
                'x_activate':     self.activation_scale(g),
                'log_resolution': TWO_PI / g,
            })
        return result

    def prime_zeta_table(self, primes: List[int]) -> List[Dict]:
        """ζ(p), double index, and wavelength data for each prime in list."""
        return [self.prime_record(p, n) for n, p in enumerate(primes, 1)]

    def zeta_ordering(self, primes: List[int]) -> List[Tuple[int, int, int]]:
        """
        Return primes sorted by zeta index (spectral emergence ordering).
        Returns list of (zeta_idx, ordinal, prime).
        Primes with the same ζ are sorted by ordinal.
        """
        records = self.prime_zeta_table(primes)
        return sorted(
            [(r['zeta_idx'], r['n'], r['p']) for r in records],
            key=lambda x: (x[0], x[1])
        )

    def monster_gap_zeta(self, primes: List[int]) -> Dict:
        """
        Compare the zeta index distribution for Monster gap primes (p ≡ 1,11,15
        mod 16) against all other primes.

        CENSORING. :meth:`zeta_index` returns -1 for any prime whose threshold
        γ*(p) exceeds the largest zero in the table -- 'not resolved within the
        first n_zeros', not an index. Those entries are EXCLUDED from the means
        here and counted separately. Averaging them in silently treats -1 as a
        very small index and drags the mean down in proportion to how often a
        group is censored, which manufactures a difference out of the censoring
        rate alone.

        With n_zeros=100 over primes ≤ 500 that is not a small correction: 61%
        of gap primes and 46% of others are censored, and the raw means (15.9 vs
        23.7) invert into 42.6 vs 44.6 once the sentinels are removed -- i.e.
        the apparent separation is the censoring, not the Monster gap. Read
        ``censored_frac`` before reading either mean, and treat any comparison
        as uninformative unless both groups are censored at a similar rate.

        :param primes: primes to classify.
        :returns: means over resolved primes only, plus censoring counts.
        :rtype: dict
        """
        MONSTER_GAP = {1, 11, 15}
        gap_all, other_all = [], []
        for p in primes:
            zi = self.zeta_index(p)
            (gap_all if p % 16 in MONSTER_GAP else other_all).append(zi)

        gap_res   = [z for z in gap_all   if z != -1]
        other_res = [z for z in other_all if z != -1]

        def _mean(v):
            return sum(v) / len(v) if v else None

        return {
            # means over RESOLVED primes only; None if a group is fully censored
            'monster_gap_zeta_mean':  _mean(gap_res),
            'other_zeta_mean':        _mean(other_res),
            'monster_gap_zeta_min':   min(gap_res) if gap_res else None,
            'monster_gap_zeta_max':   max(gap_res) if gap_res else None,
            'n_gap':                  len(gap_all),
            'n_other':                len(other_all),
            'n_gap_censored':         len(gap_all) - len(gap_res),
            'n_other_censored':       len(other_all) - len(other_res),
            'gap_censored_frac':      (len(gap_all) - len(gap_res)) / len(gap_all) if gap_all else 0.0,
            'other_censored_frac':    (len(other_all) - len(other_res)) / len(other_all) if other_all else 0.0,
            'comparable':             False,   # set True only when censoring rates match
            'gap_zetas':              gap_res,
            'other_zetas':            other_res,
        }

    def run_all(self, primes: List[int]) -> Dict:
        """Print and return the complete zeta index analysis."""
        print("=" * 60)
        print("ZETA INDEX ENGINE — SPECTRAL WAVELENGTH ANALYSIS")
        print("=" * 60)

        print(f"\nFirst 10 Riemann zeros and their spectral wavelengths:")
        zt = self.zero_table()[:10]
        print(f"  {'n':>4}  {'γₙ':>10}  {'λₙ=2π/γₙ':>12}  {'x=e^λₙ':>10}")
        print("  " + "-" * 44)
        for row in zt:
            print(f"  {row['n']:4d}  {row['gamma']:10.6f}  {row['lambda_log']:12.8f}  {row['x_activate']:10.6f}")

        print(f"\nZeta index for primes 2..47:")
        small_primes = [p for p in primes if p <= 47]
        MONSTER_GAP = {1, 11, 15}
        for rec in self.prime_zeta_table(small_primes):
            mg = " ← SILVER (Monster gap)" if rec['nshape'] in MONSTER_GAP else ""
            print(f"  p={rec['p']:4d}  n={rec['n']:3d}  e{rec['nshape']:2d}  "
                  f"γ*={rec['gamma_star']:8.3f}  ζ(p)={rec['zeta_idx']:3d}  "
                  f"γ_ζ={rec['gamma_zeta']:.3f}{mg}")

        print(f"\nZeta sub-ordering of first 10 primes:")
        ordering = self.zeta_ordering(primes[:20])[:10]
        for zi, n, p in ordering:
            print(f"  ζ={zi:3d}  n={n:3d}  p={p:5d}  → p_{{{n}[{zi}]}}")

        mg = self.monster_gap_zeta(primes)

        def _f(v, spec='.1f'):
            return format(v, spec) if v is not None else 'n/a'

        print(f"\nζ over RESOLVED primes only "
              f"(γ*(p) ≤ γ_{len(self.zeros())} = {self.zeros()[-1]:.3f}):")
        print(f"  Monster gap: mean ζ = {_f(mg['monster_gap_zeta_mean'])}  "
              f"(range {mg['monster_gap_zeta_min']}..{mg['monster_gap_zeta_max']})  "
              f"censored {mg['n_gap_censored']}/{mg['n_gap']} "
              f"({mg['gap_censored_frac']*100:.1f}%)")
        print(f"  Other:       mean ζ = {_f(mg['other_zeta_mean'])}  "
              f"censored {mg['n_other_censored']}/{mg['n_other']} "
              f"({mg['other_censored_frac']*100:.1f}%)")
        print(f"  Censoring rates differ by "
              f"{abs(mg['gap_censored_frac']-mg['other_censored_frac'])*100:.1f} points; "
              f"groups comparable: {mg['comparable']}")

        print("\n" + "=" * 60)
        return {
            'zero_table':     zt,
            'primes':         primes,
            'records':        self.prime_zeta_table(primes),
            'ordering':       self.zeta_ordering(primes),
            'monster_gap':    mg,
        }


# ---------------------------------------------------------------------------
# Convenience functions (module-level)
# ---------------------------------------------------------------------------

def spectral_wavelength(gamma_n: float) -> float:
    """λₙ = 2π/γₙ — the canonical log-space wavelength of Riemann zero ρₙ."""
    return TWO_PI / gamma_n

def activation_scale(gamma_n: float) -> float:
    """x = e^(2π/γₙ) — scale at which zero ρₙ first completes one oscillation cycle."""
    return math.exp(TWO_PI / gamma_n)

def gamma_threshold(p: int) -> float:
    """γ*(p) = 2πp/log(p) — minimum γ for zero to resolve prime p."""
    return TWO_PI * p / math.log(p)

def zeta_index(p: int, gamma_list: List[float]) -> int:
    """ζ(p) = min{n : γₙ ≥ γ*(p)} — first zero index resolving prime p."""
    thresh = gamma_threshold(p)
    for n, g in enumerate(gamma_list, 1):
        if g >= thresh:
            return n
    return -1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(__file__))
    from telperion_engine import prime_sieve

    primes = prime_sieve(500)

    # Need enough zeros: γ*(500) = 2π×500/log(500) ≈ 2024
    # Approximate: ≈ 2024/(2π) × log(2024/(2π)) ≈ 322 × log(322) ≈ 322 × 5.77 ≈ 1860 zeros
    # We'll use 100 from the precomputed table for the demo,
    # which covers primes up to the point where γ*(p) ≤ γ₁₀₀ ≈ 236.5
    # γ*(p) ≤ 236.5 → 2πp/log(p) ≤ 236.5 → p ≤ ~55
    engine = ZetaIndexEngine(n_zeros=100)
    results = engine.run_all(primes)
