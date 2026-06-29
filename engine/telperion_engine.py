"""
Telperion — The Un-Extinctable Bulk

The Zero Tree IS Telperion.  The primes are its leaves.
Fermat's Nightmare (FLT via ZD cascade) shakes every composite loose.
What remains — the prime-indexed paths from ℝ (k=0) through nine CD levels
to T_256 (k=8) — is this tree.  It cannot be extinguished.

The N-shape theorem (proved in FermatMonster engine v0.300):
    The Generalized N-Shape Fermat Equation IS the Monster Group + 70 siblings.
    71 holomorphic c=24 VOAs = 71 N-shapes = complete Fermat forbidden zone.
    Niemeier root systems cover 13 N-shapes (h mod 16).
    Monster fills the gap: {e₁, e₁₁, e₁₅} — algebraically unreachable by A/D/E.

Primes map to N-shapes via p mod 16.
Monster gap primes (p ≡ 1,11,15 mod 16) are Telperion's silver leaves:
    the leaves that not even regular algebraic structure can describe.

Fractal boundary:
    The prime distribution itself has fractal character.
    Oscillations in π(x; 16, k) are driven by zeros of Dirichlet L-functions L(s,χ).
    These zeros ARE the spectral nodes of the Zero Tree.
    The fractal boundary at each CD level is the density envelope
    of surviving prime paths — a standing wave on the critical line.

Three coordinate spaces for rendering:
    A — Spherical Sedenion Space (existing zero_tree_tower.py)
    B — Consecutive Euclidean Planes   (zero_tree_planes.py)
    C — Fano Tower / 32 heptagons      (zero_tree_fano.py)

Imports:
    fixed_point.py           — two fixed points, angular quanta, V(n), GAP
    fermat_monster_engine.py — N-shape map, ZD pairs, 71-VOA coverage

No free parameters.  No renormalization.  Failed predictions stay in data.

Version: 0.100 — 2026-06-29
"""

import sys
import os
import math
import json
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field, asdict

# ── Sibling engine imports ─────────────────────────────────────────────────────

_HERE        = os.path.dirname(os.path.abspath(__file__))
_FERMAT_DIR  = os.path.join(
    os.path.dirname(os.path.dirname(_HERE)),  # FourthAgePapers/
    'FermatMonster', 'engine'
)
sys.path.insert(0, _HERE)
sys.path.insert(0, _FERMAT_DIR)

from fixed_point import (
    v_nball, two_fixed_points, angular_quantum_sequence,
    OMEGA_ZS, D_STAR, GAP, SIGMA_HALF,
)
from fermat_monster_engine import (
    fermat_n_shape_map, cd_tower_check, fermat_niemeier_bridge,
    sed_mul, sedenion_unit,
    ZD_CONSTELLATIONS_ODD, MOONSHINE_PRIMES, PRIME_SECTOR,
)

# ── Constants ──────────────────────────────────────────────────────────────────

NIEMEIER_GAP      = frozenset({1, 11, 15})    # Monster gap: A/D/E cannot reach these
LEECH_SHAPE       = 0                          # Leech lattice: no roots, identity shape
N_LEVELS          = 9                          # k = 0..8  (ℝ → T_256)
FIRST_ZD_LEVEL    = 4                          # k=4 (𝕊): first ZD crossing
MOONSHINE_SET     = frozenset(MOONSHINE_PRIMES)

CD_NAMES = {
    0: 'ℝ', 1: 'ℂ', 2: 'ℍ', 3: '𝕆', 4: '𝕊',
    5: 't_32', 6: 't_64', 7: 't_128', 8: 'T_256',
}

# Angular base (degrees) for each level — from zero_tree_tower.py
LEVEL_BASE_DEG = {
    0: 0.0,                 # ℝ: real point, no quadrant distinction
    1: 0.0,   # J_red
    2: 45.0,  # J_blue
    3: 0.0,   # J_red
    4: 45.0,  # J_blue
    5: 0.0,   # J_red
    6: 45.0,  # J_blue
    7: 0.0,   # J_red
    8: 45.0,  # J_blue
}

# THE ANGLE: rotates J_red +22.5°, J_blue −22.5° — straightens prime paths into radial spokes
THE_ANGLE = 22.5  # degrees


# ── 1. Prime sieve ─────────────────────────────────────────────────────────────

