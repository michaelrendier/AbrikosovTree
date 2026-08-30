"""
two_trees.py — Telperion & Laurelin: the Abrikosov Tree as The Two Trees
======================================================================

The Abrikosov Tree was originally built off "the old Telperion" alone — the
prime-indexed paths that survive Fermat's Nightmare.  That is only half the
domain.  The Two Trees are the COMPLETE domain of the integers, partitioned
exactly, with no remainder (Ainulindale/wiki/47):

    TELPERION   B_p   BLUE    Fermat–Weierstrass   what CANNOT BE    backward, entropic
    LAURELIN    R_p   RED     Berry–Keating  x·p   what IS           forward, inertial
    MINGLING            —     J_Red = J_Blue       σ = ½             the critical line

Applied to ℕ, the partition is factorisation itself:

    TELPERION   PRIME       defined by what it cannot be decomposed into
    LAURELIN    COMPOSITE   defined by what it IS decomposed into
    MINGLING    0 and 1     neither prime nor composite — the hour the trees balance

Measured over [0, 100000]:  2 + 9592 + 90407 = 100001 = every integer,
zero overlap.  The partition is EXACT.

The two trees COUNTER-ROTATE.  Prime density B(n) and composite density R(n)
sum to 1 at every scale (the unit pair {0,1} carries the slack M(n) = 2/(n+1)):

    B(n) + R(n) + M(n) = 1        exactly, for every n          ← J_Red + J_Blue conserved

The Mingling — equal brightness, B(n) = R(n) — is not a point but THREE
crossings, measured at n = 9, 11, 13 (near e² = 7.389).  After n = 13
Laurelin dominates forever: composites outnumber primes at every larger scale.

Through the Cayley–Dickson tower the two trees wind opposite ways.  Telperion
twists +Θ(k), Laurelin twists −Θ(k), with Θ(k) = k · THE_ANGLE (22.5° = π/8,
the angular quantum of the first zero-divisor level).  At ℍ (k=2, σ=½) the two
carry equal weight — the Abrikosov pinning level, where the Noether current
J = −∂L/∂σ is balanced.  At 𝕊 (k=4, σ=0, dim 16 — the Emmy Noether Sedenion)
that balance is first OBSTRUCTED: norm-multiplicativity |ab| = |a||b| — the
composition symmetry whose conserved current is J — fails for the first time
(Hurwitz 1898).  Its failure locus is a space homeomorphic to G₂ = Aut(𝕆)
(Moreno 1998): 7 box-kites, 42 assessors, indexed by the 7 Fano lines.  This
is where Laurelin's leaves fall — a composite n = a·b becomes a zero-divisor
pair — and where the octonions are "born to a quadratic ±".  Telperion passes
straight through: a prime has no factorisation, so no zero-divisor pair forms.

No free parameters.  No renormalisation.  Failed predictions stay in data.

Version: 0.300 — 2026-08-30 — Two Trees framing (was: old-Telperion-only)
"""

import os
import sys
import math
import json
from typing import Dict, List, Tuple, Optional

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

# fixed_point only needs math + numpy — safe to import without FermatMonster.
from fixed_point import OMEGA_ZS, D_STAR, GAP, SIGMA_HALF  # noqa: F401

# ── The Two Trees — identity constants ────────────────────────────────────────

THE_ANGLE = 22.5           # degrees = π/8 = 2π/16, angular quantum of 𝕊 (dim 16)
E_SQUARED = math.e ** 2    # 7.389… — the Mingling sits near here

TELPERION = {
    'name':     'Telperion',
    'colour':   'BLUE',
    'hex':      '#6f9cff',
    'symbol':   'B_p',
    'domain':   'prime',
    'defined_by': 'what it CANNOT be decomposed into',
    'character': 'what CANNOT BE',
    'arrow':    'backward, entropic',
    'operator': 'Fermat–Weierstrass',
    'winding':  +1,          # counter-rotation sense through the CD tower
}

LAURELIN = {
    'name':     'Laurelin',
    'colour':   'RED',
    'hex':      '#ff5a3c',
    'symbol':   'R_p',
    'domain':   'composite',
    'defined_by': 'what it IS decomposed into',
    'character': 'what IS',
    'arrow':    'forward, inertial',
    'operator': 'Berry–Keating x·p',
    'winding':  -1,
}

MINGLING = {
    'name':     'Mingling',
    'colour':   'GOLD',
    'hex':      '#ffcf3f',
    'members':  (0, 1),
    'condition': 'J_Red = J_Blue',
    'sigma':    0.5,
    'note':     'neither prime nor composite; the identities of ADD (0) and SCALE (1)',
}

