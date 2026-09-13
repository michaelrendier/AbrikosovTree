#!/usr/bin/env python3
"""
fermat_riemann_entropy.py — two different entropies over the same primes
=========================================================================

Cody, 2026-09-13: Fermat's factor-structure (the composites, the spaces
BETWEEN the primes) looked at "from across the boundary" (σ ↔ 1−σ, the
functional equation) by Riemann's zeta zeros, top-down — the claim is that
this exposes the GREATEST gaps first and only sharpens to the small, early
gaps as more zero-content is added; a claim this file makes FALSIFIABLE
rather than argued.

THE MECHANISM (not an analogy — the literal explicit formula):

    ψ(x) = x − Σ_ρ x^ρ/ρ − ln(2π) − ½ln(1−x⁻²)          (von Mangoldt/Riemann)

Pair each zero ρ=½+iγ with its conjugate 1−ρ̄ (required for convergence —
this sum is only conditionally convergent) and the pair collapses to

    2·Re(x^ρ/ρ) = (2/|ρ|)·√x·cos(γ·ln x − arg ρ)

— a literal Fourier term in ln x with ANGULAR FREQUENCY γ. Truncating the
sum at the first K zeros (ordered by |γ|, the only way the sum is ever
computed) is therefore exactly a low-pass reconstruction: γ is the axis
"top-down" moves along, and it is ORTHOGONAL to x — each new zero refines
the WHOLE range at once, unlike a sieve, which reveals gap information
strictly causally in x and never revisits a range once past it.

THE FALSIFIABLE CLAIM: if low-|γ| zeros really do carry coarse (large-
scale, "greatest spaces") structure and only high-|γ| zeros carry fine
(small-scale, individual-gap) structure, then a COARSE-GRAINED error
against the true ψ(x) should collapse at much smaller K than a
FINE-GRAINED (pointwise) error does. If both collapse at the same rate,
the claim is false — the zeros carry uniform, scale-blind information and
"top-down" is not a meaningful direction. Panel C measures exactly this,
with no interpretation baked in before the numbers come back.

Panel D is the OTHER entropy for contrast: the sieve's own reveal of gap
structure — strictly positional, strictly causal in x, no coarse/fine axis
at all. The two panels are not the same kind of plot on purpose.

Zeros: mpmath.zetazero(n), arbitrary precision, cached to
fermat_riemann_zeros_cache.json (repeat runs skip the ~20s/100-zero cost).
Output: render/fermat_riemann_entropy.png
"""
import os
import json
import math
import time
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

X_MAX = 3000
K_LIST = [0, 1, 2, 5, 10, 20, 50, 100, 150]
ZERO_CACHE = os.path.join(_HERE, 'fermat_riemann_zeros_cache.json')


def spf_sieve(n):
    s = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if s[i] == i:
            for j in range(i * i, n + 1, i):
                if s[j] == j:
                    s[j] = i
    return s


def psi_exact(n_max, spf):
    """von Mangoldt sum, exact, for every integer x up to n_max — one pass."""
    psi = np.zeros(n_max + 1)
    run = 0.0
    for x in range(2, n_max + 1):
        # is x a prime power p^k?  (spf gives the smallest prime factor)
        p = spf[x]
        y = x
        while y % p == 0:
            y //= p
        if y == 1:                        # x IS p^k for some k
            run += math.log(p)
        psi[x] = run
    return psi


def get_zeros(k_max):
    if os.path.exists(ZERO_CACHE):
        with open(ZERO_CACHE) as f:
            cached = json.load(f)
        if len(cached) >= k_max:
            return cached[:k_max]
    import mpmath
    mpmath.mp.dps = 20
    print(f'  computing {k_max} zeta zeros (mpmath.zetazero) — cached after this…')
    t0 = time.time()
    gammas = [float(mpmath.zetazero(n).imag) for n in range(1, k_max + 1)]
    print(f'  done in {time.time()-t0:.1f}s')
    with open(ZERO_CACHE, 'w') as f:
        json.dump(gammas, f)
    return gammas


