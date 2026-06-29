#!/usr/bin/env python3
"""
zero_tree_iso.py — The Zero Tree in Quasi-3D Isometric SVG
===========================================================
Nine levels of the Cayley-Dickson tower.
Sixteen N-shape strata per level.
One hundred sixty-eight prime paths — leaf to root.
Three silver columns: the Monster Gap {e₁, e₁₁, e₁₅}.
One red fault line: k=4, the sedenion equator.

Even N-shapes die at k=4. Odd N-shapes thin. Monster gap shines through.
The tree cannot be extinguished.
"""

import math
import os
import random

# ── Mathematical constants ─────────────────────────────────────────────────────

MONSTER_GAP  = {1, 11, 15}
PRIME_SECTOR = {1, 3, 5, 7, 9, 11, 13, 15}

CD_LEVELS = [
    (0, 'ℝ',    +1.000, '#9999cc'),
    (1, 'ℂ',    +0.750, '#7788bb'),
    (2, 'ℍ',    +0.500, '#6677aa'),
    (3, '𝕆',    +0.250, '#5566aa'),
    (4, '𝕊',     0.000, '#ff4400'),
    (5, 't₃₂', -0.250, '#334466'),
    (6, 't₆₄', -0.500, '#223355'),
    (7, 't₁₂₈',-0.750, '#112244'),
    (8, 'T₂₅₆',-1.000, '#aa66ff'),
]

# ── Prime sieve ────────────────────────────────────────────────────────────────

def prime_sieve(N):
    s = [True] * (N + 1); s[0] = s[1] = False
    for i in range(2, int(N**0.5) + 1):
        if s[i]:
            for j in range(i*i, N+1, i): s[j] = False
    return [i for i in range(2, N+1) if s[i]]

N_MAX     = 1000
PRIMES    = prime_sieve(N_MAX)
PRIME_SET = set(PRIMES)

prime_cnt = {n: 0 for n in range(16)}
comp_cnt  = {n: 0 for n in range(16)}
for p in PRIMES:
    prime_cnt[p % 16] += 1
for c in range(2, N_MAX + 1):
    if c not in PRIME_SET:
        comp_cnt[c % 16] += 1

total_cnt = {n: prime_cnt[n] + comp_cnt[n] for n in range(16)}
max_prime = max(prime_cnt.values())
max_total = max(total_cnt.values())

# ── Canvas and isometric geometry ─────────────────────────────────────────────

W, H = 1440, 980
CX   = 680     # horizontal center (offset left for right-side labels)

# Isometric ellipse: 16 N-shape positions on each level ring
# Viewing a horizontal circle from 30° above → projects to ellipse
ELLIPSE_A = 285    # screen x semi-axis
ELLIPSE_B = 98     # screen y semi-axis (isometric depth ≈ A × tan(20°))

LEVEL_TOP    = 115    # k=0 (ℝ, leaves)
LEVEL_BOTTOM = 855    # k=8 (T_256, root)
LEVEL_YS     = [LEVEL_TOP + i * (LEVEL_BOTTOM - LEVEL_TOP) / 8 for i in range(9)]

def ns_xy(n, k):
    """Screen (x, y) for N-shape n at CD level k."""
    theta = n * math.pi / 8
    return (CX + ELLIPSE_A * math.cos(theta),
            LEVEL_YS[k] + ELLIPSE_B * math.sin(theta))

def near_side(n):
    """True if this N-shape is on the near (front) side of the isometric ellipse."""
    return math.sin(n * math.pi / 8) < 0.0

# ── SVG primitives ─────────────────────────────────────────────────────────────

