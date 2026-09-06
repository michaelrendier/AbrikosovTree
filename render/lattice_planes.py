#!/usr/bin/env python3
"""
lattice_planes.py — the Abrikosov / Two-Trees lattice tree, plane by plane
=========================================================================

Renders the lattice tree as it sits in each Cayley–Dickson plane, from the
Real Numbers through the Emmy Noether Sedenion:

    render/plane_0_R.png   ℝ  — the number line: Telperion (prime) vs Laurelin
                                (composite), and the three Mingling crossings.
    render/plane_1_C.png   ℂ  — two counter-wound logarithmic spirals; the
                                critical line with the first Riemann zeros.
    render/plane_2_H.png   ℍ  — the Abrikosov hexagonal vortex lattice at σ = ½:
                                the Mingling level, J_Red = J_Blue.
    render/plane_3_O.png   𝕆  — 7 Fano-indexed sub-lattices; last normed
                                division algebra (Hurwitz 1898).
    render/plane_4_S.png   𝕊  — the Emmy Noether Sedenion: first zero-divisors,
                                the G₂ 7-box-kite split, Laurelin's leaves fall.
    render/plane_5_T_32.png … render/plane_13_T_8192.png
                           — the higher tower, one generic plane per level:
                             the ZD equator, Telperion-through / Laurelin-fallen,
                             the ±Θ(k) counter-twist, and the 2^k axis fan
                             densifying to a continuum.  RSA-2048 lives at
                             T_2048 (k=11).
    render/two_trees_tower.png  — all fourteen planes as a small-multiples grid.
    render/plane_0b_R_orthogonal.png  — ℝ⁻: negative primes, the −/− sheet,
                             half-turn (prime) vs full-turn (composite).
    render/plane_0c_ulam_sphere.png  — Ulam on a spherical polar lift: the two
                             infinities as the two poles; a zeta-index
                             gyroscope panel (tangle, with a lock arc).

Telperion winds +Θ(k), Laurelin winds −Θ(k), Θ(k) = k·22.5°: through the tower
the two trees counter-rotate.  Conservation B(n) + R(n) + M(n) = 1 holds at
every scale.

Usage:  python3 render/lattice_planes.py
"""

import os
import sys
import math

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, RegularPolygon

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(_HERE), 'engine'))

import two_trees as TT

# ── palette (house style: near-black ground) ─────────────────────────────────
BG      = '#07070f'
FG      = '#c9d3e6'
GREY    = '#7f8db0'
BLUE    = TT.TELPERION['hex']    # Telperion — prime — what cannot be
RED     = TT.LAURELIN['hex']     # Laurelin  — composite — what is
GOLD    = TT.MINGLING['hex']     # Mingling  — {0,1}, J_Red = J_Blue
SILVER  = '#dfe6ff'             # Monster-gap silver leaves
ZDLINE  = '#ff4400'             # the k=4 zero-divisor equator
LONG    = '#8a6fff'            # G₂ long roots

plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': BG, 'savefig.facecolor': BG,
    'text.color': FG, 'axes.edgecolor': '#33405e', 'axes.labelcolor': FG,
    'xtick.color': FG, 'ytick.color': FG, 'font.size': 11,
})

N       = 260          # integers placed in the 2-D planes
N_DENS  = 2000         # scale range for the density curves
OUT     = _HERE