def prime_sieve(N: int) -> List[int]:
    """
    Sieve of Eratosthenes.  Returns all primes p with 2 ≤ p ≤ N.

    These are the leaves of Telperion.  Every prime is a leaf.
    No leaf can fall: primes have no non-trivial factorization,
    so they cannot be expressed as ZD products at any CD level.
    """
    if N < 2:
        return []
    sieve = bytearray([1]) * (N + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(N**0.5) + 1):
        if sieve[i]:
            sieve[i * i :: i] = bytearray(len(sieve[i * i :: i]))
    return [i for i, v in enumerate(sieve) if v]


# ── 2. N-shape classification ──────────────────────────────────────────────────

def prime_nshape(p: int) -> int:
    """
    N-shape of prime p: p mod 16.

    Maps p to the sedenion basis element e_k that p 'activates'.
    This is the address of the prime leaf in the sedenion tower.
    """
    return p % 16


def classify_prime(p: int) -> Dict:
    """
    Full classification of prime p by N-shape and VOA source.

    Returns:
        nshape         — p mod 16 (sedenion index)
        classification — 'monster_gap' | 'niemeier' | 'leech_adjacent' | 'other_even'
        in_prime_sector— p mod 16 ∈ {1,3,5,7,9,11,13,15}
        is_moonshine   — p ∈ Moonshine prime list
        voa_source     — which class of VOA covers this N-shape
        fermat_survives— always True for primes (definitional)
    """
    ns = p % 16
    in_prime_sec = ns in PRIME_SECTOR
    is_moon      = p in MOONSHINE_SET

    if ns in NIEMEIER_GAP:
        cls      = 'monster_gap'
        voa_src  = 'Monster + siblings (47 non-lattice VOAs)'
    elif ns == LEECH_SHAPE:
        cls      = 'leech_adjacent'
        voa_src  = 'Leech lattice Λ₂₄ (lattice VOA, no roots)'
    elif ns in PRIME_SECTOR:
        cls      = 'niemeier_odd'
        voa_src  = 'Niemeier root system (odd h, A-type)'
    else:
        cls      = 'niemeier_even'
        voa_src  = 'Niemeier root system (even h, D/E-type or even A-type)'

    return {
        'p':              p,
        'nshape':         ns,
        'classification': cls,
        'in_prime_sector':in_prime_sec,
        'is_moonshine':   is_moon,
        'voa_source':     voa_src,
        'fermat_survives':True,    # primes never fall — definitional
    }


# ── 3. CD tower structure at each level ───────────────────────────────────────

def cd_level_data(k: int) -> Dict:
    """
    Structural data for CD level k.

    k=0  ℝ      σ=+1.00  theta=0°    leaf (The Unit)
    k=2  ℍ      σ=+0.50  theta=45°   gravastar shell / critical line
    k=4  𝕊      σ= 0.00  theta=90°   equator / first ZD / Fermat extinction threshold
    k=8  T_256  σ=−1.00  theta=180°  root / 32 Fano planes / all-boundary

    At k≥4: ZD pairs exist.  The sedenion norm |ab|=|a||b| fails.
    Composites reach k=4 and find their factors expressed as ZD pairs.
    They fall.  Primes have no factors.  They reach k=8.
    """
    sigma    = 1.0 - k / 4.0
    theta    = k * math.pi / 8.0
    dim      = 2 ** k
    n_fano   = 2 ** (k - 3) if k >= 3 else 0
    v_vol    = v_nball(float(dim))
    ang_q    = (2.0 * math.pi / dim) if dim >= 2 else 0.0

    is_red   = (k % 2 == 1) and k > 0
    is_blue  = (k % 2 == 0) and k > 0
    base_deg = LEVEL_BASE_DEG[k]

    return {
        'k':           k,
        'name':        CD_NAMES[k],
        'sigma':       sigma,
        'theta_rad':   theta,
        'theta_deg':   math.degrees(theta),
        'dim':         dim,
        'n_fano':      n_fano,
        'v_nball':     v_vol,
        'angular_q':   ang_q,
        'angular_q_deg': math.degrees(ang_q) if ang_q > 0 else 0.0,
        'is_zd':       k >= FIRST_ZD_LEVEL,
        'is_gravastar':k == 2,
        'is_leaf':     k == 0,
        'is_root':     k == 8,
        'j_type':      'J_red' if is_red else ('J_blue' if is_blue else 'real'),
        'base_deg':    base_deg,
    }


def full_tower() -> List[Dict]:
    """Complete CD tower: k=0..8."""
    return [cd_level_data(k) for k in range(N_LEVELS)]


# ── 4. Prime path through the tower ───────────────────────────────────────────

