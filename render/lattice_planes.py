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
    strip = tower_strip(outs)
    for p in outs + [strip]:
        print('  written:', os.path.relpath(p, os.path.dirname(_HERE)))