def psi_K(xs, gammas, K):
    xs = np.asarray(xs, dtype=float)
    lnx = np.log(xs)
    sqrtx = np.sqrt(xs)
    s = xs.copy()
    for g in gammas[:K]:
        rho = complex(0.5, g)
        # 2*Re(x^rho / rho), x^rho = sqrt(x) * exp(i*g*lnx)
        c, sgn = np.cos(g * lnx), np.sin(g * lnx)
        xrho_re = sqrtx * c
        xrho_im = sqrtx * sgn
        # (xrho)/rho, rho = 0.5 + i g  ->  divide complex by complex
        denom = 0.25 + g * g
        term_re = (xrho_re * 0.5 + xrho_im * g) / denom
        s -= 2.0 * term_re
    s -= math.log(2 * math.pi)
    s -= 0.5 * np.log(np.maximum(1 - xs ** -2, 1e-300))
    return s


def main():
    print(f'sieving psi_exact up to {X_MAX}…')
    spf = spf_sieve(X_MAX)
    is_prime = [i > 1 and spf[i] == i for i in range(X_MAX + 1)]
    psi_true_int = psi_exact(X_MAX, spf)

    K_max = max(K_LIST)
    gammas = get_zeros(K_max)

    xs = np.arange(2, X_MAX + 1, dtype=float)
    psi_true = psi_true_int[2:]

    curves = {K: psi_K(xs, gammas, K) for K in K_LIST}

    # ── coarse vs fine residual, per K ──────────────────────────────────
    n_bins = 15
    bin_edges = np.linspace(2, X_MAX, n_bins + 1)
    bin_idx = np.clip(np.digitize(xs, bin_edges) - 1, 0, n_bins - 1)

    coarse_rmse, fine_rmse = [], []
    for K in K_LIST:
        d = curves[K] - psi_true
        fine_rmse.append(float(np.sqrt(np.mean(d ** 2))))
        bin_true = np.array([psi_true[bin_idx == b].mean() for b in range(n_bins)])
        bin_K = np.array([curves[K][bin_idx == b].mean() for b in range(n_bins)])
        coarse_rmse.append(float(np.sqrt(np.mean((bin_K - bin_true) ** 2))))

    # the falsifiable numbers: K at which each metric first drops under
    # 10% of its own K=0 value
    def half_life(series):
        target = series[0] * 0.10
        for K, v in zip(K_LIST, series):
            if v <= target:
                return K
        return None
    k_coarse_10pct = half_life(coarse_rmse)
    k_fine_10pct = half_life(fine_rmse)

    # ── prime gaps, positionally (the sieve's own entropy) ──────────────
    primes = [i for i in range(2, X_MAX + 1) if is_prime[i]]
    gaps = np.diff(primes)
    gap_n = primes[:-1]

    # ══════════════════════════════════════════════════════════════════
    fig = plt.figure(figsize=(16, 11.5))
    gs = fig.add_gridspec(3, 2, height_ratios=[1.05, 1.0, 1.0], hspace=0.55, wspace=0.24,
                          left=0.06, right=0.975, top=0.85, bottom=0.06)
    fig.suptitle('Two entropies over the same primes: position (the sieve) vs. zero-height (Riemann/Fermat)',
                 color=FG, fontsize=14, x=0.06, ha='left', y=0.965)
    fig.text(0.06, 0.925,
             'ψ_K(x) = x − Σ_{n≤K} 2·Re(x^ρ_n/ρ_n) − ln2π − ½ln(1−x⁻²), ρ_n=½+iγ_n, γ_n = the n-th zeta zero height.\n'
             'Each zero pair is a Fourier term of angular frequency γ in ln x — truncating at K zeros orders '
             'information by SCALE, not by position, coarse-to-fine as K grows.',
             color=GREY, fontsize=9, va='top')

    # A — psi_K(x) overlaid at a few K, vs the true step function
    axA = fig.add_subplot(gs[0, :])
    axA.plot(xs, psi_true, color=SILVER, lw=1.4, alpha=0.9, label='ψ(x)  (exact)')
    for K, col in zip((0, 5, 50, 150), (RED, GOLD, CY, BLUE)):
        axA.plot(xs, curves[K], color=col, lw=1.0, alpha=0.85, label=f'ψ_K(x),  K={K}')
    axA.set_xlim(2, X_MAX)
    axA.set_xlabel('x'); axA.set_ylabel('ψ(x)')
    axA.legend(fontsize=8.5, facecolor=BG, edgecolor='#33405e', labelcolor=FG, ncol=5, loc='upper left')
    axA.set_title('A — the explicit-formula reconstruction: smooth envelope (K small) sharpening '
                  'toward the true step function (K large)', color=FG, fontsize=10)

    # B — zoomed window, small x (where real gaps are smallest / most clustered)
    axB = fig.add_subplot(gs[1, 0])
    zoom = xs <= 200
    axB.plot(xs[zoom], psi_true[zoom], color=SILVER, lw=1.8, label='ψ(x) exact', drawstyle='steps-post')
    for K, col in zip((0, 10, 50, 150), (RED, GOLD, CY, BLUE)):
        axB.plot(xs[zoom], curves[K][zoom], color=col, lw=1.1, alpha=0.85, label=f'K={K}')
    axB.set_xlabel('x  (2..200 — where the real gaps are smallest)'); axB.set_ylabel('ψ(x)')
    axB.legend(fontsize=8, facecolor=BG, edgecolor='#33405e', labelcolor=FG)
    axB.set_title('B — the early, tightly-clustered region: needs the MOST zeros to resolve exactly',
                  color=FG, fontsize=9.5)

    # C — the falsifiable measurement: coarse vs fine RMSE vs K
    axC = fig.add_subplot(gs[1, 1])
    axC.semilogy(K_LIST, coarse_rmse, 'o-', color=GOLD, lw=1.6, label='coarse (15-bin average) RMSE')
    axC.semilogy(K_LIST, fine_rmse, 's-', color=RED, lw=1.6, label='fine (pointwise) RMSE')
    axC.set_xlabel('K  (number of zeta zero pairs used)'); axC.set_ylabel('RMSE vs ψ(x), log scale')
    axC.legend(fontsize=8.5, facecolor=BG, edgecolor='#33405e', labelcolor=FG)
    verdict = ('CONFIRMED — coarse collapses at far smaller K than fine'
              if (k_coarse_10pct is not None and (k_fine_10pct is None or k_coarse_10pct < k_fine_10pct))
              else 'NOT CONFIRMED on this range/K — see console')
    axC.set_title(f'C — the falsifiable claim: {verdict}', color=FG, fontsize=9.5)

    # D — the OTHER entropy: the sieve's positional reveal of gaps
    axD = fig.add_subplot(gs[2, :])
    axD.scatter(gap_n, gaps, s=3, color=BLUE, alpha=0.5)
    # average trend ~ ln(p), the PNT prediction, overlaid
    trend_x = np.array(gap_n, dtype=float)
    axD.plot(trend_x, np.log(trend_x), color=GOLD, lw=1.3, alpha=0.9,
            label='⟨gap⟩ ~ ln(p)  (Prime Number Theorem)')
    axD.set_xlabel('p_n  (position along the number line)'); axD.set_ylabel('gap  g_n = p_{n+1} − p_n')
    axD.legend(fontsize=8.5, facecolor=BG, edgecolor='#33405e', labelcolor=FG)
    axD.set_title('D — the SIEVE\'s entropy, for contrast: gaps revealed strictly causally in x, '
                  'one at a time, no coarse/fine axis — small near the start, growing (with huge local '
                  'variance) as x increases', color=FG, fontsize=9.5)

    out = os.path.join(_HERE, 'fermat_riemann_entropy.png')
    fig.savefig(out, dpi=140); plt.close(fig)

    print(f'\n{"K":>5}  {"coarse RMSE":>12}  {"fine RMSE":>12}')
    for K, c, fi in zip(K_LIST, coarse_rmse, fine_rmse):
        print(f'{K:>5}  {c:>12.4f}  {fi:>12.4f}')
    print(f'\ncoarse RMSE drops to 10% of its K=0 value at K = {k_coarse_10pct}')
    print(f'fine   RMSE drops to 10% of its K=0 value at K = {k_fine_10pct}')
    print(f'\nVERDICT: {verdict}')
    print('\n  written:', os.path.relpath(out, os.path.dirname(_HERE)))


if __name__ == '__main__':
    main()