def prime_tower_path(p: int) -> Dict:
    """
    Trace prime p through all 9 CD levels.

    At each level k, p is mapped to a quadrant angle based on its N-shape.
    N-shape = p mod 16.  16 N-shapes, 4 quadrants per level → 4 N-shapes per quadrant.
    Quadrant assignment:
        q = (p mod 16) % 4   → which of the 4 quadrant spokes (0..3)

    Angular position at level k:
        phi = base_deg[k] + q * 90.0  (structural position)

    With THE ANGLE applied:
        J_red:  phi += 22.5°
        J_blue: phi -= 22.5°
    This rotates the n-sphere at each level so that the prime path
    becomes a radial spoke — a geodesic on the sphere.

    Returns per-level positions for all three coordinate spaces.
    """
    ns     = p % 16
    q      = ns % 4           # quadrant index (0..3)
    ns_sub = ns // 4          # sub-quadrant (0..3), governs fine fractal position

    levels = []
    for k in range(N_LEVELS):
        lv       = cd_level_data(k)
        base     = lv['base_deg']
        j_type   = lv['j_type']

        phi_base = base + q * 90.0
        # The angle: straighten the path into a geodesic spoke
        if j_type == 'J_red':
            phi_straight = phi_base + THE_ANGLE
        elif j_type == 'J_blue':
            phi_straight = phi_base - THE_ANGLE
        else:
            phi_straight = phi_base   # k=0: degenerate (north pole)

        R = 3.0  # sphere radius (matches zero_tree_tower.py)
        theta = lv['theta_rad']
        phi_r = math.radians(phi_straight)

        # Space A: sphere coordinates
        x_sph = R * math.sin(theta) * math.cos(phi_r)
        y_sph = R * math.sin(theta) * math.sin(phi_r)
        z_sph = R * math.cos(theta)

        # Space B: plane stack coordinates
        # z-height from σ: top = σ=+1 (k=0), bottom = σ=-1 (k=8)
        z_plane = lv['sigma'] * 4.0          # scale to [-4, +4]
        r_plane = 2.0 if k > 0 else 0.0     # radius of plane (0 at degenerate pole)
        x_plane = r_plane * math.cos(phi_r)
        y_plane = r_plane * math.sin(phi_r)

        # Space C: Fano plane index at this level
        fano_idx = (ns % lv['n_fano']) if lv['n_fano'] > 0 else 0

        levels.append({
            'k':          k,
            'name':       lv['name'],
            'sigma':      lv['sigma'],
            'is_zd':      lv['is_zd'],
            'quadrant':   q,
            'ns_sub':     ns_sub,
            'phi_deg':    phi_straight,
            # Space A
            'sph': {'x': x_sph, 'y': y_sph, 'z': z_sph},
            # Space B
            'plane': {'x': x_plane, 'y': y_plane, 'z': z_plane},
            # Space C
            'fano_idx': fano_idx,
        })

    cls = classify_prime(p)
    return {
        'p':              p,
        'nshape':         ns,
        'quadrant':       q,
        'classification': cls['classification'],
        'is_moonshine':   cls['is_moonshine'],
        'levels':         levels,
    }


# ── 5. Fermat survival data ────────────────────────────────────────────────────

def fermat_survival_table(N: int) -> Dict:
    """
    For every integer n, 2 ≤ n ≤ N:
        primes:     fermat_survives = True  (by definition — no factorization)
        composites: fermat_survives = False (fall at k=FIRST_ZD_LEVEL=4)

    Also records the 'fall N-shape': the sedenion index where the composite falls.
    For a composite n = a × b (smallest non-trivial factorization):
        fall N-shape = n mod 16  (same logic as prime N-shape)
        The composite falls at the ZD crossing node closest to its N-shape.

    The boundary between survivors (primes) and fallen (composites)
    at each CD level is the Fermat survival frontier.
    """
    primes = set(prime_sieve(N))
    table  = {}

    for n in range(2, N + 1):
        is_prime = n in primes
        ns       = n % 16

        if is_prime:
            entry = {
                'n':              n,
                'is_prime':       True,
                'fermat_survives':True,
                'fall_level':     None,
                'fall_nshape':    None,
                'smallest_factor':None,
            }
        else:
            # Find smallest non-trivial factor
            sf = None
            for f in range(2, int(n**0.5) + 1):
                if n % f == 0:
                    sf = f
                    break

            entry = {
                'n':              n,
                'is_prime':       False,
                'fermat_survives':False,
                'fall_level':     FIRST_ZD_LEVEL,   # k=4: first ZD
                'fall_nshape':    ns,
                'smallest_factor':sf,
            }

        table[n] = entry

    # Boundary statistics at each level k
    level_stats = {}
    for k in range(N_LEVELS):
        if k < FIRST_ZD_LEVEL:
            # No ZD here — all survive
            surviving = [n for n in range(2, N + 1)]
        else:
            surviving = [n for n in primes if n <= N]
        fallen    = [n for n in range(2, N + 1) if n not in primes and n <= N]

        ns_survival = {}
        for ns in range(16):
            p_count = sum(1 for p in primes if p <= N and p % 16 == ns)
            ns_survival[ns] = p_count

        level_stats[k] = {
            'k':                k,
            'is_zd':            k >= FIRST_ZD_LEVEL,
            'n_surviving':      len(surviving),
            'n_fallen':         len(fallen) if k >= FIRST_ZD_LEVEL else 0,
            'survival_by_nshape': ns_survival,
        }

    return {
        'N':           N,
        'n_primes':    len(primes),
        'n_composites':N - 1 - len(primes),
        'table':       table,
        'level_stats': level_stats,
    }