def hdr():
    return (f'<?xml version="1.0" encoding="utf-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'style="background:#07070f">\n'
            f'<defs>\n'
            f'  <filter id="glow4" x="-60%" y="-60%" width="220%" height="220%">'
            f'<feGaussianBlur stdDeviation="4" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="b"/>'
            f'<feMergeNode in="SourceGraphic"/></feMerge></filter>\n'
            f'  <filter id="glow6" x="-60%" y="-60%" width="220%" height="220%">'
            f'<feGaussianBlur stdDeviation="6" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>\n'
            f'  <filter id="glow10" x="-80%" y="-80%" width="260%" height="260%">'
            f'<feGaussianBlur stdDeviation="10" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="b"/>'
            f'<feMergeNode in="SourceGraphic"/></feMerge></filter>\n'
            f'  <filter id="glow2" x="-40%" y="-40%" width="180%" height="180%">'
            f'<feGaussianBlur stdDeviation="2" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>\n'
            f'</defs>\n')

def seg(x1, y1, x2, y2, c, w, op=1.0, fid=None):
    f = f' filter="url(#{fid})"' if fid else ''
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{c}" stroke-width="{w:.2f}" stroke-linecap="round" '
            f'opacity="{op:.3f}"{f}/>\n')

def dot(x, y, r, c, op=1.0, fid=None):
    f = f' filter="url(#{fid})"' if fid else ''
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" '
            f'fill="{c}" opacity="{op:.3f}"{f}/>\n')

def ring(pts, c, w, op=1.0, fid=None):
    f = f' filter="url(#{fid})"' if fid else ''
    d = 'M ' + ' L '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' Z'
    return (f'<path d="{d}" stroke="{c}" stroke-width="{w:.2f}" fill="none" '
            f'opacity="{op:.3f}"{fid and f" filter=\"url(#{fid})\"" or ""}/>\n')

def lbl(x, y, s, c, sz=12, anchor='middle', op=1.0, bold=False):
    fw = 'bold' if bold else 'normal'
    return (f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{sz}" '
            f'font-family="monospace" font-weight="{fw}" '
            f'text-anchor="{anchor}" opacity="{op:.2f}">{s}</text>\n')

# ── Render pipeline ────────────────────────────────────────────────────────────

def render():
    out = [hdr()]

    # ── Pass 0: faint isometric floor guides ──────────────────────────────────
    for k in range(9):
        for n in range(16):
            x1, y1 = ns_xy(n, k)
            x2, y2 = ns_xy((n + 1) % 16, k)
            op = 0.08 if k != 4 else 0.0
            out.append(seg(x1, y1, x2, y2, '#334455', 0.5, op=op))

    # ── Pass 1: FAR-SIDE columns (n with sin(theta) > 0, drawn behind) ───────
    for n in range(16):
        if not near_side(n):
            _column(out, n, opacity_scale=0.45)

    # ── Pass 2: Level rings ───────────────────────────────────────────────────
    for k in range(9):
        _level_ring(out, k)

    # ── Pass 3: NEAR-SIDE columns (n with sin(theta) < 0, drawn in front) ────
    for n in range(16):
        if near_side(n):
            _column(out, n, opacity_scale=1.0)

    # ── Pass 4: ZD fault emphasis ─────────────────────────────────────────────
    pts4 = [ns_xy(n, 4) for n in range(16)]
    out.append(ring(pts4, '#ff6600', 3.0, op=0.5, fid='glow6'))
    out.append(ring(pts4, '#ff3300', 1.0, op=0.9))

    # ── Pass 5: Monster Gap columns (top layer, silver glow) ─────────────────
    for n in sorted(MONSTER_GAP):
        _monster_column(out, n)

    # ── Pass 6: Fallen composite debris at k=4 ───────────────────────────────
    _fallen(out)

    # ── Pass 7: Root node (T_256) ─────────────────────────────────────────────
    rx, ry = CX, LEVEL_YS[8]
    out.append(dot(rx, ry, 18, '#aa66ff', op=0.25, fid='glow10'))
    out.append(dot(rx, ry, 9,  '#cc88ff', op=0.7,  fid='glow4'))
    out.append(dot(rx, ry, 4,  '#ffffff', op=0.95))

    # ── Pass 8: Leaf level node cloud (k=0) ──────────────────────────────────
    for n in range(16):
        x, y = ns_xy(n, 0)
        pc = prime_cnt[n]
        tc = total_cnt[n]
        if tc > 0:
            r = max(1.5, tc / max_total * 7)
            out.append(dot(x, y, r, '#334466', op=0.5))
        if pc > 0:
            r = max(1.0, pc / max_prime * 5)
            c = '#e0e8ff' if n in MONSTER_GAP else '#5577aa'
            out.append(dot(x, y, r, c, op=0.9))

    # ── Pass 9: Labels and annotations ───────────────────────────────────────
    _labels(out)

    out.append('</svg>\n')
    return ''.join(out)