# CD tower — same σ law as the rest of the engine: σ(k) = 1 − k/4
CD_NAMES = {0: 'ℝ', 1: 'ℂ', 2: 'ℍ', 3: '𝕆', 4: '𝕊',
            5: 't_32', 6: 't_64', 7: 't_128', 8: 'T_256'}
CD_LABELS = {0: 'Real Numbers', 1: 'Complex', 2: 'Quaternion',
             3: 'Octonion', 4: 'Emmy Noether Sedenion',
             5: 't_32', 6: 't_64', 7: 't_128', 8: 'T_256'}
N_LEVELS       = 9
FIRST_ZD_LEVEL = 4        # 𝕊: |ab| = |a||b| fails; Laurelin's leaves fall
MINGLING_LEVEL = 2        # ℍ: σ = ½, Noether current balanced

# The 7 Fano lines (standard octonion labelling) — index the 7 box-kites of 𝕊.
FANO_LINES = [(1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 7),
              (5, 6, 1), (6, 7, 2), (7, 1, 3)]


# ── 1. The partition ─────────────────────────────────────────────────────────

def prime_sieve(N: int) -> List[int]:
    if N < 2:
        return []
    s = bytearray([1]) * (N + 1)
    s[0] = s[1] = 0
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return [i for i, v in enumerate(s) if v]


def classify_tree(n: int) -> str:
    """Which tree does the integer n belong to?  Exactly one, always."""
    if n in (0, 1):
        return 'mingling'
    for f in range(2, int(n ** 0.5) + 1):
        if n % f == 0:
            return 'laurelin'
    return 'telperion'


def tree_densities(N: int) -> Dict:
    """
    B(n), R(n), M(n) for every n in 0..N, with the conservation law checked.

        B(n) = π(n) / (n+1)            Telperion  (prime density)
        R(n) = composites(n) / (n+1)   Laurelin   (composite density)
        M(n) = 2 / (n+1)               Mingling   ({0,1})
        B + R + M = 1                  exactly

    Also returns the running prime-minus-composite count, whose zero crossings
    are the Mingling.
    """
    primes = set(prime_sieve(N))
    ns, B, R, M, diff = [], [], [], [], []
    pc = cc = 0
    for n in range(N + 1):
        if n >= 2:
            if n in primes:
                pc += 1
            else:
                cc += 1
        mc = (1 if n >= 0 else 0) + (1 if n >= 1 else 0)   # {0,1} seen so far
        ns.append(n)
        B.append(pc / (n + 1))
        R.append(cc / (n + 1))
        M.append(mc / (n + 1))
        diff.append(pc - cc)
        # conservation — exact to floating point
        assert abs(B[-1] + R[-1] + M[-1] - 1.0) < 1e-12, n
    return {
        'N': N, 'n': ns, 'B': B, 'R': R, 'M': M, 'prime_minus_composite': diff,
        'n_primes': pc, 'n_composites': cc,
        'conservation': 'B(n) + R(n) + M(n) = 1  verified for all n ≤ %d' % N,
    }


def mingling_crossings(N: int = 2000) -> List[int]:
    """
    The n where the running prime count equals the running composite count.
    Measured: [9, 11, 13].  After the last one Laurelin dominates forever.
    """
    d = tree_densities(N)['prime_minus_composite']
    out = []
    for n in range(3, N):
        if d[n] == 0 or (d[n - 1] > 0 >= d[n]) or (d[n - 1] < 0 <= d[n]):
            if d[n] == 0:
                out.append(n)
    return out


# ── 2. Counter-rotation through the CD tower ─────────────────────────────────

def twist(k: int) -> float:
    """Cumulative twist magnitude at CD level k, in degrees:  Θ(k) = k · 22.5°."""
    return k * THE_ANGLE


def counter_rotation(k: int) -> Dict:
    """
    The signed twist of each tree at level k.  Telperion +Θ(k), Laurelin −Θ(k):
    the two trees wind opposite ways.  Their angular separation is 2Θ(k).
    """
    th = twist(k)
    return {
        'k': k, 'name': CD_NAMES[k],
        'theta': th,
        'telperion_deg': +th * TELPERION['winding'],
        'laurelin_deg':  +th * LAURELIN['winding'],
        'separation_deg': 2 * th,
    }