# ── 6. Fractal boundary ────────────────────────────────────────────────────────

def prime_gap_fractal(primes: List[int]) -> Dict:
    """
    Prime gap distribution: gaps[i] = primes[i+1] - primes[i].

    The gap distribution has fractal-like structure:
        - Mean gap ~ log(p) by the prime number theorem
        - Oscillations around the mean driven by Riemann zeros
        - The same zeros that are the 'lens' of the Zero Tree (wiki #72)

    Returns:
        gaps           — raw gap sequence
        gap_by_nshape  — gaps grouped by N-shape of the smaller prime
        mean_gap       — overall mean
        gap_envelope   — running mean (fractal envelope at each index)
        self_similar_ratio — log(max_gap)/log(min_gap) > 1 signals fractal character
    """
    if len(primes) < 2:
        return {}

    gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]

    gap_by_nshape: Dict[int, List[int]] = {ns: [] for ns in range(16)}
    for i, p in enumerate(primes[:-1]):
        gap_by_nshape[p % 16].append(gaps[i])

    mean_gap      = sum(gaps) / len(gaps)
    max_gap       = max(gaps)
    min_gap       = min(gaps)
    running_mean  = []
    acc = 0.0
    for i, g in enumerate(gaps):
        acc += g
        running_mean.append(acc / (i + 1))

    # Self-similarity ratio: measures fractal character of gap distribution
    # A uniform distribution gives ratio ~ 1; fractal gives > 1
    if min_gap > 0:
        self_sim = math.log(max_gap) / math.log(min_gap) if min_gap > 1 else math.log(max_gap + 1)
    else:
        self_sim = float('inf')

    nshape_stats = {}
    for ns, gs in gap_by_nshape.items():
        if gs:
            nshape_stats[ns] = {
                'count':  len(gs),
                'mean':   sum(gs) / len(gs),
                'max':    max(gs),
                'min':    min(gs),
            }

    return {
        'n_gaps':            len(gaps),
        'gaps':              gaps,
        'mean_gap':          mean_gap,
        'max_gap':           max_gap,
        'min_gap':           min_gap,
        'running_mean':      running_mean,
        'self_similar_ratio':self_sim,
        'gap_by_nshape':     gap_by_nshape,
        'nshape_gap_stats':  nshape_stats,
    }