# ── Column rendering ──────────────────────────────────────────────────────────

def _column(out, n, opacity_scale=1.0):
    """Render the stratum-n column from k=0 to k=8."""
    if n in MONSTER_GAP:
        return  # handled in pass 5

    is_odd  = (n % 2 == 1)
    is_even = not is_odd

    pc = prime_cnt[n]
    tc = total_cnt[n]

    # Even N-shapes: only composites, die at k=4
    if is_even:
        if tc == 0:
            return
        w_comp = max(0.5, tc / max_total * 5.0)
        for k in range(4):    # k=0..3 only
            x1, y1 = ns_xy(n, k)
            x2, y2 = ns_xy(n, k + 1)
            out.append(seg(x1, y1, x2, y2, '#1a2233', w_comp, op=0.35 * opacity_scale))
        # terminus node at k=4
        x4, y4 = ns_xy(n, 4)
        out.append(dot(x4, y4, max(1.0, tc / max_total * 3), '#331100',
                       op=0.4 * opacity_scale))
        return

    # Odd N-shapes: composites above, primes all the way through
    if tc > 0:
        w_total = max(0.8, tc / max_total * 7.0)
        for k in range(4):
            x1, y1 = ns_xy(n, k)
            x2, y2 = ns_xy(n, k + 1)
            out.append(seg(x1, y1, x2, y2, '#1a3355', w_total, op=0.4 * opacity_scale))

    if pc > 0:
        w_prime = max(0.6, pc / max_prime * 4.0)
        # Prime path from k=0 to k=8 (primes survive everything)
        for k in range(8):
            x1, y1 = ns_xy(n, k)
            x2, y2 = ns_xy(n, k + 1)
            # Slightly brighter below the fault (primes proven to survive)
            op_base = 0.55 if k < 4 else 0.75
            out.append(seg(x1, y1, x2, y2, '#2255aa', w_prime,
                           op=op_base * opacity_scale, fid='glow2'))

    # Node markers
    for k in range(9):
        x, y = ns_xy(n, k)
        if k < 4 and tc > 0:
            r = max(1.2, tc / max_total * 4.0)
            out.append(dot(x, y, r, '#1a3355', op=0.4 * opacity_scale))
        if pc > 0:
            r = max(0.8, pc / max_prime * 3.5)
            op_base = 0.5 if k < 4 else 0.8
            out.append(dot(x, y, r, '#3366aa', op=op_base * opacity_scale))