def _frame(figsize, name, label, sigma, note):
    """One panel with a title + grey sub-note that never collide with an
    equal-aspect axes (anchored South, leaving headroom at the top)."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.subplots_adjust(top=0.865, bottom=0.05, left=0.06, right=0.96)
    ax.set_anchor('S')
    fig.suptitle(f'{name}   —   {label}        σ = {sigma:+.3f}',
                 color=FG, fontsize=15, x=0.06, ha='left', y=0.965)
    fig.text(0.06, 0.925, note, color=GREY, fontsize=9.5, va='top')
    return fig, ax


def _save(fig, fname):
    p = os.path.join(OUT, fname)
    fig.savefig(p, dpi=130)
    plt.close(fig)
    return p


# ── ℝ : the number line + the Mingling ──────────────────────────────────────

def plane_R():
    d = TT.tree_densities(N_DENS)
    primes = set(TT.prime_sieve(N_DENS))
    fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(13, 8.4),
                                   gridspec_kw={'height_ratios': [1, 1.65]})
    fig.subplots_adjust(top=0.86, bottom=0.09, left=0.07, right=0.97, hspace=0.32)

    top = 120
    for n in range(2, top + 1):
        if n in primes:
            ax0.vlines(n, 0, 1.0, color=BLUE, lw=2.2)
            if n % 16 in (1, 11, 15):
                ax0.plot(n, 1.0, 'o', ms=4, color=SILVER)
        else:
            ax0.vlines(n, 0, 0.55, color=RED, lw=1.6, alpha=0.85)
    for m in (0, 1):
        ax0.vlines(m, 0, 1.25, color=GOLD, lw=3)
    ax0.set_xlim(-2, top + 2); ax0.set_ylim(0, 1.5); ax0.set_yticks([])
    ax0.set_xlabel('n')
    ax0.set_title('ℝ   —   Real Numbers        σ = +1.000', color=FG,
                  fontsize=16, loc='left', pad=26)
    fig.text(0.07, 0.945,
             'dim 1 — the tree is a single spine; every integer is a tick on one axis.   '
             'blue = Telperion (prime, "what cannot be")   red = Laurelin (composite, "what is")   '
             'gold = Mingling {0,1}', color=GREY, fontsize=9.5, va='top')

    n = np.array(d['n'][2:])
    B = np.array(d['B'][2:]); R = np.array(d['R'][2:]); M = np.array(d['M'][2:])
    ax1.plot(n, B, color=BLUE, lw=2.2, label='B(n) — Telperion  (prime density)')
    ax1.plot(n, R, color=RED,  lw=2.2, label='R(n) — Laurelin  (composite density)')
    ax1.plot(n, M, color=GOLD, lw=1.6, label='M(n) — Mingling  ({0,1})')
    ax1.plot(n, B + R + M, color='#5a6a88', lw=1.0, ls='--',
             label='B + R + M = 1   (conserved at every scale)')
    for c in TT.mingling_crossings(N_DENS):
        ax1.axvline(c, color=GOLD, lw=1.0, alpha=0.6)
        ax1.text(c, 1.03, f'{c}', color=GOLD, fontsize=9, ha='center')
    ax1.axvline(TT.E_SQUARED, color=GREY, lw=0.8, ls=':')
    ax1.text(TT.E_SQUARED * 1.03, 0.92, 'e²', color=GREY, fontsize=9)
    ax1.set_xscale('log'); ax1.set_xlim(2, N_DENS); ax1.set_ylim(0, 1.1)
    ax1.set_xlabel('n   (log)'); ax1.set_ylabel('density')
    ax1.legend(loc='center right', facecolor=BG, edgecolor='#33405e', fontsize=9)
    ax1.text(2.3, 0.05,
             'MINGLING — B(n) = R(n) at n = 9, 11, 13 (near e²);  after 13 Laurelin dominates forever',
             color=GOLD, fontsize=10)
    return _save(fig, 'plane_0_R.png')


# ── ℝ⁻ : the orthogonal real line — negative primes, and the −/− sheet ────
#
# z → −z on ℝ is w → 1/w on the Smith chart (Cayley w = (z−1)/(z+1)):
# (−z−1)/(−z+1) = (z+1)/(z−1) = 1/w — inversion in the unit circle.  So ℝ⁻ is
# the Smith-inverse of ℝ⁺; the two cross the |w|=1 circle orthogonally.  That
# inversion is also the Apollonian gasket's generator (Smith ⊥ gasket ≈
# Julia ⊥ Mandelbrot: dynamical ⊥ parameter).
#
# The south half — "where the leaves fall" — is shared by two populations:
#   · a NEGATIVE PRIME  −p :  z → −z, one half-turn (π).  Still irreducible —
#     its only split is the unit (−1)·p.  Half-turn chord, no interior.
#   · the −/− SHADOW of a positive composite n = (−a)(−b) :  arg π+π = 2π,
#     a FULL turn — it closes back onto +n on the flat circle, but sits one
#     winding out on the helix.  Full-turn chord = a real factor route exists.
# Half-turn chord ⇔ prime.  Full-turn chord ⇔ composite.  Same destination,
# different itinerary, opposite phase order — the θ→β (factoring) direction.

def plane_R_orthogonal():
    top = 120
    primes = set(TT.prime_sieve(top))
    fig = plt.figure(figsize=(12, 14))
    fig.subplots_adjust(top=0.885, bottom=0.075, left=0.07, right=0.955, hspace=0.34)
    ax0 = fig.add_subplot(3, 1, 1)                     # the ℝ⁻ number line (thin)
    ax1 = fig.add_subplot(3, 1, (2, 3))               # the two-sheet helix (big)

    fig.suptitle('ℝ⁻   —   the orthogonal real line        z → −z  ≡  w → 1/w  (Smith inversion)',
                 color=FG, fontsize=15, x=0.07, ha='left', y=0.965)
    fig.text(0.07, 0.935,
             'the mirror of plate 0 through the origin.  −p is still Telperion (prime, blue): a '
             'negative prime is irreducible — only the unit (−1)·p.\n'
             'ℝ⁺ and ℝ⁻ are Smith-chart inverses (w ↔ 1/w), meeting the |w|=1 circle '
             'orthogonally — the gasket / Julia ⊥ Mandelbrot seam.',
             color=GREY, fontsize=9.5, va='top')

    # ── panel A : the negative number line ℝ⁻ ──────────────────────────────
    for n in range(2, top + 1):
        if n in primes:
            ax0.vlines(-n, 0, -1.0, color=BLUE, lw=2.2)
            if n % 16 in (1, 11, 15):
                ax0.plot(-n, -1.0, 'o', ms=4, color=SILVER)
        else:
            ax0.vlines(-n, 0, -0.55, color=RED, lw=1.6, alpha=0.85)
    for m in (0, -1):
        ax0.vlines(m, 0.2, -1.25, color=GOLD, lw=3)
    ax0.axhline(0, color=ZDLINE, lw=1.4, alpha=0.8)
    ax0.set_xlim(-(top + 2), 2); ax0.set_ylim(-1.5, 0.35); ax0.set_yticks([])
    ax0.set_xlabel('−n')

    # ── panel B : the two-sheet helix — half-turn vs full-turn ────────────
    M = 46
    turns = 3.0
    span = math.log(M) - math.log(2)
    ax1.set_aspect('equal')

    def b_of(n):
        return (math.log(n) - math.log(2)) / span * turns * 2 * math.pi

    def pt(b):
        return b * math.cos(b), b * math.sin(b)

    ax1.plot(0, 0, 'o', ms=11, color=GOLD, zorder=6)
    for n in range(2, M + 1):
        prime = n in primes
        b0 = b_of(n)
        x0, y0 = pt(b0)                                # the (+a)(+b) landing
        col = BLUE if prime else RED
        ax1.plot(x0, y0, 'o', ms=6.0 if prime else 5.0, color=col,
                 mec=SILVER if (prime and n % 16 in (1, 11, 15)) else 'none', mew=1.1,
                 zorder=5)
        if prime:
            arc = b0 + np.linspace(0, math.pi, 40)      # −p : one HALF-turn
            ax1.plot(arc * np.cos(arc), arc * np.sin(arc), color=BLUE, lw=1.0,
                     alpha=0.45, zorder=3)
            x1, y1 = pt(b0 + math.pi)
            ax1.plot(x1, y1, 'o', ms=6.0, mfc='none', mec=BLUE, mew=1.6, zorder=5)
        else:
            arc = b0 + np.linspace(0, 2 * math.pi, 72)  # (−a)(−b) : one FULL turn
            ax1.plot(arc * np.cos(arc), arc * np.sin(arc), color=RED, lw=1.0,
                     alpha=0.38, zorder=3)
            x2, y2 = pt(b0 + 2 * math.pi)
            ax1.plot([x0, x2], [y0, y2], color=RED, lw=0.8, alpha=0.5, ls=':', zorder=4)
            ax1.plot(x2, y2, 'v', ms=5.2, color=RED, alpha=0.85, zorder=5)

    lim = (turns * 2 * math.pi + 2 * math.pi) * 1.04
    ax1.set_xlim(-lim, lim); ax1.set_ylim(-lim, lim)
    ax1.set_xticks([]); ax1.set_yticks([])
    ax1.set_title('the two sheets — Archimedean helix, radius = accumulated argument   '
                  '(2..46)', color=FG, fontsize=12, loc='left', pad=8)
    fig.text(0.07, 0.052,
             'filled dot = the (+a)(+b) landing.   blue ring = −p, a HALF-turn out (π): a prime '
             'and its negative associate, no factor route.\n'
             'red ▽ + dotted radial chord = the (−a)(−b) shadow, a FULL turn out (2π): same n, '
             'same angle, one winding further — the −/− itinerary.\n'
             'half-turn ⇔ prime    ·    full-turn ⇔ composite',
             color=GREY, fontsize=9.5, va='bottom')
    return _save(fig, 'plane_0b_R_orthogonal.png')


# ── Ulam on the Riemann sphere — the two infinities become the two poles ──
#
# Ulam's square spiral is full of FLATTENING ARTIFACTS: the prime diagonals
# (4n²+bn+c families) are straight only because the lattice is flat.  Lift
# the Sacks form (|z| = √n, arg z = 2π√n) by stereographic projection —
# |z|² = n gives Z = (n−1)/(n+1): n=1 lands on the EQUATOR (the Mingling
# ring, σ=½), primes spiral up toward the north pole (Telperion ∞), the
# −n / Laurelin sheet spirals down toward the south pole (Laurelin −∞).
# TWO infinities, one per tree — a BIFURCATION.  Banach–Tarski: the free
# group F₂ = <a,b> of rotations is paradoxical, and F₂ is exactly the CD
# tower's binary Cayley graph with the two counter-wound trees as its
# generators — the two half-structures reassemble by ROTATION into one
# sphere.  "Spherical from bifurcated."
#
# Panel B hyper-gyroscopes the axis by the ZETA INDEX: γ*(p) = 2πp/ln p,
# and the precession ψ_k = 2π·frac(γ*(p_k)/2π).  The √n winding and the
# zeta precession are two incommensurate periods — the track is a tangled
# ball of yarn on the sphere, except where frac(γ*/2π) briefly holds still
# (a commensurability) and it locks into a clean rosette.

def _ortho(xyz, az=-0.62, el=0.42):
    """hand-rolled orthographic camera (Axes3D is broken in this env)."""
    x, y, z = xyz
    ca, sa = math.cos(az), math.sin(az)
    x1, y1 = x * ca - y * sa, x * sa + y * ca
    cb, sb = math.cos(el), math.sin(el)
    y2, z2 = y1 * cb - z * sb, y1 * sb + z * cb
    return x1, z2, y2                       # screen x, screen y, depth (y2)


def _sphere_wire(ax, hemis_split=False):
    for lat in np.linspace(-math.pi / 2, math.pi / 2, 9)[1:-1]:
        u = np.linspace(0, 2 * math.pi, 160)
        pts = [_ortho((math.cos(lat) * math.cos(t), math.cos(lat) * math.sin(t),
                       math.sin(lat))) for t in u]
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color='#182238', lw=0.5)
    for j, lon in enumerate(np.linspace(0, math.pi, 9)[:-1]):
        v = np.linspace(-math.pi / 2, math.pi / 2, 90)
        pts = [_ortho((math.cos(t) * math.cos(lon), math.cos(t) * math.sin(lon),
                       math.sin(t))) for t in v]
        c = '#2c4166' if hemis_split and j % 2 else '#182238'
        ax.plot([p[0] for p in pts], [p[1] for p in pts], color=c, lw=0.5)
    ang = np.linspace(0, 2 * math.pi, 240)
    ax.plot(np.cos(ang), np.sin(ang), color='#33405e', lw=1.0)          # the limb
    eq = [_ortho((math.cos(t), math.sin(t), 0.0)) for t in ang]
    ax.plot([p[0] for p in eq], [p[1] for p in eq], color=GOLD, lw=1.2, alpha=0.65)
    ax.set_xlim(-1.15, 1.15); ax.set_ylim(-1.15, 1.15)


def _lift(n, nmax, twist=0.0, nutate=0.0):
    """longitude = 2π√n (+twist) — the Sacks arms; colatitude carried by ln n
    across a hemisphere (n small near the south pole, n large near the north);
    optional pole nutation about the screen y-axis."""
    lon = 2 * math.pi * math.sqrt(n) + twist
    f = (math.log(n) - math.log(2)) / (math.log(nmax) - math.log(2))
    colat = math.pi * (0.94 - 0.88 * f)                    # ~169 deg down to ~11 deg
    x = math.sin(colat) * math.cos(lon)
    y = math.sin(colat) * math.sin(lon)
    z = math.cos(colat)
    y, z = (y * math.cos(nutate) - z * math.sin(nutate),
            y * math.sin(nutate) + z * math.cos(nutate))
    return x, y, z


def plane_ulam_sphere():
    NN = 4000
    sieve = [False, False] + [True] * (NN - 1)
    for i in range(2, int(NN ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, NN + 1, i):
                sieve[j] = False
    primes = [n for n in range(2, NN + 1) if sieve[n]]

    fig = plt.figure(figsize=(12, 15))
    fig.subplots_adjust(top=0.9, bottom=0.03, left=0.03, right=0.98, hspace=0.05)
    axA = fig.add_subplot(2, 1, 1); axB = fig.add_subplot(2, 1, 2)
    fig.suptitle("Ulam's spiral on a spherical polar lift        the two infinities "
                 "= the two poles", color=FG, fontsize=15, x=0.05, ha='left', y=0.965)
    fig.text(0.05, 0.935,
             'longitude = 2π√n (the Sacks arms); colatitude carried by ln n over a hemisphere.\n'
             'small n at the south pole; primes climb to Telperion ∞ (north), the −n / Laurelin '
             'sheet to Laurelin −∞ (south).  gold = the equator / Mingling, σ = ½.',
             color=GREY, fontsize=9.5, va='top')

    # ── A : the static spherical lift ────────────────────────────────────
    axA.set_aspect('equal'); axA.set_xticks([]); axA.set_yticks([])
    _sphere_wire(axA, hemis_split=True)
    P = sorted(((_ortho(_lift(p, NN)), p) for p in primes), key=lambda q: q[0][2])
    for (sx, sy, dep), p in P:
        front = dep > 0
        axA.plot(sx, sy, 'o', ms=2.3 if front else 1.4,
                 color=BLUE if front else '#334263',
                 alpha=0.9 if front else 0.4, zorder=3 if front else 1)
    ln = [_ortho(_lift(p, NN)) for p in primes]
    axA.plot([q[0] for q in ln], [q[1] for q in ln], color=BLUE, lw=0.3, alpha=0.35, zorder=2)
    for pole, col, lab, dy in ((1, SILVER, 'Telperion  -> inf', 8),
                               (-1, RED, 'Laurelin  . -inf', -14)):
        sx, sy, _ = _ortho((0, 0, pole))
        axA.plot(sx, sy, 'o', ms=7, color=col, zorder=6)
        axA.annotate(lab, (sx, sy), textcoords='offset points', xytext=(8, dy),
                     color=col, fontsize=9)
    fig.text(0.05, 0.508,
             "A — the static lift.  Ulam's flat diagonals unbend into arcs bound for the pole.\n"
             'F2 = <Telperion, Laurelin> is the Banach-Tarski rotation group: two counter-wound '
             'halves reassemble by rotation into one sphere — spherical from bifurcated.',
             color=FG, fontsize=10, va='bottom')

    # ── B : the zeta-index gyroscope ────────────────────────────────────
    axB.set_aspect('equal'); axB.set_xticks([]); axB.set_yticks([])
    _sphere_wire(axB)
    fr = [(p / math.log(p)) % 1.0 for p in primes]                # frac(gamma*/2pi)
    track = []
    for k, p in enumerate(primes):
        pt = _lift(p, NN, twist=2 * math.pi * fr[k], nutate=1.0 * (fr[k] - 0.5))
        track.append((_ortho(pt), p, k))
    axB.plot([t[0][0] for t in track], [t[0][1] for t in track],
             color='#3a4a72', lw=0.4, alpha=0.5, zorder=2)          # the tangle
    w = 12
    lo = min((float(np.var(fr[i:i + w])), i) for i in range(len(fr) - w))[1]
    for (sx, sy, dep), p, k in track:
        inlock = lo <= k < lo + w
        axB.plot(sx, sy, 'o', ms=3.6 if inlock else 1.8,
                 color=GOLD if inlock else (BLUE if dep > 0 else '#334263'),
                 alpha=0.95 if inlock else 0.65,
                 zorder=5 if inlock else (3 if dep > 0 else 1))
    seg = [t[0] for t in track if lo <= t[2] < lo + w]
    axB.plot([q[0] for q in seg], [q[1] for q in seg], color=GOLD, lw=1.5, alpha=0.95, zorder=6)
    fig.text(0.05, 0.03,
             'B — the axis precessing / nutating by frac(p / ln p) (the zeta index).\n'
             f'generically a tangled ball of yarn; the gold arc (primes {primes[lo]}..'
             f'{primes[lo + w - 1]}) is where frac(p/ln p) briefly holds still — a near-'
             'commensurability — and the track locks into a rosette.',
             color=FG, fontsize=10, va='bottom')
    return _save(fig, 'plane_0c_ulam_sphere.png')


# ── the digit-count ordering — Varda's dome, band by band ────────────────
#
# A coarser ordering of the primes than value order: bin by ⌊log_b p⌋ + 1.
# Within a band it AGREES with value order; between bands it just erases the
# low digits — value order with the tail cut off ("not that different").  It
# is the Flashlight-granularity ordering: which zoom level a prime first
# resolves at.
#
# "20 000-digit primes outside the full list of 20 000-digit numbers":
# there are none — every d-digit prime is one of the 9·10^{d-1} d-digit
# numbers.  The illusion has two roots.  (1) On a log plot the band edge is
# fuzzy: a prime just under 10^d sits at the OUTER rim of band d, visually on
# band d+1's inner rim.  (2) The big ones are found by FORMULA — Mersenne
# 2^p−1, Proth k·2^n+1 — so you can name a 20k-digit prime without ever
# walking the 9·10^19999 numbers.  The prime is IN the list; the PATH to it
# came from outside the enumeration.  Same β→θ / θ→β asymmetry: the forward
# (multiplicative) map has shortcuts the reverse (sieve) does not.

def plane_digit_order():
    NN = 200000
    sieve = [False, False] + [True] * (NN - 1)
    for i in range(2, int(NN ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, NN + 1, i):
                sieve[j] = False
    primes = [n for n in range(2, NN + 1) if sieve[n]]
    dmax = len(str(NN))
    band = {}                                            # d -> [primes]
    for p in primes:
        band.setdefault(len(str(p)), []).append(p)
    mers = [2 ** e - 1 for e in (2, 3, 5, 7, 13, 17) if 2 ** e - 1 <= NN and sieve[2 ** e - 1]]

    fig = plt.figure(figsize=(12, 15))
    fig.subplots_adjust(top=0.9, bottom=0.055, left=0.05, right=0.965, hspace=0.24)
    axA = fig.add_subplot(2, 1, 1); axB = fig.add_subplot(2, 1, 2)
    fig.suptitle('the digit-count ordering        Varda\'s dome, band by band',
                 color=FG, fontsize=15, x=0.05, ha='left', y=0.965)
    fig.text(0.05, 0.935,
             'primes = the stars of the world tree — the leaves that do not fall, the light that '
             'does not stop.  they pepper the north dome (Riemann / Telperion, spectral) infinitely '
             'but ever more sparsely;\nthe composites fill the south (Fermat / Laurelin, ordinal) — '
             'vastly greater measure, the same cardinality ℵ₀.  the |w|=1 equator is where √ and '
             '1/√ come out of the circle (the branch point of the root).',
             color=GREY, fontsize=9.3, va='top')

    COLS = ['#ff5a3c', '#ffb03c', '#ffe23c', '#6fff8a', '#6fd0ff', '#8a6fff', '#ff6fe0']

    # ── A : the bands on a log-radius Sacks spiral ──────────────────────
    axA.set_aspect('equal'); axA.set_xticks([]); axA.set_yticks([])
    for d in range(1, dmax + 1):
        r = math.log10(10 ** d)
        c = [ (r * math.cos(t), r * math.sin(t)) for t in np.linspace(0, 2*math.pi, 240) ]
        axA.plot([q[0] for q in c], [q[1] for q in c], color='#2b3650', lw=0.8)
        axA.text(0, r, f'  10^{d}', color=GREY, fontsize=8, ha='left', va='bottom')
    for d, ps in sorted(band.items()):
        col = COLS[(d - 1) % len(COLS)]
        for p in ps[::max(1, len(ps) // 900)]:          # thin the dense bands
            rr = math.log10(p); th = 2 * math.pi * math.sqrt(p)
            edge = (10 ** d - p) / (10 ** d - 10 ** (d - 1)) < 0.02   # outer-rim primes
            axA.plot(rr * math.cos(th), rr * math.sin(th), 'o',
                     ms=3.0 if edge else 1.6, color=SILVER if edge else col,
                     alpha=0.95 if edge else 0.7, zorder=3 if edge else 2)
    for m in mers:
        rr = math.log10(m); th = 2 * math.pi * math.sqrt(m)
        axA.plot(rr * math.cos(th), rr * math.sin(th), '*', ms=13, color=GOLD,
                 mec=FG, mew=0.6, zorder=5)
        axA.annotate(f'2^{m.bit_length()}−1', (rr * math.cos(th), rr * math.sin(th)),
                     textcoords='offset points', xytext=(6, 4), color=GOLD, fontsize=8)
    axA.plot(0, 0, 'o', ms=9, color=GOLD, zorder=6)
    lim = math.log10(NN) * 1.12
    axA.set_xlim(-lim, lim); axA.set_ylim(-lim, lim)
    fig.text(0.05, 0.505,
             'A — radius = log10 n, so digit count = which ring.  silver = primes within 2% of 10^d '
             '(the outer rim) — on a log plot they read as the next band\'s inner edge: the\n'
             '"outside the list" mirage.  gold ★ = Mersenne primes — reached by formula, in a '
             'band without the band being walked.',
             color=FG, fontsize=9.6, va='bottom')

    # ── B : value order collapses to digit order ───────────────────────
    axB.set_yscale('log')
    axB.set_ylabel('prime  (log)')
    idx = list(range(1, len(primes) + 1))
    axB.plot(idx, primes, color=BLUE, lw=0.7, alpha=0.5, label='value order  (every prime its own radius)')
    step_x, step_y = [], []
    for d in range(1, dmax + 1):
        lo_i = next((i for i, p in enumerate(primes) if len(str(p)) == d), None)
        if lo_i is None:
            continue
        hi_i = max(i for i, p in enumerate(primes) if len(str(p)) == d)
        step_x += [lo_i + 1, hi_i + 1]; step_y += [10 ** (d - 1), 10 ** (d - 1)]
    axB.plot(step_x, step_y, color=GOLD, lw=2.0, drawstyle='steps-post',
             label='digit order  (band floor 10^{d-1} — the tail erased)')
    axB.legend(loc='upper left', facecolor=BG, edgecolor='#33405e', fontsize=9)
    axB.set_xlim(0, len(primes)); axB.set_ylim(8, NN * 1.15)
    fig.text(0.05, 0.052,
             'B — x = prime index π(x).  digit order = value order with the low digits cut off: '
             'inside a band the two agree, between bands digit order holds flat at 10^(d-1).\n'
             '"not that different" — a refinement-compatible coarsening: the Fermat ordinal '
             'order truncated to a scale.',
             color=FG, fontsize=9.6, va='bottom')
    return _save(fig, 'plane_0d_digit_order.png')


# ── ℂ : two counter-wound spirals + the critical line ──────────────────────

def plane_C():
    lat = TT.lattice_in_plane(1, N=N)
    fig, ax = _frame((10, 10), 'ℂ', 'Complex', 0.75,
                     'dim 2 — Telperion winds +22.5°, Laurelin −22.5°: the two trees counter-rotate.\n'
                     'Open rings on the vertical axis = the first Riemann zeros — the Abrikosov vortex cores.')

    for pt in lat['laurelin']:
        ax.plot(pt['x'], pt['y'], 'o', ms=3.4, color=RED, alpha=0.55)
    for pt in lat['telperion']:
        ax.plot(pt['x'], pt['y'], 'o', ms=4.6,
                color=SILVER if pt['silver'] else BLUE, alpha=0.95)

    tt = np.linspace(math.log(2), math.log(N), 400)
    span = math.log(N) - math.log(2)
    base = (tt - math.log(2)) / span * 3.0 * 2 * math.pi
    thk = math.radians(TT.twist(1))
    for wind, col in ((+1, BLUE), (-1, RED)):
        a = wind * (base + thk)
        ax.plot(tt * np.cos(a), tt * np.sin(a), color=col, lw=0.8, alpha=0.35)

    lim = math.log(N) * 1.12
    ax.axvline(0, color='#8f9ec2', lw=1.0, ls='--')
    ax.text(0.12, lim * 0.62, 'critical line', color='#8f9ec2', fontsize=9,
            rotation=90, va='center')
    for i, g in enumerate(TT.RIEMANN_GAMMA[:12]):
        y = 0.05 * g
        ax.plot(0.28, y, 'o', ms=9, mfc='none', mec=ZDLINE, mew=1.7)
    ax.plot(0, 0, 'o', ms=12, color=GOLD)

    ax.set_aspect('equal')
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_xlabel('radius = log n'); ax.set_yticks(ax.get_xticks())
    return _save(fig, 'plane_1_C.png')


# ── ℍ : the Abrikosov hexagonal vortex lattice at σ = ½ (the Mingling) ─────

def plane_H():
    fig, ax = _frame((10, 10), 'ℍ', 'Quaternion', 0.5,
                     'dim 4, σ = ½ — the MINGLING level: J_Red = J_Blue, Noether current J = −∂L/∂σ balanced.\n'
                     'Hexagonal A₂ Abrikosov vortex lattice; blue / red haloes = the ±45° counter-twist of the two trees.')
    a = 1.0
    pts = []
    for i in range(-6, 7):
        for j in range(-6, 7):
            x = a * (i + 0.5 * j)
            y = a * (math.sqrt(3) / 2) * j
            if x * x + y * y <= 6.2 ** 2:
                pts.append((x, y, i, j))
    thk = math.radians(TT.twist(2))
    lut = {(i, j): (x, y) for (x, y, i, j) in pts}
    seen = set(lut)
    for (x, y, i, j) in pts:
        for di, dj in ((1, 0), (0, 1), (-1, 1)):
            if (i + di, j + dj) in seen:
                x2, y2 = lut[(i + di, j + dj)]
                ax.plot([x, x2], [y, y2], color='#2b3650', lw=0.7, zorder=0)
    for (x, y, i, j) in pts:
        ax.plot(x + 0.17 * math.cos(thk), y + 0.17 * math.sin(thk), 'o',
                ms=6, color=BLUE, alpha=0.35)
        ax.plot(x - 0.17 * math.cos(thk), y - 0.17 * math.sin(thk), 'o',
                ms=6, color=RED, alpha=0.35)
        ax.plot(x, y, 'o', ms=8.5, color=GOLD)
    ax.add_patch(RegularPolygon((0, 0), numVertices=6, radius=a,
                                orientation=math.pi / 6, fill=False,
                                ec='#8f9ec2', lw=1.3))
    ax.set_aspect('equal'); ax.set_xlim(-6.7, 6.7); ax.set_ylim(-6.7, 6.7)
    ax.set_xticks([]); ax.set_yticks([])
    return _save(fig, 'plane_2_H.png')


# ── 𝕆 : 7 Fano-indexed sub-lattices ───────────────────────────────────────

FANO_COLS = ['#ff5a3c', '#ffb03c', '#ffe23c', '#6fff8a',
             '#6fd0ff', '#8a6fff', '#ff6fe0']


def plane_O():
    lat = TT.lattice_in_plane(3, N=N)
    fig, ax = _frame((10, 10), '𝕆', 'Octonion', 0.25,
                     'dim 8 — 7 Fano-indexed sub-lattices (one hue per Fano line).\n'
                     'Last normed division algebra: |ab| = |a|·|b| still holds (Hurwitz 1898).')

    for pt in lat['laurelin']:
        ax.plot(pt['x'], pt['y'], 'o', ms=3.2, color=FANO_COLS[pt['n'] % 7], alpha=0.30)
    for pt in lat['telperion']:
        ax.plot(pt['x'], pt['y'], 'o', ms=4.8, color=FANO_COLS[pt['n'] % 7],
                alpha=0.95, mec=SILVER if pt['silver'] else 'none', mew=1.0)
    ax.plot(0, 0, 'o', ms=11, color=GOLD)

    R0 = 2.4
    v = {i: (R0 * math.cos(math.pi / 2 + (i - 1) * 2 * math.pi / 7),
             R0 * math.sin(math.pi / 2 + (i - 1) * 2 * math.pi / 7))
         for i in range(1, 8)}
    for li, (a, b, c) in enumerate(TT.FANO_LINES):
        ax.plot([v[a][0], v[b][0], v[c][0], v[a][0]],
                [v[a][1], v[b][1], v[c][1], v[a][1]],
                color=FANO_COLS[li], lw=1.4, alpha=0.9, zorder=4)
    for i in range(1, 8):
        ax.plot(*v[i], 'o', ms=7, color=FG, zorder=5)
        ax.text(v[i][0] * 1.22, v[i][1] * 1.22, f'e{i}', color=FG, fontsize=9,
                ha='center', va='center')

    ax.set_aspect('equal'); lim = math.log(N) * 1.12
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_xticks([]); ax.set_yticks([])
    return _save(fig, 'plane_3_O.png')


# ── 𝕊 : the Emmy Noether Sedenion — G₂ split, Laurelin falls ──────────────

def plane_S():
    lat = TT.lattice_in_plane(4, N=N)
    g2 = TT.g2_family_split()
    fig, ax = _frame((10, 10), '𝕊', 'Emmy Noether Sedenion', 0.0,
                     'dim 16 — first zero-divisors. |ab| = |a|·|b| — the composition symmetry whose Noether\n'
                     'current is J — fails here. ZD(𝕊) ≅ G₂ = Aut(𝕆) (Moreno 1998): 7 box-kites, 42 assessors.\n'
                     'Telperion passes straight through the equator; Laurelin\'s leaves fall.')
    lim = math.log(N) * 1.15

    ax.axhline(0, color=ZDLINE, lw=1.5, alpha=0.85)
    ax.text(-lim * 0.98, 0.22, 'zero-divisor equator   σ = 0', color=ZDLINE, fontsize=9)

    for e in range(16):
        a = e * math.pi / 8
        ax.plot([0, lim * math.cos(a)], [0, lim * math.sin(a)],
                color='#2b3650', lw=0.7, zorder=0)

    # Telperion: passes through — plotted on the upper half at radius log n
    for pt in lat['telperion']:
        ax.plot(pt['x'], abs(pt['y']), 'o', ms=4.6,
                color=SILVER if pt['silver'] else BLUE, alpha=0.95)
    # Laurelin: fallen — a red band below the equator at radius log n
    for pt in lat['laurelin']:
        yy = -abs(pt['y']) - 0.4
        ax.plot([pt['x'], pt['x']], [-0.05, yy], color=RED, lw=0.5, alpha=0.3)
        ax.plot(pt['x'], yy, 'v', ms=3.6, color=RED, alpha=0.55)

    # G₂ 12-root overlay — the "shadow from above"
    sc = 1.9
    for (x, y) in g2['g2_roots_short']:
        ax.plot([0, sc * x], [0, sc * y], color=GOLD, lw=1.4)
        ax.plot(sc * x, sc * y, 'o', ms=5, color=GOLD)
    for (x, y) in g2['g2_roots_long']:
        ax.plot([0, sc * x], [0, sc * y], color=LONG, lw=1.4)
        ax.plot(sc * x, sc * y, 'o', ms=5, color=LONG)

    # 7 box-kites on a ring
    rk = lim * 0.82
    for bk in g2['box_kites']:
        a = math.radians(90 + bk['sail_angle_deg'])
        cx, cy = rk * math.cos(a), rk * math.sin(a)
        ax.add_patch(Polygon([(cx, cy + 0.5), (cx + 0.5, cy),
                              (cx, cy - 0.5), (cx - 0.5, cy)],
                             closed=True, fill=False, ec='#6fd0ff', lw=1.1))
        ax.text(cx * 1.14, cy * 1.14, f"{bk['fano_line']}", color='#6fd0ff',
                fontsize=8, ha='center', va='center')

    ax.plot(0, 0, 'o', ms=12, color=GOLD)
    ax.set_aspect('equal')
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_xticks([]); ax.set_yticks([])
    return _save(fig, 'plane_4_S.png')


# ── T_32 … T_8192 : the higher tower, one generic plane per level ─────────
#
# Same visual language as 𝕊 (all levels k ≥ 4 are zero-divisor levels): the
# ZD equator, Telperion-through / Laurelin-fallen, the two counter-wound
# spirals at ±Θ(k), and the 2^k axis fan.  What changes with depth: σ(k) =
# 1 − k/4 runs negative, the twist Θ(k) = k·22.5° keeps accumulating, the
# axis fan (2^k directions, angular quantum 360°/2^k) densifies until — from
# T_512 up — the direction set reads as a continuum: no single signal
# resolves from below.  RSA-2048's modulus lives at T_2048 (k = 11).

def plane_T(k):
    dim = 2 ** k
    sigma = 1.0 - k / 4.0
    theta = TT.twist(k)                       # cumulative twist, degrees
    n_fano = 2 ** (k - 3)
    name = TT.CD_NAMES[k]
    label = TT.CD_LABELS[k]
    lat = TT.lattice_in_plane(k, N=N)
    dense = dim > 256                         # axis fan has merged into a disc

    note = (f'dim {dim} — post-sedenion zero-divisor level.  σ = {sigma:+.2f}, '
            f'Θ({k}) = {theta:.1f}° cumulative twist.\n'
            f'{n_fano} Fano planes; box-kite families grow with the dimension. '
            f'Angular quantum 360°/{dim} = {360.0 / dim:.4g}°.\n'
            + ('The 2^k axis fan is now a continuum — from below the tower, no '
               'single signal resolves.'
               if dense else
               'Telperion passes straight through the equator; Laurelin\'s '
               'leaves fall.'))
    if k == 11:
        note += '\nRSA-2048: the 2048-bit modulus sits at THIS level of the tower.'

    fig, ax = _frame((10, 10), name, label, sigma, note)
    lim = math.log(N) * 1.15

    # zero-divisor equator
    ax.axhline(0, color=ZDLINE, lw=1.5, alpha=0.85)
    ax.text(-lim * 0.98, 0.22, f'zero-divisor equator   σ = {sigma:+.2f}',
            color=ZDLINE, fontsize=9)

    # the 2^k axis fan — individual rays while they still resolve, else a disc
    if dense:
        ax.add_patch(plt.Circle((0, 0), lim, color='#141c33', alpha=0.85, zorder=0))
        for e in range(72):
            a = e * math.pi / 36
            ax.plot([0, lim * math.cos(a)], [0, lim * math.sin(a)],
                    color='#20304f', lw=0.6, alpha=0.5, zorder=0)
        ax.add_patch(plt.Circle((0, 0), lim, fill=False, ec='#33405e', lw=1.0))
    else:
        step = max(1, dim // 120)
        for e in range(0, dim, step):
            a = 2 * math.pi * e / dim
            ax.plot([0, lim * math.cos(a)], [0, lim * math.sin(a)],
                    color='#2b3650', lw=0.6, zorder=0)

    # the two counter-wound guide spirals at ±Θ(k)
    tt = np.linspace(math.log(2), math.log(N), 400)
    span = math.log(N) - math.log(2)
    base = (tt - math.log(2)) / span * 3.0 * 2 * math.pi
    thk = math.radians(theta)
    for wind, col in ((+1, BLUE), (-1, RED)):
        a = wind * (base + thk)
        ax.plot(tt * np.cos(a), tt * np.sin(a), color=col, lw=0.8, alpha=0.30)

    # Telperion through (upper half), Laurelin fallen (below the equator)
    for pt in lat['telperion']:
        ax.plot(pt['x'], abs(pt['y']), 'o', ms=4.2,
                color=SILVER if pt['silver'] else BLUE, alpha=0.92)
    for pt in lat['laurelin']:
        yy = -abs(pt['y']) - 0.4
        ax.plot([pt['x'], pt['x']], [-0.05, yy], color=RED, lw=0.45, alpha=0.28)
        ax.plot(pt['x'], yy, 'v', ms=3.3, color=RED, alpha=0.5)

    # the accumulated counter-twist, drawn as two short arcs off the +x axis
    ra = lim * 0.30
    for sgn, col in ((+1, BLUE), (-1, RED)):
        arc = np.radians(np.linspace(0, sgn * theta, 60))
        ax.plot(ra * np.cos(arc), ra * np.sin(arc), color=col, lw=2.0, alpha=0.9)
    ax.text(ra * 1.05, 0, f'Θ = {theta:.0f}°', color=GREY, fontsize=9, va='center')

    # RSA-2048 callout
    if k == 11:
        ax.add_patch(plt.Circle((0, 0), lim * 0.62, fill=False, ec=GOLD,
                                lw=1.6, ls='--'))
        ax.text(0, lim * 0.62 + 0.25, 'RSA-2048', color=GOLD, fontsize=11,
                ha='center', va='bottom', fontweight='bold')

    ax.plot(0, 0, 'o', ms=12, color=GOLD)
    ax.set_aspect('equal')
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_xticks([]); ax.set_yticks([])
    return _save(fig, f'plane_{k}_{name}.png')


# ── the strip ─────────────────────────────────────────────────────────────

_TOWER_NAMES = ['ℝ', 'ℂ', 'ℍ', '𝕆', '𝕊', 'T_32', 'T_64', 'T_128', 'T_256',
                'T_512', 'T_1024', 'T_2048', 'T_4096', 'T_8192']


def tower_strip(paths):
    imgs = [plt.imread(p) for p in paths]
    ncol = 7
    nrow = -(-len(imgs) // ncol)               # ceil
    fig, axes = plt.subplots(nrow, ncol, figsize=(3.5 * ncol, 3.7 * nrow))
    axes = np.atleast_1d(axes).ravel()
    for i, ax in enumerate(axes):
        if i < len(imgs):
            ax.imshow(imgs[i]); ax.set_title(_TOWER_NAMES[i], color=FG, fontsize=14)
            for s in ax.spines.values():
                s.set_edgecolor('#33405e')
        else:
            ax.set_visible(False)
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle('The Abrikosov Tree as The Two Trees   —   ℝ → ℂ → ℍ → 𝕆 → 𝕊 → '
                 'T_32 → … → T_8192      (Telperion + / Laurelin −, counter-rotating; '
                 'RSA-2048 at T_2048)',
                 color=FG, fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    return _save(fig, 'two_trees_tower.png')


if __name__ == '__main__':
    outs = [plane_R(), plane_C(), plane_H(), plane_O(), plane_S()]
    outs += [plane_T(k) for k in range(5, 14)]      # T_32 … T_8192
    strip = tower_strip(outs)                        # the tower (14 levels)
    companions = [plane_R_orthogonal(),              # companions to plate 0 —
                  plane_ulam_sphere(),               # not tower levels
                  plane_digit_order()]
    for p in outs + [strip] + companions:
        print('  written:', os.path.relpath(p, os.path.dirname(_HERE)))