def fractal_boundary_data(primes: List[int], N_levels: int = 9) -> Dict:
    """
    The fractal boundary of Telperion.

    At each CD level k, the 'boundary' between surviving primes and fallen
    composites is a density contour in (angle, radius) space.

    Specifically, at level k:
        For each N-shape ns ∈ 0..15:
            density[k][ns] = number of primes with p % 16 == ns, p ≤ max_prime

    The boundary contour at level k is the set of (angle, density) pairs.
    It is fractal because:
        - Dirichlet: π(x; 16, ns) ~ li(x)/φ(16) asymptotically (equal density)
        - But oscillations driven by L-function zeros create local imbalance
        - These oscillations are self-similar at different scales
        - The envelope of the oscillations traces a fractal curve

    Each level k scales the boundary:
        Below k=4: all integers survive (boundary = full circle)
        At k=4:    composites fall — boundary becomes the prime density contour
        Above k=4: primes continue; boundary shape is frozen but rescaled by V(n)

    Angular position of each N-shape (for plotting):
        phi[ns] = ns * (360/16) = ns * 22.5°
    """
    ns_count = {ns: 0 for ns in range(16)}
    for p in primes:
        ns_count[p % 16] += 1

    total = len(primes)
    ns_phi    = {ns: ns * 22.5 for ns in range(16)}
    ns_density = {ns: ns_count[ns] / total if total > 0 else 0.0 for ns in range(16)}

    # Cumulative prime count per N-shape (for fractal envelope)
    cumulative = {ns: [] for ns in range(16)}
    running    = {ns: 0 for ns in range(16)}
    for p in sorted(primes):
        ns = p % 16
        running[ns] += 1
        for n2 in range(16):
            cumulative[n2].append(running[n2])

    # Boundary profile at each level
    level_boundary = {}
    for k in range(N_levels):
        lv = cd_level_data(k)
        # Volume factor: V(dim) modulates the boundary radius at each level
        v_factor = v_nball(float(lv['dim']))
        level_boundary[k] = {
            'k':         k,
            'name':      lv['name'],
            'sigma':     lv['sigma'],
            'v_factor':  v_factor,
            'is_zd':     lv['is_zd'],
            # At ZD levels: only prime-paths survive → boundary = prime density contour
            # Below ZD: all paths survive → boundary = full circle (v_factor radius)
            'boundary_type':  'prime_density' if lv['is_zd'] else 'full_circle',
            'nshape_density': {
                ns: {
                    'phi_deg':    ns_phi[ns],
                    'count':      ns_count[ns],
                    'density':    ns_density[ns],
                    'radius':     v_factor * ns_density[ns] * 16,  # normalized radius
                    'is_gap':     ns in NIEMEIER_GAP,
                    'is_leech':   ns == LEECH_SHAPE,
                }
                for ns in range(16)
            },
        }

    # Monster gap dominance: in the prime sector, gap elements have equal density
    # (Dirichlet) but their V-function path is uniquely un-reachable by Niemeier
    gap_density    = sum(ns_density[ns] for ns in NIEMEIER_GAP)
    niemeier_density = sum(ns_density[ns] for ns in range(16) if ns not in NIEMEIER_GAP and ns != 0)

    return {
        'n_primes':          total,
        'ns_count':          ns_count,
        'ns_phi':            ns_phi,
        'ns_density':        ns_density,
        'level_boundary':    level_boundary,
        'gap_density_frac':  gap_density,
        'niemeier_density_frac': niemeier_density,
        'dirichlet_expected': 1.0 / 16,  # asymptotic density per N-shape (≠ 0, i.e., φ(16)=8 coprime)
        'note': (
            'Dirichlet: for gcd(ns,16)=1 (the 8 odd N-shapes), '
            'density → 1/8 asymptotically.  For gcd(ns,16)>1 (even N-shapes), '
            'density → 0 (only finitely many primes ≤ 2,4,... except p=2). '
            'The actual density at finite N deviates from the asymptote — these '
            'deviations are the fractal oscillations driven by L-function zeros.'
        ),
    }


def prime_density_at_level(primes: List[int], k: int) -> Dict:
    """
    Prime path density at CD level k, organized by N-shape.

    Used to drive the fractal point clouds in the Blender renders.
    Returns one entry per N-shape: count, angular position, fractal radius.

    The fractal radius for N-shape ns at level k:
        r(ns, k) = (ns_count[ns] / max_count) ^ (1 / log2(k+2)) × R_base

    The exponent 1/log2(k+2) creates self-similar scaling: at high k,
    differences in density are amplified; at low k, they are smoothed.
    This is the fractal structure of the boundary across levels.
    """
    ns_count = {ns: 0 for ns in range(16)}
    for p in primes:
        ns_count[p % 16] += 1

    max_count = max(ns_count.values()) or 1
    R_base    = 2.5   # Blender units
    exponent  = 1.0 / math.log2(k + 2)

    result = {}
    for ns in range(16):
        c = ns_count[ns]
        r = (c / max_count) ** exponent * R_base if max_count > 0 else 0.0
        result[ns] = {
            'ns':         ns,
            'count':      c,
            'phi_deg':    ns * 22.5,
            'density':    c / len(primes) if primes else 0.0,
            'radius':     r,
            'is_gap':     ns in NIEMEIER_GAP,
            'is_leech':   ns == LEECH_SHAPE,
        }
    return result


# ── 7. Fano plane data for Space C ─────────────────────────────────────────────