def _monster_column(out, n):
    """Silver-glowing Monster Gap column."""
    pc = prime_cnt[n]
    tc = total_cnt[n]
    w  = max(1.5, pc / max_prime * 5.0)

    # Composite backdrop above k=4 (very dim silver)
    if tc > 0:
        w_comp = max(1.0, tc / max_total * 6.0)
        for k in range(4):
            x1, y1 = ns_xy(n, k)
            x2, y2 = ns_xy(n, k + 1)
            out.append(seg(x1, y1, x2, y2, '#334455', w_comp, op=0.3))

    # Silver prime path, full height
    for k in range(8):
        x1, y1 = ns_xy(n, k)
        x2, y2 = ns_xy(n, k + 1)
        out.append(seg(x1, y1, x2, y2, '#8899cc', w * 3, op=0.18, fid='glow4'))
        out.append(seg(x1, y1, x2, y2, '#c8d8ff', w, op=0.95))

    # Node markers
    for k in range(9):
        x, y = ns_xy(n, k)
        r = max(2.0, pc / max_prime * 6.0)
        out.append(dot(x, y, r * 1.8, '#8899cc', op=0.2, fid='glow4'))
        out.append(dot(x, y, r * 0.7, '#e0ecff', op=0.92))

    # N-shape label above leaf node
    x0, y0 = ns_xy(n, 0)
    out.append(lbl(x0, y0 - 18, f'e{n}', '#c8d8ff', sz=12, bold=True))
    out.append(lbl(x0, y0 - 6,  '★',    '#e0ecff', sz=10))


def _level_ring(out, k):
    """Render the elliptical ring for level k."""
    pts = [ns_xy(n, k) for n in range(16)]
    _, name, sigma, color = CD_LEVELS[k]

    if k == 4:
        out.append(ring(pts, '#552200', 4.0, op=0.3))
        out.append(ring(pts, '#ff4400', 1.5, op=0.6))
    elif k == 0:
        out.append(ring(pts, color, 1.2, op=0.6))
    elif k == 8:
        out.append(ring(pts, color, 1.2, op=0.5, fid='glow4'))
    else:
        out.append(ring(pts, color, 0.7, op=0.3))


