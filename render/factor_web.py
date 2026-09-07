#!/usr/bin/env python3
"""
factor_web.py — every number wired to its factors, two colours
=============================================================

Goal: ALL factors of ANY number — a general factoring substrate, not RSA.

Every integer m sits on the Sacks/Ulam spiral in native space:
    P(m) = ( ln m · cos 2π√m ,  ln m · sin 2π√m )
The Scale ln m is the Contractor/Dilator — the radius IS the SCALE operator.

Two edges, per composite n and prime factor p | n:

    RED  — EXTINCTION : one chord  P(n) → P(p).  Decomposition jumps straight
           to the atom.  The deductive sieve — a single pass, the geodesic, FREE.
    BLUE — REBIRTH    : the STEM  p → p·q₁ → p·q₁q₂ → … → n, a polyline through
           real integers, the other factors multiplied back in REVERSE of the
           extinction order.  A path through waypoints, always ≥ its chord —
           the cost of emergence (θ→β).

Opposite of extinction, mathematically = **generation**.  In Dirichlet
convolution the Möbius function μ (sieve / extinction) is the inverse of the
constant 𝟙 (count every way up / rebirth):  μ ∗ 𝟙 = ε.  Extinction flows to
the atoms (primes are fixed points); rebirth flows from the unit (1 is the
source).  Sink vs source — winter vs spring.

Toroidal: a fallen (negative) leaf, run again through negative-only products,
(−p)(−q) = +n, becomes a leaf again — a full 2π winding (full turn ⇔ composite,
the range-check).  RED (radial, contract, cos/standing) ⊥ BLUE (tangential,
wind, sin/travelling) is the E ⊥ B quadrature; Poynting E×B points up the tower.

Output: render/factor_web.png
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
plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': BG, 'savefig.facecolor': BG,
    'text.color': FG, 'axes.edgecolor': '#33405e', 'axes.labelcolor': FG,
    'xtick.color': GREY, 'ytick.color': GREY, 'font.size': 10,
})


def sieve_spf(n):
    spf = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


def factor_multiset(m, spf):
    out = []
    while m > 1:
        p = spf[m]; out.append(p); m //= p
    return out                                    # ascending (Eratosthenes order)


def P(m):
    r = math.log(m)
    a = 2 * math.pi * math.sqrt(m)
    return r * math.cos(a), r * math.sin(a)


def rebirth_stem(p, fac):
    """p, then the OTHER factors multiplied back in reverse extinction order."""
    rest = sorted(fac, reverse=True)
    rest.remove(p)                                # drop one copy of p
    chain, cur = [p], p
    for q in rest:
        cur *= q; chain.append(cur)
    return chain                                  # ends at n


def polyline_len(chain):
    pts = [P(m) for m in chain]
    return sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
               for i in range(len(pts) - 1)), pts


def main():
    NBIG = 6000
    NDRAW = 500
    spf = sieve_spf(NBIG)
    is_prime = [i > 1 and spf[i] == i for i in range(NBIG + 1)]

    rec = []                                      # n, p, red, blue, Omega
    red_deg = np.zeros(NBIG + 1)                   # m as a prime factor of how many n
    blue_deg = np.zeros(NBIG + 1)                  # m as a rebirth-stem waypoint of how many (n,p)
    for n in range(4, NBIG + 1):
        if is_prime[n]:
            continue
        fac = factor_multiset(n, spf)
        Om = len(fac)
        for p in set(fac):
            xn, yn = P(n); xp, yp = P(p)
            red = math.hypot(xn - xp, yn - yp)
            stem = rebirth_stem(p, fac)
            blue, _ = polyline_len(stem)
            rec.append((n, p, red, blue, Om))
            red_deg[p] += 1
            for w in stem[1:-1]:                   # only the intermediate products (hubs)
                blue_deg[w] += 1
    rec = np.array(rec, float)
    ratio = rec[:, 3] / np.maximum(rec[:, 2], 1e-9)

    fig = plt.figure(figsize=(15.5, 8.4))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.12, 1.0], wspace=0.16,
                          left=0.035, right=0.975, top=0.83, bottom=0.10)
    fig.suptitle('The factor web — every number wired to its factors:  red = extinction, blue = rebirth',
                 color=FG, fontsize=14, x=0.035, ha='left', y=0.965)
    fig.text(0.035, 0.915,
             'Sacks spiral, radius = ln n (The Scale, the Contractor/Dilator).  RED = one chord n→p '
             '(decomposition jumps to the atom).  BLUE = the stem p→p·q₁→…→n through real integers '
             '(rebirth\nwinds the other factors back in — a path through waypoints, always longer).  '
             f'web drawn for n ≤ {NDRAW}; distances measured over 2..{NBIG}.',
             color=GREY, fontsize=9, va='top')

    # ── A : the web ───────────────────────────────────────────────────
    axA = fig.add_subplot(gs[0, 0]); axA.set_aspect('equal')
    axA.set_xticks([]); axA.set_yticks([])
    for n in range(4, NDRAW + 1):
        if is_prime[n]:
            continue
        fac = factor_multiset(n, spf); xn, yn = P(n)
        for p in set(fac):
            xp, yp = P(p)
            axA.plot([xn, xp], [yn, yp], color=RED, lw=0.35, alpha=0.5, zorder=2)
            _, pts = polyline_len(rebirth_stem(p, fac))
            axA.plot([q[0] for q in pts], [q[1] for q in pts],
                     color=BLUE, lw=0.5, alpha=0.5, zorder=3)
    for m in range(2, NDRAW + 1):
        x, y = P(m)
        axA.plot(x, y, 'o', ms=3.4 if is_prime[m] else 2.0,
                 color=SILVER if is_prime[m] else GREY,
                 alpha=0.95 if is_prime[m] else 0.55, zorder=5)
    axA.plot(0, 0, 'o', ms=7, color=GOLD, zorder=6)
    axA.set_title(f'A — the web (n ≤ {NDRAW})   silver = prime  ·  grey = composite',
                  color=FG, fontsize=10)

    # ── B : the web's HUBS — who is on the most factor-edges ─────────
    axB = fig.add_subplot(gs[0, 1])
    ms = np.arange(2, NBIG + 1)
    rp = np.array([m for m in range(2, NBIG+1) if is_prime[m]])
    axB.semilogy(rp, red_deg[rp] + 0.7, '.', ms=3.0, color=RED, alpha=0.6,
                 label='RED hub degree — primes only  (~ NBIG/p)')
    axB.semilogy(ms, blue_deg[2:] + 0.7, '.', ms=2.5, color=BLUE, alpha=0.5,
                 label='BLUE hub degree — intermediate products in rebirth stems')
    # label the top blue hubs (the smooth / highly-composite numbers)
    top = np.argsort(blue_deg)[-9:]
    for m in sorted(top):
        axB.annotate(str(m), (m, blue_deg[m]), textcoords='offset points',
                     xytext=(2, 3), color=SILVER, fontsize=7.5)
    axB.set_xlabel('m'); axB.set_ylabel('number of factor-edges on m')
    axB.set_xlim(0, NBIG); axB.legend(fontsize=8, facecolor=BG, edgecolor='#33405e', labelcolor=FG)
    axB.set_title('B — the hubs: small primes carry extinction, smooth numbers carry rebirth',
                  color=FG, fontsize=10)

    out = os.path.join(_HERE, 'factor_web.png')
    fig.savefig(out, dpi=140); plt.close(fig)

    # ── console ─────────────────────────────────────────────────────
    print(f"{len(rec):,} (composite, prime-factor) edges over 2..{NBIG}")
    print(f"blue/red — min {ratio.min():.3f}  median {np.median(ratio):.2f}  max {ratio.max():.1f}")
    o = np.argsort(ratio)
    print("\nblue ≈ red  (rebirth barely costs more than the direct cut):")
    for i in o[:14]:
        n, p, rd, bl, om = rec[i]
        print(f"  n={int(n):5d}  p={int(p):<5d} red={rd:6.2f} blue={bl:6.2f}  ratio={ratio[i]:.3f}  Ω={int(om)}")
    print("\nblue ≫ red  (the factor is phase-distant — the stem winds far):")
    for i in o[-10:]:
        n, p, rd, bl, om = rec[i]
        print(f"  n={int(n):5d}  p={int(p):<5d} red={rd:6.2f} blue={bl:7.1f}  ratio={ratio[i]:.1f}  Ω={int(om)}")
    print('\n  written:', os.path.relpath(out, os.path.dirname(_HERE)))


if __name__ == '__main__':
    main()