def fano_plane_data() -> Dict:
    """
    The Fano plane F₇: 7 points, 7 lines (each line has 3 points).

    The octonion multiplication table IS the Fano plane.
    Points: e₁..e₇ (the 7 imaginary units of 𝕆).
    Lines: the 7 triples {i,j,k} such that eᵢeⱼ = eₖ (cyclic).

    Standard labelling (ISO convention):
        Lines: {1,2,4},{2,3,5},{3,4,6},{4,5,7},{5,6,1},{6,7,2},{7,1,3}
        (Each line is a triple closed under cyclic octonion multiplication.)

    The 7 vertices of the heptagon = the 7 imaginary units.
    The 7 lines of the Fano plane = 7 edges of the 'inner star' (not the heptagon boundary).
    Total: 7 boundary edges (heptagon) + 7 inner edges (Fano lines) = 14 edges per plane.

    At CD level k ≥ 3: n_fano(k) = 2^(k-3) embedded Fano planes.
    """
    # The 7 Fano lines (standard octonion labelling, 1-indexed)
    fano_lines = [
        (1, 2, 4),
        (2, 3, 5),
        (3, 4, 6),
        (4, 5, 7),
        (5, 6, 1),
        (6, 7, 2),
        (7, 1, 3),
    ]

    # Vertex positions on a regular heptagon (unit circle, offset so vertex 1 is at top)
    vertices = {}
    for i in range(1, 8):
        angle = math.pi / 2 + (i - 1) * 2 * math.pi / 7  # counter-clockwise from top
        vertices[i] = (math.cos(angle), math.sin(angle))

    return {
        'n_points': 7,
        'n_lines':  7,
        'points':   list(range(1, 8)),
        'lines':    fano_lines,
        'vertices': vertices,
        'note': (
            'Each Fano line {i,j,k} is a closed triple: eᵢeⱼ = ±eₖ (cyclic). '
            'The Fano plane encodes the full octonion multiplication structure. '
            'At T_256 (k=8): 32 Fano planes = 32 octonion sub-algebras embedded in 𝕊.'
        ),
    }


def fano_tower_layout() -> List[Dict]:
    """
    Tower of Fano planes across CD levels k=0..8.

    At k < 3: no Fano structure (dim too small).
    At k = 3 (𝕆): 1 Fano plane.
    At k = 4..8: 2^(k-3) Fano planes per level, doubling with each CD step.
    Total planes in tower: 0+0+0+1+2+4+8+16+32 = 63.

    Layout for rendering (Space C):
        Each level is a horizontal row at z = level_sigma * scale.
        Planes in a row are spaced uniformly in x.
        Row k has n_fano(k) planes; the row width is 2^(k-3) × spacing.
    """
    fano_base   = fano_plane_data()
    spacing_x   = 2.5    # Blender units between adjacent Fano planes
    scale_z     = 3.0    # z-scale for sigma

    tower = []
    total_planes = 0
    for k in range(N_LEVELS):
        lv     = cd_level_data(k)
        n_f    = lv['n_fano']
        z_pos  = lv['sigma'] * scale_z

        if n_f == 0:
            tower.append({
                'k':       k,
                'name':    lv['name'],
                'sigma':   lv['sigma'],
                'n_fano':  0,
                'planes':  [],
                'z':       z_pos,
            })
            continue

        total_planes += n_f
        planes = []
        row_width = (n_f - 1) * spacing_x
        for fi in range(n_f):
            x_pos = -row_width / 2.0 + fi * spacing_x

            # N-shape coverage: which N-shape does this Fano plane serve?
            # Fano plane fi at level k covers N-shapes:
            #   ns where ns % n_f == fi  (round-robin assignment)
            covered_ns = [ns for ns in range(16) if ns % n_f == fi]

            # Monster gap planes: those covering {1, 11, 15}
            covers_gap = any(ns in NIEMEIER_GAP for ns in covered_ns)

            planes.append({
                'fi':         fi,
                'x':          x_pos,
                'z':          z_pos,
                'covered_ns': covered_ns,
                'covers_gap': covers_gap,
                'lines':      fano_base['lines'],
                'vertices':   fano_base['vertices'],
            })

        tower.append({
            'k':      k,
            'name':   lv['name'],
            'sigma':  lv['sigma'],
            'n_fano': n_f,
            'planes': planes,
            'z':      z_pos,
        })

    return tower


# ── 8. Full Telperion dataset ──────────────────────────────────────────────────