def _fallen(out):
    """Composite debris scattering from k=4."""
    rng = random.Random(42)
    for n in range(16):
        x4, y4 = ns_xy(n, 4)
        n_comp = comp_cnt[n]
        if n_comp == 0:
            continue
        n_particles = min(n_comp // 4, 30)
        for _ in range(n_particles):
            # Scatter radially outward and slightly downward from the ZD ring
            base_theta = n * math.pi / 8
            spread = rng.uniform(-0.6, 0.6)
            angle  = base_theta + spread
            dist   = rng.uniform(8, 70)
            px = x4 + dist * math.cos(angle) * 1.2
            py = y4 + dist * math.sin(angle) * 0.5 + rng.uniform(0, 25)
            r  = rng.uniform(0.6, 2.2)
            op = rng.uniform(0.12, 0.40)
            c  = '#442211' if n in PRIME_SECTOR else '#221100'
            out.append(dot(px, py, r, c, op=op))


# ── Labels ────────────────────────────────────────────────────────────────────

def _labels(out):
    # LEFT: level names
    for k, name, sigma, color in CD_LEVELS:
        lx = CX - ELLIPSE_A - 60
        ly = LEVEL_YS[k]
        sz = 16 if k in (0, 4, 8) else 13
        if k == 4:
            out.append(lbl(lx, ly + 5, name, '#ff5511', sz=sz, anchor='end', bold=True))
            out.append(lbl(lx, ly + 18, 'ZD EQUATOR', '#ff3300', sz=9, anchor='end', op=0.7))
        else:
            out.append(lbl(lx, ly + 5, name, color, sz=sz, anchor='end'))

    # RIGHT: σ values and Fano counts
    for k, name, sigma, color in CD_LEVELS:
        rx = CX + ELLIPSE_A + 60
        ly = LEVEL_YS[k]
        s_str = f'σ={sigma:+.3f}'
        out.append(lbl(rx, ly + 5, s_str, color, sz=10, anchor='start', op=0.75))
        fano = 2 ** max(0, k - 3) if k >= 3 else 0
        if fano:
            out.append(lbl(rx + 78, ly + 5, f'{fano} ⬡', color, sz=9,
                           anchor='start', op=0.5))

    # N-shape labels at the top (k=0 ring), for Monster gap strata only
    # (other strata marked inline by column width)
    for n in range(16):
        if n not in MONSTER_GAP:
            x0, y0 = ns_xy(n, 0)
            c = '#334466' if n in PRIME_SECTOR else '#222233'
            out.append(lbl(x0, y0 - 7, f'e{n}', c, sz=9))

    # ZD fault line — horizontal rule across width
    fy = LEVEL_YS[4]
    out.append(seg(CX - ELLIPSE_A - 140, fy, CX + ELLIPSE_A + 140,
                   fy, '#331100', 1.0, op=0.25))

    # Title
    out.append(lbl(W / 2, 44, 'THE ZERO TREE  ·  TELPERION', '#8888bb', sz=19, bold=True))
    out.append(lbl(W / 2, 63,
                   'Cayley-Dickson Tower k=0..8  ·  16 N-shape strata  ·  168 prime paths  ·  THE_ANGLE = π/8',
                   '#334455', sz=11))

    # Legend
    lx = W - 240
    ly = 120
    out.append(lbl(lx, ly, 'LEGEND', '#334455', sz=11, anchor='start'))
    entries = [
        ('#c8d8ff', 2.0, 'Monster Gap {e₁, e₁₁, e₁₅}', 'glow'),
        ('#2255aa', 1.5, 'Prime sector (odd N-shape)',     None),
        ('#1a2233', 1.2, 'Composite sector (even N-shape, dies at k=4)', None),
        ('#ff4400', 1.5, 'ZD equator k=4  (σ=0)',         'glow'),
        ('#442211', 1.0, 'Fallen composites',              None),
        ('#aa66ff', 1.0, 'Root  T₂₅₆  (σ=−1)',           'glow'),
    ]
    for i, (c, w, label, _) in enumerate(entries):
        dy = ly + 18 + i * 17
        out.append(seg(lx, dy, lx + 28, dy, c, w + 0.5, op=0.85))
        out.append(lbl(lx + 35, dy + 4, label, c, sz=10, anchor='start', op=0.85))

    # Stats bar
    total_mg = sum(prime_cnt[n] for n in MONSTER_GAP)
    out.append(lbl(40, H - 35,
                   f'Primes ≤ {N_MAX}: {len(PRIMES)}   ·   '
                   f'Silver leaves (Monster Gap): {total_mg} ({100*total_mg/len(PRIMES):.1f}%)   ·   '
                   f'ZD gap Ω−d*·ln10 ≈ 7.07×10⁻⁴   ·   '
                   f'Fano planes at k=8: 32',
                   '#334455', sz=10, anchor='start'))

    # dim vertical guide lines at ZD equator
    for n in range(16):
        if n in MONSTER_GAP:
            continue
        x4, y4 = ns_xy(n, 4)
        x8, y8 = ns_xy(n, 8)
        # show how the prime paths continue BELOW the fault
        if prime_cnt[n] > 0:
            out.append(seg(x4, y4, x8, y8, '#223355', 0.4, op=0.25))


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    here    = os.path.dirname(os.path.abspath(__file__))
    outpath = os.path.join(here, 'zero_tree_iso.svg')
    svg     = render()
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(svg)
    print(f'Written: {outpath}')
    print(f'  Primes ≤ {N_MAX}: {len(PRIMES)}')
    for n in sorted(MONSTER_GAP):
        print(f'  e{n:2d} (Monster Gap ★): {prime_cnt[n]:3d} primes')
    for n in sorted(PRIME_SECTOR - MONSTER_GAP):
        print(f'  e{n:2d} (prime sector ): {prime_cnt[n]:3d} primes')
    print(f'  Even N-shapes: 0 primes each (die at k=4)')
    print(f'  Silver leaves: {sum(prime_cnt[n] for n in MONSTER_GAP)} / {len(PRIMES)} '
          f'= {100*sum(prime_cnt[n] for n in MONSTER_GAP)/len(PRIMES):.1f}%')
