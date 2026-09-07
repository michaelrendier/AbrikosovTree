#!/usr/bin/env python3
"""
two_spin_resonance.py — the tower twist vs the factor winding, and where they lock
================================================================================

From the tower renders: each level adds a counter-clockwise turn (Θ(k)=k·22.5°);
the factors, north-pole down, turn clockwise.  Two counter-rotating spins.

    J_red  (twist / "what cannot be" / the tower)  :  φ_twist(m) = c · ln m,
             c = π / (8 ln 2) ≈ 0.5665   — LINEAR in The Scale, slow, CCW.
             ADDITIVE:  φ_twist(pq) = φ_twist(p) + φ_twist(q)  — it always closes.
    J_blue (winding / "what is" / the factors)     :  φ_wind(m) = 2π√m — grows
             like √m, fast, CW.
             NOT additive:  √(pq) ≠ √p + √q  — it closes only on a resonance.

Their interaction, for a semiprime N = p·q:  the twist closes exactly, so the
lock condition is purely on the winding —

        δ_w(N; p,q) = ‖ √(pq) − √p − √q ‖   (distance to the nearest integer)

δ_w = 0  ⇔  the two spins phase-lock  ⇔  the factor is "in phase" with N.
J_red = J_blue (σ = ½) is the 1:1 resonance; the detuning grows like √N, which
is why small N sits near the resonance and large N is thrown clear of it.

Panel A : the two counter-rotating spirals + their beats.
Panel B : the δ_w distribution and how it moves with ln N; the resonant set.
Output  : render/two_spin_resonance.png
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
C_TWIST = math.pi / (8 * math.log(2))          # rad of twist per e-fold of scale
RNG = np.random.default_rng(20260907)


def sieve(bound):
    s = bytearray([1]) * (bound + 1); s[0] = s[1] = 0
    for i in range(2, int(bound ** 0.5) + 1):
        if s[i]:
            s[i * i::i] = bytearray(len(s[i * i::i]))
    return np.flatnonzero(np.frombuffer(s, np.uint8))


def dist_int(x):
    return abs(x - round(x))


def main():
    P = sieve(1 << 20)
    # semiprimes across a wide size band, both factors prime, balanced-ish
    lo, hi = np.searchsorted(P, 30), np.searchsorted(P, 900000)
    M = 120000
    ip = RNG.integers(lo, hi, M); iq = RNG.integers(lo, hi, M)
    p = P[np.minimum(ip, iq)].astype(np.float64)
    q = P[np.maximum(ip, iq)].astype(np.float64)
    keep = p != q
    p, q = p[keep], q[keep]
    N = p * q
    lnN = np.log(N)

    # twist closure (should be ~0 to float error — J_red is additive)
    dt = np.abs(C_TWIST * np.log(N) - C_TWIST * np.log(p) - C_TWIST * np.log(q))
    # winding closure — the actual lock quantity
    sdef = np.sqrt(N) - np.sqrt(p) - np.sqrt(q)
    dw = np.abs(sdef - np.round(sdef))                # distance to nearest integer

    # shuffle control
    qs = q[RNG.permutation(len(q))]
    sdef_s = np.sqrt(p * qs) - np.sqrt(p) - np.sqrt(qs)
    dw_s = np.abs(sdef_s - np.round(sdef_s))

    fig = plt.figure(figsize=(15.5, 8.2))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.05, 1.0], hspace=0.42, wspace=0.30,
                          left=0.055, right=0.975, top=0.83, bottom=0.09)
    fig.suptitle('Two counter-rotating spins — the tower twist (J_red) vs the factor winding (J_blue)',
                 color=FG, fontsize=14, x=0.055, ha='left', y=0.965)
    fig.text(0.055, 0.915,
             'J_red twist φ = c·ln m (c = π/8ln2, CCW, additive — always closes).   '
             'J_blue winding φ = 2π√m (CW, √-fast, closes only on a resonance).\n'
             'lock quantity for N = p·q:  δ_w = ‖√(pq) − √p − √q‖ → 0 at a phase-lock.  '
             'the σ=½ (J_red = J_blue) 1:1 resonance detunes like √N.',
             color=GREY, fontsize=9, va='top')

    # ── A : the two spirals + beats ──────────────────────────────────
    axA = fig.add_subplot(gs[:, 0]); axA.set_aspect('equal')
    axA.set_xticks([]); axA.set_yticks([])
    t = np.linspace(math.log(2), math.log(400), 4000)
    axA.plot(t * np.cos(C_TWIST * t), t * np.sin(C_TWIST * t),
             color=RED, lw=1.3, alpha=0.85, label='J_red twist  (CCW, c·ln m)')
    axA.plot(t * np.cos(-2 * math.pi * np.sqrt(np.exp(t))),
             t * np.sin(-2 * math.pi * np.sqrt(np.exp(t))),
             color=BLUE, lw=0.5, alpha=0.55, label='J_blue winding  (CW, 2π√m)')
    # beats: where the two phases coincide mod 2π
    beat = np.where(np.abs(((C_TWIST * t + 2 * math.pi * np.sqrt(np.exp(t))) %
                            (2 * math.pi)) - math.pi) > math.pi - 0.03)[0]
    axA.plot((t[beat]) * np.cos(C_TWIST * t[beat]),
             (t[beat]) * np.sin(C_TWIST * t[beat]), 'o', ms=3, color=GOLD,
             label='beat (phases coincide)')
    axA.legend(fontsize=7.5, facecolor=BG, edgecolor='#33405e', labelcolor=FG, loc='lower left')
    axA.set_title('A — the two spins (m ≤ 400)', color=FG, fontsize=10)

    # ── B : δ_w distribution ────────────────────────────────────────
    axB = fig.add_subplot(gs[0, 1])
    axB.hist(dw, bins=60, density=True, histtype='step', color=BLUE, label='true pairs')
    axB.hist(dw_s, bins=60, density=True, histtype='step', color=GREY, label='shuffled')
    axB.axhline(2.0, color=GREY, ls=':', lw=0.8)      # uniform on [0,0.5] has density 2
    axB.set_xlabel('δ_w = ‖√(pq) − √p − √q‖'); axB.set_ylabel('density')
    axB.legend(fontsize=8, facecolor=BG, edgecolor='#33405e', labelcolor=FG)
    axB.set_title(f'B — lock quantity  (uniform ⇒ no lock).  median {np.median(dw):.3f} vs '
                  f'shuffled {np.median(dw_s):.3f}', color=FG, fontsize=9.5)

    # ── C : δ_w vs ln N ────────────────────────────────────────────
    axC = fig.add_subplot(gs[0, 2])
    bins = np.linspace(lnN.min(), lnN.max(), 22)
    bc = 0.5 * (bins[1:] + bins[:-1])
    med = [np.median(dw[(lnN >= a) & (lnN < b)]) for a, b in zip(bins[:-1], bins[1:])]
    med_s = [np.median(dw_s[(lnN >= a) & (lnN < b)]) for a, b in zip(bins[:-1], bins[1:])]
    axC.plot(bc, med, 'o-', color=BLUE, label='true')
    axC.plot(bc, med_s, 's--', color=GREY, label='shuffled')
    axC.axhline(0.25, color=GREY, ls=':', lw=0.8, label='uniform median')
    axC.set_xlabel('ln N'); axC.set_ylabel('median δ_w in bin'); axC.set_ylim(0, 0.3)
    axC.legend(fontsize=8, facecolor=BG, edgecolor='#33405e', labelcolor=FG)
    axC.set_title('C — does the lock degrade with size?', color=FG, fontsize=9.5)

    # ── D : twist closure (control — should be flat at 0) ──────────
    axD = fig.add_subplot(gs[1, 1])
    axD.hist(dt, bins=60, color=RED, alpha=0.7)
    axD.set_xlabel('|φ_twist(N) − φ_twist(p) − φ_twist(q)|')
    axD.set_title(f'D — J_red twist closure  (max {dt.max():.2e} — it closes exactly)',
                  color=FG, fontsize=9.5)

    # ── E : the resonant set ──────────────────────────────────────
    axE = fig.add_subplot(gs[1, 2])
    resmask = dw < 0.01
    axE.scatter(lnN[~resmask][:6000], dw[~resmask][:6000], s=3, color='#334263', alpha=0.4)
    axE.scatter(lnN[resmask], dw[resmask], s=12, color=GOLD, label=f'δ_w < 0.01  ({resmask.sum()})')
    axE.set_xlabel('ln N'); axE.set_ylabel('δ_w'); axE.set_ylim(0, 0.1)
    axE.legend(fontsize=8, facecolor=BG, edgecolor='#33405e', labelcolor=FG)
    axE.set_title('E — the phase-locked semiprimes', color=FG, fontsize=9.5)

    out = os.path.join(_HERE, 'two_spin_resonance.png')
    fig.savefig(out, dpi=140); plt.close(fig)

    # ── console verdict ────────────────────────────────────────────
    exp_uniform = 0.25
    print(f"{len(N):,} semiprimes,  ln N in [{lnN.min():.1f}, {lnN.max():.1f}]")
    print(f"J_red twist closure   : max |defect| = {dt.max():.2e}   (additive — closes exactly)")
    print(f"J_blue winding lock δ_w: median true {np.median(dw):.4f}  shuffled {np.median(dw_s):.4f}  "
          f"uniform {exp_uniform:.4f}")
    frac_res = (dw < 0.01).mean()
    frac_res_s = (dw_s < 0.01).mean()
    print(f"P(δ_w < 0.01)         : true {frac_res:.4f}   shuffled {frac_res_s:.4f}   "
          f"uniform 0.0200   -> {'LOCK' if frac_res > 1.5*frac_res_s else 'no lock beyond chance'}")
    # size trend
    lo_bin = dw[lnN < np.percentile(lnN, 15)]
    hi_bin = dw[lnN > np.percentile(lnN, 85)]
    print(f"median δ_w  small-N {np.median(lo_bin):.4f}   large-N {np.median(hi_bin):.4f}   "
          f"(detuning grows with N?  {'yes' if np.median(hi_bin) > np.median(lo_bin)+0.01 else 'flat'})")
    print('\n  written:', os.path.relpath(out, os.path.dirname(_HERE)))


if __name__ == '__main__':
    main()