def telperion_data(N: int = 500) -> Dict:
    """
    Complete Telperion dataset for rendering in all three coordinate spaces.

    N: compute primes up to N (leaves of the tree).

    Returns:
        primes          — list of all prime leaves
        prime_paths     — full tower path for each prime (first 100 for size)
        tower           — CD tower structure (k=0..8)
        survival        — Fermat survival table
        fractal_boundary— density data at each level and N-shape
        gap_fractal     — prime gap distribution (fractal character)
        fano_tower      — Fano plane layout for Space C
        nshape_summary  — N-shape classification summary
    """
    primes = prime_sieve(N)
    classified = [classify_prime(p) for p in primes]

    # N-shape distribution
    ns_dist = {ns: 0 for ns in range(16)}
    for p in primes:
        ns_dist[p % 16] += 1

    nshape_summary = {}
    for ns in range(16):
        cnt = ns_dist[ns]
        in_gap = ns in NIEMEIER_GAP
        nshape_summary[ns] = {
            'ns':           ns,
            'count':        cnt,
            'fraction':     cnt / len(primes) if primes else 0.0,
            'is_gap':       in_gap,
            'is_leech':     ns == LEECH_SHAPE,
            'in_prime_sec': ns in PRIME_SECTOR,
            'voa_type':     ('Monster/siblings' if in_gap
                             else ('Leech' if ns == LEECH_SHAPE
                                   else 'Niemeier')),
        }

    # Only first 100 prime paths (full paths are large)
    prime_paths_sample = [prime_tower_path(p) for p in primes[:100]]

    return {
        'N':                 N,
        'primes':            primes,
        'n_primes':          len(primes),
        'nshape_summary':    nshape_summary,
        'tower':             full_tower(),
        'prime_paths_100':   prime_paths_sample,
        'survival':          fermat_survival_table(min(N, 200)),
        'fractal_boundary':  fractal_boundary_data(primes),
        'gap_fractal':       prime_gap_fractal(primes),
        'fano_tower':        fano_tower_layout(),
        'monster_gap':       sorted(NIEMEIER_GAP),
        'moonshine_primes':  MOONSHINE_PRIMES,
    }


# ── 9. Blender-ready JSON export ───────────────────────────────────────────────

def export_blender_json(N: int = 500, output_path: Optional[str] = None) -> str:
    """
    Export Telperion data to JSON for consumption by Blender scripts.

    The JSON contains:
        - Prime leaf positions in all three coordinate spaces (first 200 primes)
        - Fractal boundary contours at each level (16 N-shapes × 9 levels)
        - Fano tower layout (63 planes)
        - Monster gap annotation (which positions are Telperion silver)

    Returns the path written to.
    """
    if output_path is None:
        output_path = os.path.join(
            os.path.dirname(os.path.dirname(_HERE)),
            'ZeroTree', 'telperion_blender_data.json'
        )

    primes  = prime_sieve(N)
    frac    = fractal_boundary_data(primes)
    fano_t  = fano_tower_layout()
    tower   = full_tower()

    # Prime paths for ALL primes up to N (positions only, for Blender scatter)
    prime_positions = []
    for p in primes:
        ns = p % 16
        q  = ns % 4
        positions_per_level = []
        for k in range(N_LEVELS):
            lv   = cd_level_data(k)
            base = lv['base_deg']
            jt   = lv['j_type']
            phi  = base + q * 90.0
            if jt == 'J_red':
                phi += THE_ANGLE
            elif jt == 'J_blue':
                phi -= THE_ANGLE

            R     = 3.0
            theta = lv['theta_rad']
            phi_r = math.radians(phi)

            positions_per_level.append({
                'k': k,
                # Space A
                'sph': [
                    R * math.sin(theta) * math.cos(phi_r),
                    R * math.sin(theta) * math.sin(phi_r),
                    R * math.cos(theta),
                ],
                # Space B
                'plane': [
                    (2.0 if k > 0 else 0.0) * math.cos(phi_r),
                    (2.0 if k > 0 else 0.0) * math.sin(phi_r),
                    lv['sigma'] * 4.0,
                ],
                # Space C: fano plane index
                'fano_idx': (ns % lv['n_fano']) if lv['n_fano'] > 0 else 0,
            })

        prime_positions.append({
            'p':          p,
            'ns':         ns,
            'is_gap':     ns in NIEMEIER_GAP,
            'is_moonshine': p in MOONSHINE_SET,
            'log_p':      math.log(p),
            'positions':  positions_per_level,
        })

    # Fractal boundary contours per level (for Blender polyline rendering)
    boundary_contours = {}
    for k in range(N_LEVELS):
        lv_frac = frac['level_boundary'][k]
        contour = []
        for ns in range(16):
            ns_data = lv_frac['nshape_density'][ns]
            phi_r   = math.radians(ns_data['phi_deg'])
            r       = ns_data['radius']
            contour.append({
                'ns':     ns,
                'phi':    ns_data['phi_deg'],
                'x':      r * math.cos(phi_r),
                'y':      r * math.sin(phi_r),
                'count':  ns_data['count'],
                'is_gap': ns_data['is_gap'],
            })
        boundary_contours[str(k)] = contour

    # Serialize (convert any non-JSON-safe objects)
    def _make_safe(obj):
        if isinstance(obj, dict):
            return {str(k): _make_safe(v) for k, v in obj.items()}
        if isinstance(obj, (list, tuple)):
            return [_make_safe(v) for v in obj]
        if isinstance(obj, float):
            if math.isnan(obj) or math.isinf(obj):
                return None
            return obj
        return obj

    payload = _make_safe({
        'N':                  N,
        'n_primes':           len(primes),
        'monster_gap':        sorted(NIEMEIER_GAP),
        'tower':              tower,
        'prime_positions':    prime_positions,
        'boundary_contours':  boundary_contours,
        'fano_tower':         fano_t,
        'nshape_phi':         {ns: ns * 22.5 for ns in range(16)},
    })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(payload, f, indent=2)

    return output_path