def cd_tower() -> List[Dict]:
    """
    The 9-level tower, annotated for both trees.

        σ(k) = 1 − k/4
        ℍ  (k=2, σ=½) — MINGLING level: J_Red = J_Blue, Noether current balanced,
                         Abrikosov pinning.
        𝕊  (k=4, σ=0) — the Emmy Noether Sedenion: |ab| = |a||b| fails here for
                         the first time (Hurwitz 1898).  Laurelin's leaves fall;
                         Telperion passes through.
    """
    tower = []
    for k in range(N_LEVELS):
        sigma = 1.0 - k / 4.0
        dim = 2 ** k
        cr = counter_rotation(k)
        tower.append({
            'k': k,
            'name': CD_NAMES[k],
            'label': CD_LABELS[k],
            'sigma': sigma,
            'dim': dim,
            'angular_quantum_deg': (360.0 / dim) if dim >= 2 else 0.0,
            'twist_deg': cr['theta'],
            'telperion_twist_deg': cr['telperion_deg'],
            'laurelin_twist_deg': cr['laurelin_deg'],
            'is_mingling_level': k == MINGLING_LEVEL,
            'is_zd_level': k >= FIRST_ZD_LEVEL,
            'laurelin_falls': k == FIRST_ZD_LEVEL,
            'n_fano': (2 ** (k - 3)) if k >= 3 else 0,
            'note': (
                'MINGLING — J_Red = J_Blue, Noether current J = −∂L/∂σ balanced, Abrikosov pinning'
                if k == MINGLING_LEVEL else
                'EQUATOR — first zero-divisors; |ab|=|a||b| fails; ZD(𝕊) ≅ G₂; Laurelin falls'
                if k == FIRST_ZD_LEVEL else
                'normed division algebra — |ab| = |a||b| holds (Hurwitz 1898)'
                if k <= 3 else
                'post-sedenion — %d Fano planes' % (2 ** (k - 3))
            ),
        })
    return tower


# ── 3. The G₂ family split at the 𝕆 → 𝕊 boundary ────────────────────────────

def g2_family_split() -> Dict:
    """
    The unit-norm zero-divisors of 𝕊 form a space homeomorphic to G₂ = Aut(𝕆)
    (Moreno 1998).  Combinatorially (de Marrais): 7 box-kites, 6 assessors each,
    42 total, indexed by the 7 Fano lines.  This is where a composite n = a·b
    first resolves into a zero-divisor pair — where the octonions are "born to a
    quadratic ±" — and where norm-multiplicativity (the composition symmetry
    whose Noether current is J) is first obstructed.

    G₂ root system for the overlay: rank 2, 12 roots — 6 long + 6 short.
    """
    # G₂ roots: 6 short at 30° steps (radius 1), 6 long at 30° steps offset 30° (radius √3)
    short = [(math.cos(math.radians(a)), math.sin(math.radians(a)))
             for a in range(0, 360, 60)]
    long_ = [(math.sqrt(3) * math.cos(math.radians(a + 30)),
              math.sqrt(3) * math.sin(math.radians(a + 30)))
             for a in range(0, 360, 60)]
    box_kites = []
    for i, line in enumerate(FANO_LINES):
        box_kites.append({
            'index': i,
            'fano_line': line,
            'assessors': 6,
            'sail_angle_deg': i * 360.0 / 7.0,
        })
    return {
        'algebra': 'G₂ = Aut(𝕆), dim 14, rank 2',
        'citation': 'Moreno (1998); box-kite combinatorics de Marrais (2000–2008)',
        'n_box_kites': 7,
        'n_assessors': 42,
        'box_kites': box_kites,
        'g2_roots_short': short,
        'g2_roots_long': long_,
    }


# ── 4. Per-plane lattice points (for rendering) ─────────────────────────────

def lattice_in_plane(k: int, N: int = 240, spiral_turns: float = 3.0) -> Dict:
    """
    The lattice tree as it sits in CD plane k.  Every integer 2..N is placed by
    its tree:

        radius  = log(n)                        (logarithmic — Fourier-dual to the zeros)
        angle   = winding · (base_angle(n) + Θ(k))

    where base_angle(n) spirals the leaves out (spiral_turns over the range) and
    Θ(k) = k·22.5° is the CD-level twist.  Telperion winds +, Laurelin winds −:
    the two clouds counter-rotate as k increases.

    brightness = the tree's density weight at that scale (B(n) or R(n)),
    normalised so the Mingling levels read as equal brightness.
    """
    primes = set(prime_sieve(N))
    th_k = math.radians(twist(k))
    dens = tree_densities(N)
    span = math.log(N) - math.log(2)

    tel, lau, ming = [], [], []
    pc = cc = 0
    for n in range(2, N + 1):
        lp = math.log(n)
        frac = (lp - math.log(2)) / span
        base = frac * spiral_turns * 2 * math.pi
        r = lp
        if n in primes:
            pc += 1
            ang = TELPERION['winding'] * (base + th_k)
            tel.append({'n': n, 'x': r * math.cos(ang), 'y': r * math.sin(ang),
                        'r': r, 'ang': ang, 'w': dens['B'][n],
                        'silver': (n % 16) in (1, 11, 15)})
        else:
            cc += 1
            ang = LAURELIN['winding'] * (base + th_k)
            fell = (k >= FIRST_ZD_LEVEL)
            lau.append({'n': n, 'x': r * math.cos(ang), 'y': r * math.sin(ang),
                        'r': r, 'ang': ang, 'w': dens['R'][n], 'fell': fell})
    for m in (0, 1):
        ming.append({'n': m, 'x': 0.0, 'y': 0.0, 'r': 0.0})

    return {
        'k': k, 'name': CD_NAMES[k], 'label': CD_LABELS[k],
        'sigma': 1.0 - k / 4.0,
        'twist_deg': twist(k),
        'telperion': tel, 'laurelin': lau, 'mingling': ming,
        'is_mingling_level': k == MINGLING_LEVEL,
        'is_zd_level': k >= FIRST_ZD_LEVEL,
    }


