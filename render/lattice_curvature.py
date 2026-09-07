#!/usr/bin/env python3
"""
lattice_curvature.py — the winding-field curvature over the WHOLE divisor lattice
===============================================================================

Not semiprimes.  ALL interactions: every n, every factorisation n = a·b with
a, b ≥ 2 — prime·prime, prime·composite, composite·composite, coprime or not.

Two spin fields on (ℕ, |):
    J_red  twist   φ = c·ln n   — ADDITIVE, so its holonomy round the elementary
           lattice loop  1 → a → a·b → b → 1  is exactly 0.  Flat connection.
    J_blue winding φ = 2π√n     — NOT additive.  Loop holonomy:
           κ(a,b) = ‖ √(ab) − √a − √b ‖   (distance to the nearest integer).
           This IS the curvature of the winding connection — the interaction of
           the two spins, at every edge of the lattice.

If κ is equidistributed on every slice (by gcd(a,b), by balance, by Ω, by
prime-ness), the winding connection is generically flat-in-measure and there is
no resonance to find anywhere in the multiplicative structure.  If some slice
concentrates near κ = 0, that slice is the resonance.

Output: render/lattice_curvature.png
"""
import os
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
BG = '#07070f'; FG = '#c9d3e6'; GREY = '#7f8db0'
BLUE = '#4aa3ff'; RED = '#ff5566'; GOLD = '#ffcf4a'; SILVER = '#dfe6ff'
CY = '#49d0e0'
plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': BG, 'savefig.facecolor': BG,
    'text.color': FG, 'axes.edgecolor': '#33405e', 'axes.labelcolor': FG,
    'xtick.color': GREY, 'ytick.color': GREY, 'font.size': 10,
})


def spf_sieve(n):
    s = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if s[i] == i:
            for j in range(i * i, n + 1, i):
                if s[j] == j:
                    s[j] = i
    return s


def Omega(m, spf):
    k = 0
    while m > 1:
        m //= spf[m]; k += 1
    return k


def ks_uniform(x):
    """KS distance of x (assumed in [0,0.5]) to Uniform[0,0.5]."""
    x = np.sort(np.asarray(x))
    n = len(x)
    if n == 0:
        return float('nan')
    cdf = np.arange(1, n + 1) / n
    u = x / 0.5
    return float(np.max(np.abs(cdf - u)))


def main():
    NBIG = 120_000
    spf = spf_sieve(NBIG)
    is_prime = [i > 1 and spf[i] == i for i in range(NBIG + 1)]
    Om = np.zeros(NBIG + 1, dtype=np.int8)
    for m in range(2, NBIG + 1):
        Om[m] = Omega(m, spf)

    from math import gcd, isqrt
    kap, g, bal, omsum, aprime, bprime, nn = [], [], [], [], [], [], []
    for n in range(4, NBIG + 1):
        rn = math.sqrt(n)
        a = 2
        while a * a <= n:
            if n % a == 0:
                b = n // a
                k = rn - math.sqrt(a) - math.sqrt(b)
                kap.append(abs(k - round(k)))
                g.append(gcd(a, b))
                bal.append(math.log(b) - math.log(a))         # 0 = balanced
                omsum.append(int(Om[a] + Om[b]))
                aprime.append(is_prime[a]); bprime.append(is_prime[b])
                nn.append(n)
            a += 1
    kap = np.array(kap); g = np.array(g); bal = np.array(bal)
    omsum = np.array(omsum); ap = np.array(aprime); bp = np.array(bprime)
    nn = np.array(nn)
    both_prime = ap & bp
    print(f"{len(kap):,} (a,b) interactions over n = 4..{NBIG}")

    fig = plt.figure(figsize=(15.5, 9))
    gs = fig.add_gridspec(2, 3, hspace=0.42, wspace=0.30,
                          left=0.06, right=0.975, top=0.85, bottom=0.08)
    fig.suptitle('Winding-field curvature over the whole divisor lattice — every interaction n = a·b',
                 color=FG, fontsize=14, x=0.06, ha='left', y=0.965)
    fig.text(0.06, 0.915,
             'κ(a,b) = ‖√(ab) − √a − √b‖ — the holonomy of the J_blue winding field round the '
             'elementary loop 1→a→ab→b→1 (the J_red twist holonomy is 0 by additivity).\n'
             'flat density = 2.0 on [0, 0.5].  concentration near κ = 0 on any slice ⇒ a resonance '
             'there.',
             color=GREY, fontsize=9, va='top')

    def panel(ax, mask, label, color):
        d = kap[mask]
        ax.hist(d, bins=60, density=True, histtype='step', color=color)
        ax.axhline(2.0, color=GREY, ls=':', lw=0.8)
        ax.set_xlim(0, 0.5); ax.set_ylim(0, 3)
        ax.set_title(f'{label}\nn={len(d):,}  median {np.median(d):.3f}  KS {ks_uniform(d):.3f}',
                     color=FG, fontsize=9)
        ax.set_xlabel('κ')

    panel(fig.add_subplot(gs[0, 0]), np.ones(len(kap), bool), 'ALL interactions', BLUE)
    panel(fig.add_subplot(gs[0, 1]), both_prime, 'prime · prime  (coprime)', CY)
    panel(fig.add_subplot(gs[0, 2]), ~ap & ~bp, 'composite · composite', RED)
    panel(fig.add_subplot(gs[1, 0]), g > 1, 'gcd(a,b) > 1  (shared factor)', GOLD)
    panel(fig.add_subplot(gs[1, 1]), np.abs(bal) < 0.2, 'balanced  a ≈ b', '#c58bff')

    # slice by omsum: median κ per Ω(a)+Ω(b)
    axL = fig.add_subplot(gs[1, 2])
    levels = sorted(set(omsum.tolist()))
    med = [np.median(kap[omsum == L]) for L in levels]
    ksv = [ks_uniform(kap[omsum == L]) for L in levels]
    axL.plot(levels, med, 'o-', color=BLUE, label='median κ')
    axL.plot(levels, ksv, 's--', color=GOLD, label='KS vs uniform')
    axL.axhline(0.25, color=GREY, ls=':', lw=0.8)
    axL.set_xlabel('Ω(a) + Ω(b)'); axL.set_ylim(0, 0.32)
    axL.legend(fontsize=8, facecolor=BG, edgecolor='#33405e', labelcolor=FG)
    axL.set_title('κ by total factor count', color=FG, fontsize=9)

    out = os.path.join(_HERE, 'lattice_curvature.png')
    fig.savefig(out, dpi=140); plt.close(fig)

    print("\nslice                         n           median κ   KS(uniform)")
    for lab, m in (("ALL", np.ones(len(kap), bool)),
                   ("prime·prime", both_prime),
                   ("prime·composite", (ap ^ bp)),
                   ("composite·composite", ~ap & ~bp),
                   ("gcd(a,b) > 1", g > 1),
                   ("gcd(a,b) = 1", g == 1),
                   ("balanced a≈b", np.abs(bal) < 0.2),
                   ("very unbalanced", np.abs(bal) > 3.0),
                   ("a·a  (n a square)", (nn == (np.round(np.sqrt(nn)) ** 2).astype(np.int64)) &
                                         (np.abs(bal) < 1e-9))):
        d = kap[m]
        print(f"  {lab:<27} {len(d):>9,}   {np.median(d):>8.4f}   {ks_uniform(d):>8.4f}")
    print("\n  (uniform: median 0.2500, KS -> 0.  a KS well above ~0.02 on a big slice = structure.)")
    print('  written:', os.path.relpath(out, os.path.dirname(_HERE)))


if __name__ == '__main__':
    main()
