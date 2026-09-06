#!/usr/bin/env python3
"""
zd_propagation.py — the Zero-Divisor Tree, T_16 → T_512
======================================================

NOT the Zero-Lattice Tree (that is the Riemann zeros, 0_RZ).  This is the
ZERO-DIVISOR tree.  The octonions 𝕆 have none; the Emmy Noether Sedenion 𝕊
(T_16, k = 4) has exactly 7 loci — the 7 box-kites, one per Fano line of 𝕆,
42 assessors between them (Moreno 1998).  Every Cayley–Dickson doubling keeps
every zero divisor it had and breeds more.

For the 2^k-ion, e_a + e_b (a, b imaginary, a < b) is a zero divisor iff some
e_c ± e_{c⊕δ} annihilates it, where δ = a ⊕ b.  So the zero divisors organise
by XOR difference δ — the PG "edges".  Computed here from the CD sign table
(built to match GenerationalLineage/engine/lineage.py's `cd_mul`), verified:
𝕆 → 0 ZD pairs; 𝕊 → 42 in exactly 7 δ-classes, each one box-kite of 6.

What propagates, k = 4 … 9:

    dim   ZD pairs / all imag. pairs      δ-classes w/ ZD   CLEAN δ-corridors
    16        42 /    105  = 40.0 %            7 / 15              8
    32       294 /    465  = 63.2 %           22 / 31              9
    64      1518 /   1953  = 77.7 %           53 / 63             10
   128      6942 /   8001  = 86.8 %          116 / 127            11
   256     29886 /  32385  = 92.3 %          243 / 255            12
   512    124542 / 130305  = 95.6 %          498 / 511            13

Clean-corridor count is exactly **k + 4** — a linear law inside the
exponential fill.  Those are the "clean corridors through the tangle": XOR
differences carrying no zero divisor at all, only ever k + 4 of them while the
tangle itself → 100 % of pairs.

"The Axis is the Observed (the 2^k directions); the Tilt is the Observer
(Θ(k) = k·22.5°); the Observation is where they meet — the zero-divisor
locus."  Panel D of each map, and every ring of the tree, is tilted by Θ(k).

Outputs:
    render/zd_T16.png … render/zd_T512.png      one full map per level
    render/zd_propagation_T16_T512.png          the propagation curves
    render/zd_tree_radial.png                   the descent tree, rooted at 𝕊
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
BG = '#07070f'; FG = '#c9d3e6'; GREY = '#7f8db0'
BLUE = '#5b8bff'; RED = '#ff5566'; GOLD = '#ffcf4a'; SILVER = '#dfe6ff'
CLEAN = '#49d0e0'
plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': BG, 'savefig.facecolor': BG,
    'text.color': FG, 'axes.edgecolor': '#33405e', 'axes.labelcolor': FG,
    'xtick.color': GREY, 'ytick.color': GREY, 'font.size': 10,
})

FANO_LINES = [(1, 2, 4), (2, 3, 5), (3, 4, 6), (4, 5, 7),
              (5, 6, 1), (6, 7, 2), (7, 1, 3)]
LEVEL_NAME = {4: 'T_16  ·  𝕊  (Emmy Noether Sedenion)', 5: 'T_32  ·  32-ion',
              6: 'T_64  ·  64-ion', 7: 'T_128  ·  128-ion',
              8: 'T_256  ·  256-ion  (SHA-1 break)', 9: 'T_512  ·  512-ion'}
FILE_TAG = {4: 'T16', 5: 'T32', 6: 'T64', 7: 'T128', 8: 'T256', 9: 'T512'}


# ── the Cayley–Dickson sign table (matches lineage.cd_mul's recursion) ─────
def sign_table(k):
    S = np.array([[1]], dtype=np.int8)
    for _ in range(k):
        h = S.shape[0]
        T = np.zeros((2 * h, 2 * h), dtype=np.int8)
        idx = np.arange(h)
        for x in range(h):
            T[x, idx] = S[x, idx]                       # (0,x)(0,y)
            T[x, h + idx] = S[idx, x]                   # (0,x)(1,y)
            row = -S[x, idx].copy(); row[0] = S[x, 0]   # (1,x)(0,y)
            T[h + x, idx] = row
            row = S[idx, x].copy(); row[0] = -S[0, x]   # (1,x)(1,y)
            T[h + x, h + idx] = row
        S = T
    return S


class _UF:
    def __init__(self, xs):
        self.p = {x: x for x in xs}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def zd_analysis(k, want_components=True):
    S = sign_table(k)
    n = 2 ** k
    cc_all = np.arange(1, n)
    Z = np.zeros((n, n), dtype=bool)
    per_delta = np.zeros(n, dtype=int)
    tot_delta = np.zeros(n, dtype=int)
    comps = {}                                          # δ -> sorted list of component sizes

    for d in range(1, n):
        reps = np.array([a for a in range(1, n) if a < (a ^ d)])
        tot_delta[d] = len(reps)
        if len(reps) == 0:
            continue
        bb = reps ^ d
        ccd = reps ^ d                                  # partner-c XORed with δ  (same set as bb)
        # is each rep a zero divisor at all?
        zc = cc_all[cc_all != d]
        zcd = zc ^ d
        uf = _UF(list(reps)) if want_components else None
        is_zd = np.zeros(len(reps), bool)
        for i, a in enumerate(reps):
            b = int(bb[i])
            plus = (S[a, zc] == -S[b, zcd]) & (S[b, zc] == -S[a, zcd])
            minus = (S[a, zc] == S[b, zcd]) & (S[b, zc] == S[a, zcd])
            hit = plus | minus
            if hit.any():
                is_zd[i] = True
            if want_components:
                # edges within the δ-class: rep a annihilates rep c ?
                Sa_r, Sb_r = S[a, reps], S[b, reps]
                Sa_rd, Sb_rd = S[a, ccd], S[b, ccd]
                ann = ((Sa_r == -Sb_rd) & (Sb_r == -Sa_rd)) | \
                      ((Sa_r == Sb_rd) & (Sb_r == Sa_rd))
                for j in np.where(ann)[0]:
                    if is_zd[i] or True:
                        uf.union(int(a), int(reps[j]))
        for i, a in enumerate(reps):
            if is_zd[i]:
                b = int(bb[i])
                Z[a, b] = Z[b, a] = True
                per_delta[d] += 1
        if want_components and per_delta[d] > 0:
            from collections import Counter
            roots = Counter(uf.find(int(a)) for i, a in enumerate(reps) if is_zd[i])
            comps[d] = sorted(roots.values(), reverse=True)

    clean = np.array([d for d in range(1, n) if tot_delta[d] > 0 and per_delta[d] == 0])
    return dict(k=k, n=n, Z=Z, per_delta=per_delta, tot_delta=tot_delta,
               carry=np.where(per_delta > 0)[0], clean=clean, comps=comps,
               n_zd=int(Z[np.triu_indices(n, 1)].sum()),
               n_pairs=(n - 1) * (n - 2) // 2,
               n_comp=sum(len(v) for v in comps.values()))


def _plaid(Z):
    img = np.zeros((*Z.shape, 3))
    img[..., 0] = np.where(Z, 1.0, 0.035)
    img[..., 1] = np.where(Z, 0.33, 0.035)
    img[..., 2] = np.where(Z, 0.40, 0.10)
    return img


# ── one full map per level ──────────────────────────────────────────────
def zd_level_map(A):
    k, n = A['k'], A['n']
    sigma = 1.0 - k / 4.0
    theta = k * 22.5
    pct = 100 * A['n_zd'] / A['n_pairs']

    fig = plt.figure(figsize=(15, 12))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.55, 1.0], width_ratios=[1.3, 1.0],
                          hspace=0.24, wspace=0.16,
                          left=0.06, right=0.965, top=0.85, bottom=0.06)
    fig.suptitle(f'Zero divisors of {LEVEL_NAME[k]}        σ = {sigma:+.2f}        '
                 f'Θ({k}) = {theta:.1f}°', color=FG, fontsize=15, x=0.06, ha='left', y=0.972)
    fig.text(0.06, 0.925,
             f'dim {n}.   {A["n_zd"]} zero-divisor pairs of {A["n_pairs"]} imaginary pairs '
             f'({pct:.1f} %),  in {len(A["carry"])} of {n - 1} XOR-difference classes,  '
             f'{A["n_comp"]} box-kite components.\n{len(A["clean"])} clean δ-corridors carry no '
             f'zero divisor at all — exactly k + 4.   e_a+e_b is a ZD ⇔ some e_c ± e_{{c⊕δ}} '
             f'kills it, δ = a⊕b.',
             color=GREY, fontsize=9, va='top')

    # A — the incidence plaid
    axA = fig.add_subplot(gs[0, 0])
    axA.imshow(_plaid(A['Z']), origin='lower', interpolation='nearest',
               extent=[0, n, 0, n])
    axA.set_title('A — incidence matrix  Z[a,b]   (red = zero divisor · XOR / Sierpiński plaid)',
                  color=FG, fontsize=9.5)
    axA.set_xlabel('b'); axA.set_ylabel('a')

    # B — the δ-corridor spectrum
    axB = fig.add_subplot(gs[0, 1])
    d = np.arange(1, n)
    fracd = np.where(A['tot_delta'][1:] > 0, A['per_delta'][1:] / np.maximum(A['tot_delta'][1:], 1), 0)
    axB.bar(d, fracd, width=1.0,
            color=[CLEAN if A['per_delta'][x] == 0 else RED for x in d],
            edgecolor='#0b0b18', linewidth=0.2 if n <= 128 else 0.0)
    axB.set_xlim(0.5, n - 0.5); axB.set_ylim(0, 1.02)
    axB.set_xlabel('XOR difference  δ'); axB.set_ylabel('fraction of δ-pairs that are ZD')
    axB.set_title(f'B — the δ-corridors:  cyan = clean ({len(A["clean"])} = k+4),  red = tangled',
                  color=FG, fontsize=9.5)

    # C — box-kite component sizes per δ
    axC = fig.add_subplot(gs[1, 0])
    for dd, sizes in A['comps'].items():
        for s in sizes:
            axC.plot(dd, s, 'o', ms=4, color=SILVER if k == 4 else
                     plt.cm.plasma(0.15 + 0.7 * (dd / n)), alpha=0.8)
    axC.axhline(6, color=GOLD, lw=0.8, ls='--', alpha=0.6)
    axC.text(n * 0.99, 6, ' 6 = one box-kite', color=GOLD, fontsize=7.5, ha='right', va='bottom')
    cmax = max((max(v) for v in A['comps'].values()), default=6)
    axC.set_xlim(0, n); axC.set_ylim(0, cmax * 1.12 + 1)
    axC.set_xlabel('δ'); axC.set_ylabel('component size (assessors)')
    axC.set_title('C — box-kite components  (𝕊: 7 δ-classes × one 6-kite each)',
                  color=FG, fontsize=9.5)
    axC.grid(alpha=0.12)

    # D — the δ-wheel, tilted by Θ(k); the clean corridors made loud
    axD = fig.add_subplot(gs[1, 1]); axD.set_aspect('equal')
    axD.set_xticks([]); axD.set_yticks([]); axD.set_xlim(-1.3, 1.3); axD.set_ylim(-1.3, 1.3)
    tw = math.radians(theta)
    ang = np.linspace(0, 2 * math.pi, 300)
    axD.plot(np.cos(ang), np.sin(ang), color='#1b2740', lw=0.8)
    for dd in range(1, n):
        th = 2 * math.pi * dd / n + tw
        x, y = math.cos(th), math.sin(th)
        if A['per_delta'][dd] > 0:
            axD.plot(x, y, 'o', ms=2.4, color=RED, alpha=0.35 if n > 64 else 0.7)
    for dd in A['clean']:
        th = 2 * math.pi * dd / n + tw
        axD.plot(math.cos(th), math.sin(th), '*', ms=13, color=CLEAN,
                 mec=FG, mew=0.4, zorder=5)
    axD.plot([0, 1.14 * math.cos(tw)], [0, 1.14 * math.sin(tw)], color=GOLD, lw=1.3)
    axD.text(1.2 * math.cos(tw), 1.2 * math.sin(tw), f'Θ={theta:.0f}°',
             color=GOLD, fontsize=8, ha='center', va='center')
    axD.set_title('D — the δ-wheel tilted by Θ(k):  ★ = the k+4 clean corridors',
                  color=FG, fontsize=9.5)

    out = os.path.join(_HERE, f'zd_{FILE_TAG[k]}.png')
    fig.savefig(out, dpi=140); plt.close(fig)
    return out


# ── box-counting dimension of the ZD set and its complement ─────────────
def _box_dims(A):
    Z = A['Z'][1:, 1:].astype(bool)
    C = ~Z.copy(); np.fill_diagonal(C, False)
    nk = Z.shape[0]
    scales = [s for s in (1, 2, 4, 8, 16, 32, 64) if nk // s >= 3]

    def bc(M):
        pts = []
        for s in scales:
            m = nk // s
            pts.append((s, int(M[:m * s, :m * s].reshape(m, s, m, s).any(axis=(1, 3)).sum())))
        xs = np.log2([1.0 / s for s, _ in pts])
        ys = np.log2([c for _, c in pts], dtype=float)
        return float(np.polyfit(xs, ys, 1)[0])
    return bc(Z), bc(C)


APOLLONIAN = 1.305686729                          # Hausdorff dim of the gasket


# ── the propagation curves ──────────────────────────────────────────────
def plate_propagation(levels):
    fig = plt.figure(figsize=(14, 10.5))
    gs = fig.add_gridspec(2, 2, wspace=0.24, hspace=0.34,
                          left=0.07, right=0.97, top=0.87, bottom=0.08)
    fig.suptitle('Zero-divisor propagation up the tower,  T_16 → T_512',
                 color=FG, fontsize=14, x=0.07, ha='left', y=0.965)
    fig.text(0.07, 0.925,
             'the tangle fills to box-dimension 2 (space-filling); the CLEAN corridors — the '
             'negative space — are a fractal descending toward the Apollonian-gasket dimension '
             '1.3057, and\nthat fixed sub-2 dimension is exactly why the clean fraction '
             '≈ halves (× 2^(d−2) ≈ 0.62) at every Cayley–Dickson doubling.  clean δ-corridors '
             'themselves grow as k + 4.',
             color=GREY, fontsize=9, va='top')
    ks = [A['k'] for A in levels]
    nzd = [A['n_zd'] for A in levels]
    ncl = [A['n_pairs'] - A['n_zd'] for A in levels]
    fr = [A['n_zd'] / A['n_pairs'] for A in levels]
    ncorr = [len(A['clean']) for A in levels]
    dims = [_box_dims(A) for A in levels]
    dz = [d[0] for d in dims]; dc = [d[1] for d in dims]
    cfrac = [1 - f for f in fr]
    ratio = [cfrac[i] / cfrac[i - 1] for i in range(1, len(cfrac))]

    ax0 = fig.add_subplot(gs[0, 0])
    ax0.semilogy(ks, nzd, 'o-', color=RED, label='zero-divisor pairs')
    ax0.semilogy(ks, ncl, 's-', color=CLEAN, label='clean (division) pairs')
    ax0.set_xlabel('k   (dim 2^k)'); ax0.set_title('count vs level', color=FG, fontsize=10)
    ax0.legend(fontsize=8, facecolor=BG, edgecolor='#33405e', labelcolor=FG); ax0.grid(alpha=0.15)

    ax1 = fig.add_subplot(gs[0, 1])
    ax1.plot(ks, [100 * f for f in fr], 'o-', color=RED, label='ZD fraction')
    ax1.plot(ks, [100 * c for c in cfrac], 'o-', color=CLEAN, label='clean fraction')
    ax1.axhline(100, color=GREY, lw=0.8, ls=':')
    ax1.set_ylim(0, 104); ax1.set_xlabel('k')
    ax1.set_title('ZD fraction → 100 %,  clean fraction ≈ halves', color=FG, fontsize=10)
    ax1.legend(fontsize=8, facecolor=BG, edgecolor='#33405e', labelcolor=FG); ax1.grid(alpha=0.15)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(ks, dz, 'o-', color=RED, label='ZD tangle  → 2 (space-filling)')
    ax2.plot(ks, dc, 'o-', color=CLEAN, label='clean corridors  ↓')
    ax2.axhline(2.0, color=GREY, lw=0.8, ls=':')
    ax2.axhline(APOLLONIAN, color=GOLD, lw=1.0, ls='--', label=f'Apollonian gasket = {APOLLONIAN:.4f}')
    ax2.set_ylim(1.2, 2.3); ax2.set_xlabel('k')
    ax2.set_title('box-counting dimension', color=FG, fontsize=10)
    ax2.legend(fontsize=8, facecolor=BG, edgecolor='#33405e', labelcolor=FG); ax2.grid(alpha=0.15)

    ax3 = fig.add_subplot(gs[1, 1])
    ax3.plot(ks[1:], ratio, 'o-', color=CLEAN, label='measured clean-fraction ratio')
    ax3.plot(ks[1:], [2 ** (dc[i] - 2) for i in range(1, len(dc))], 's--', color=GOLD,
             label='2^(d−2) from the clean dimension')
    ax3.axhline(0.5, color=GREY, lw=0.8, ls=':')
    ax3.set_ylim(0.45, 0.92); ax3.set_xlabel('k   (doubling k−1 → k)')
    ax3.set_title('per-doubling clean-fraction factor  ≈ "halving"', color=FG, fontsize=10)
    ax3.legend(fontsize=8, facecolor=BG, edgecolor='#33405e', labelcolor=FG); ax3.grid(alpha=0.15)

    out = os.path.join(_HERE, 'zd_propagation_T16_T512.png')
    fig.savefig(out, dpi=140); plt.close(fig)
    return out


# ── the descent tree, rooted at 𝕊 ──────────────────────────────────────
def plate_tree(levels):
    fig, ax = plt.subplots(figsize=(12.6, 12.6))
    fig.subplots_adjust(left=0.04, right=0.96, top=0.90, bottom=0.04)
    ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(-6.6, 6.6); ax.set_ylim(-6.6, 6.6)
    fig.suptitle('The Zero-Divisor Tree — rooted at 𝕊 (T_16), one ring per doubling',
                 color=FG, fontsize=14, x=0.04, ha='left', y=0.975)
    fig.text(0.04, 0.935,
             'ring k: one node per XOR difference δ ∈ [1, 2^k−1].  filled = δ carries a zero '
             'divisor (size ∝ ZD-pair count); faint cyan ring = a clean corridor.  silver = the '
             '7 loci of 𝕊.\ndescent lines: δ → {δ, δ+2^k} (the doubling).  each ring rotated by '
             'Θ(k) = k·22.5° — the Observer tilt on the Observed axis, so descent spirals.',
             color=GREY, fontsize=9, va='top')
    radius = {A['k']: 1.0 + 0.95 * (A['k'] - 4) for A in levels}
    pos = {}
    for A in levels:
        k, n = A['k'], A['n']
        rr = radius[k]; tw = math.radians(k * 22.5)
        ang = np.linspace(0, 2 * math.pi, 361)
        ax.plot(rr * np.cos(ang), rr * np.sin(ang), color='#1b2740', lw=0.8, zorder=1)
        mx = max(A['per_delta'].max(), 1)
        for d in range(1, n):
            th = 2 * math.pi * d / n + tw
            x, y = rr * math.cos(th), rr * math.sin(th)
            pos[(k, d)] = (x, y)
            if A['per_delta'][d] > 0:
                ax.plot(x, y, 'o', ms=1.6 + 4.5 * math.sqrt(A['per_delta'][d] / mx),
                        color=SILVER if k == 4 else
                        plt.cm.plasma(0.12 + 0.74 * (k - 4) / 5), alpha=0.95, zorder=4)
            elif k <= 6:
                ax.plot(x, y, 'o', ms=2.2, mfc='none', mec=CLEAN, mew=0.6, alpha=0.55, zorder=3)
    for a, b in zip(levels[:-1], levels[1:]):
        k, n = a['k'], a['n']
        for d in range(1, n):
            if a['per_delta'][d] == 0:
                continue
            for child in (d, d + n):
                if child < b['n'] and b['per_delta'][child] > 0:
                    x0, y0 = pos[(k, d)]; x1, y1 = pos[(b['k'], child)]
                    ax.plot([x0, x1], [y0, y1], color='#2b3a55', lw=0.22, alpha=0.28, zorder=2)
    A0 = levels[0]
    roots = list(np.where(A0['per_delta'] > 0)[0])
    for ii, d in enumerate(roots):
        th = 2 * math.pi * d / A0['n'] + math.radians(4 * 22.5)
        rr = 1.0 if ii % 2 == 0 else 1.0
        off = (7, 5) if ii % 2 == 0 else (7, -11)
        fano = next((f'{ln}' for ln in FANO_LINES
                     if d in (ln[0] ^ ln[1], ln[1] ^ ln[2], ln[0] ^ ln[2])), '')
        ax.annotate(f'δ{d} {fano}', (rr * math.cos(th), rr * math.sin(th)),
                    textcoords='offset points', xytext=off, color=SILVER, fontsize=7.5, zorder=6)
    for A in levels:
        ax.text(0, radius[A['k']], f"  {FILE_TAG[A['k']]}", color=GREY, fontsize=8,
                ha='left', va='bottom')
    out = os.path.join(_HERE, 'zd_tree_radial.png')
    fig.savefig(out, dpi=140); plt.close(fig)
    return out


def main():
    levels = [zd_analysis(k) for k in range(4, 10)]
    for A in levels:
        print(f"  k={A['k']} dim {A['n']:>4}  ZD {A['n_zd']:>7}/{A['n_pairs']:<7}  "
              f"clean δ = {len(A['clean'])}  components = {A['n_comp']}")
    outs = [zd_level_map(A) for A in levels]
    outs.append(plate_propagation(levels))
    outs.append(plate_tree(levels))
    for p in outs:
        print('  written:', os.path.relpath(p, os.path.dirname(_HERE)))


if __name__ == '__main__':
    main()