# ── 5. Riemann zeros — the Abrikosov vortices, unchanged from the old tree ───

RIEMANN_GAMMA = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
]


def zero_unfold(gamma: float) -> float:
    """Riemann–von Mangoldt unfolding: wₙ = (γ/2π)·ln(γ/2π) − γ/2π."""
    x = gamma / (2 * math.pi)
    return x * math.log(x) - x


# ── 6. Dataset + JSON export ───────────────────────────────────────────────

def two_trees_data(N: int = 1000) -> Dict:
    d = tree_densities(N)
    return {
        'N': N,
        'telperion': TELPERION,
        'laurelin': LAURELIN,
        'mingling': MINGLING,
        'n_primes': d['n_primes'],
        'n_composites': d['n_composites'],
        'n_mingling': 2,
        'partition_check': '%d + %d + 2 = %d = N+1'
                           % (d['n_primes'], d['n_composites'], N + 1),
        'conservation': d['conservation'],
        'mingling_crossings': mingling_crossings(max(N, 2000)),
        'cd_tower': cd_tower(),
        'g2_split': g2_family_split(),
        'riemann_gamma': RIEMANN_GAMMA,
        'constants': {'OMEGA_ZS': OMEGA_ZS, 'D_STAR': D_STAR, 'GAP': GAP,
                      'THE_ANGLE': THE_ANGLE, 'E_SQUARED': E_SQUARED},
    }


def export_json(N: int = 1000, path: Optional[str] = None) -> str:
    if path is None:
        path = os.path.join(_HERE, 'two_trees_data.json')
    with open(path, 'w') as f:
        json.dump(two_trees_data(N), f, indent=2)
    return path


# ── Runner ────────────────────────────────────────────────────────────────

def run_all(N: int = 1000) -> Dict:
    print("=" * 68)
    print("THE TWO TREES  —  Telperion (prime) ⟂ Laurelin (composite)")
    print("=" * 68)
    data = two_trees_data(N)
    print(f"\n  Partition over [0, {N}]:  {data['partition_check']}")
    print(f"  Conservation:            {data['conservation']}")
    print(f"  Mingling crossings B(n) = R(n):  n = {data['mingling_crossings']}"
          f"   (near e² = {E_SQUARED:.3f})")
    print(f"  After the last crossing, Laurelin dominates at every larger scale.")

    print("\n  Counter-rotation through the Cayley–Dickson tower:")
    print(f"    {'k':>2}  {'plane':<22} {'σ':>6}  {'dim':>4}  "
          f"{'Telperion':>10}  {'Laurelin':>10}  note")
    for lv in data['cd_tower'][:5]:
        print(f"    {lv['k']:>2}  {lv['name']+' — '+lv['label']:<22} "
              f"{lv['sigma']:>6.3f}  {lv['dim']:>4}  "
              f"{lv['telperion_twist_deg']:>+9.1f}°  {lv['laurelin_twist_deg']:>+9.1f}°  "
              f"{lv['note'][:44]}")

    g2 = data['g2_split']
    print(f"\n  𝕊 (Emmy Noether Sedenion) — the G₂ family split:")
    print(f"    {g2['algebra']}")
    print(f"    {g2['n_box_kites']} box-kites · {g2['n_assessors']} assessors · "
          f"indexed by the 7 Fano lines")
    print(f"    {g2['citation']}")

    path = export_json(N)
    print(f"\n  Written: {path}")
    print("=" * 68)
    print("  Telperion passes through 𝕊 intact.  Laurelin's leaves fall there.")
    print("=" * 68)
    return data


if __name__ == '__main__':
    run_all(N=1000)