# ── Master runner ──────────────────────────────────────────────────────────────

def run_all(N: int = 500) -> Dict:
    """Full Telperion analysis.  Prints summary, returns data."""
    print("=" * 64)
    print("TELPERION — The Un-Extinctable Bulk")
    print("The Zero Tree.  The White Tree.  The primes that cannot fall.")
    print("=" * 64)

    data = telperion_data(N)

    primes = data['primes']
    print(f"\n  Leaves (primes ≤ {N}): {data['n_primes']}")
    print(f"  First 10: {primes[:10]}")
    print(f"  Last 10:  {primes[-10:]}")

    print("\n  N-shape distribution (p mod 16):")
    ns = data['nshape_summary']
    for k in range(16):
        entry = ns[k]
        gap_mark  = ' ← MONSTER GAP (Telperion silver)' if entry['is_gap'] else ''
        leech_mark = ' ← Leech (identity shape)'        if entry['is_leech'] else ''
        print(f"    e{k:2d}: {entry['count']:4d} primes  ({entry['fraction']*100:5.2f}%)"
              f"  [{entry['voa_type']}]{gap_mark}{leech_mark}")

    print("\n  Fermat survival frontier:")
    surv = data['survival']
    print(f"    N={surv['N']}: {surv['n_primes']} survive (primes), "
          f"{surv['n_composites']} fall (composites at k=4)")

    print("\n  Fractal boundary:")
    fb = data['fractal_boundary']
    print(f"    Gap N-shapes density fraction: {fb['gap_density_frac']*100:.2f}%")
    print(f"    Niemeier density fraction:     {fb['niemeier_density_frac']*100:.2f}%")
    print(f"    Dirichlet expected per ns:     {fb['dirichlet_expected']*100:.2f}%")

    gf = data['gap_fractal']
    print(f"\n  Prime gap fractal:")
    print(f"    N gaps:             {gf['n_gaps']}")
    print(f"    Mean gap:           {gf['mean_gap']:.4f}")
    print(f"    Min / Max gap:      {gf['min_gap']} / {gf['max_gap']}")
    print(f"    Self-similar ratio: {gf['self_similar_ratio']:.6f}")

    print("\n  Fano tower (Space C):")
    ft = data['fano_tower']
    for lv in ft:
        if lv['n_fano'] > 0:
            gap_planes = sum(1 for pl in lv['planes'] if pl['covers_gap'])
            print(f"    k={lv['k']} {lv['name']:<8}: {lv['n_fano']:2d} Fano planes"
                  f"  ({gap_planes} cover Monster gap)")

    print("\n  Export JSON for Blender...")
    json_path = export_blender_json(N)
    print(f"    Written: {json_path}")

    print("\n" + "=" * 64)
    print("TELPERION COMPUTED.")
    print("Leaves: primes.  Root: T_256.  The tree: un-extinctable.")
    print("Fermat's Nightmare found nothing here to shake.")
    print("=" * 64)

    return data


if __name__ == '__main__':
    run_all(N=1000)
