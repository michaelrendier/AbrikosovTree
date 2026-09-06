#!/usr/bin/env python3
"""
broken_so4_nodal.py — what the toroidal perturbation leaves behind
=================================================================

Hydrogen's clean n^-2 spectrum is protected by an SO(4) symmetry (the
Runge–Lenz vector).  Put the atom in a magnetic field and the diamagnetic
term

        H  =  p²/2  −  1/r  +  (γ²/8) ρ²          ρ² = x² + y²

is added.  That term depends ONLY on the distance from the field axis — a
torus around the axis.  It deletes the Runge–Lenz vector (SO(4) → SO(2): only
L_z survives).  The invariant tori of the motion do not vanish; they
*bifurcate* — KAM island chains, islands around islands, self-similar at every
scale.  Reference: Friedrich & Wintgen, Phys. Rep. 183 (1989) 37.

TOP ROW — scaled diamagnetic hydrogen, Poincaré surface of section (u = 0
plane) in regularised semiparabolic coordinates, at a ladder of scaled
energies ε = E·γ^(−2/3).  Nested closed curves = surviving tori; speckle =
chaotic sea.  The torus stack around the axis dissolving is the toroidal
bifurcation.

BOTTOM ROW — the quantum shadow, on the Hénon–Heiles system (the local normal
form of diamagnetic H at its saddle; perturbation (λ/3)·r³·sin 3θ is again a
pure angular term about the axis).  Nodal lines (ψ = 0) of an eigenstate deep
in the regular regime vs. one near the dissociation energy E_diss = 40/3: an
ordered set of nested nodal curves vs. irregular nodal domains — Chladni figures
gone fractal.

Output: render/broken_so4_diamagnetic.png
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.sparse import diags, kron, identity
from scipy.sparse.linalg import eigsh

_HERE = os.path.dirname(os.path.abspath(__file__))
BG   = '#07070f'; FG = '#c9d3e6'; GREY = '#7f8db0'
BLUE = '#5b8bff'; RED = '#ff5566'; GOLD = '#ffcf4a'; SILVER = '#dfe6ff'
plt.rcParams.update({
    'figure.facecolor': BG, 'axes.facecolor': BG, 'savefig.facecolor': BG,
    'text.color': FG, 'axes.edgecolor': '#33405e', 'axes.labelcolor': FG,
    'xtick.color': GREY, 'ytick.color': GREY, 'font.size': 10,
})


# ── scaled diamagnetic hydrogen — regularised semiparabolic dynamics ────────
# coords u,v with r = (u²+v²)/2, z = (u²−v²)/2, ρ = uv ; fictitious time τ.
# separable H = ½p² + W(q), W = −ε(u²+v²) + ⅛u²v²(u²+v²); h = 2 is conserved
# (the regularised −1/r).  Integrated with velocity-Verlet (symplectic).
def _force(q, eps):
    u, v = q[:, 0], q[:, 1]
    Fu = 2 * eps * u - 0.25 * u * v * v * (2 * u * u + v * v)
    Fv = 2 * eps * v - 0.25 * v * u * u * (2 * v * v + u * u)
    return np.column_stack((Fu, Fv))


def _h(q, p, eps):
    u, v = q[:, 0], q[:, 1]
    return (0.5 * (p * p).sum(1) - eps * (u * u + v * v)
            + 0.125 * u * u * v * v * (u * u + v * v))


def poincare(eps, n_ic=30, dt=0.007, nsteps=115000, seed=1):
    """Poincaré section on u = 0 (upward).  Returns [(v[], pv[])] per orbit."""
    rng = np.random.default_rng(seed)
    vmax = np.sqrt(2.0 / abs(eps)) * 0.985
    vs, pvs = [], []
    for _ in range(n_ic):
        for _ in range(400):
            v0 = rng.uniform(-vmax, vmax)
            pv0 = rng.uniform(-2.0, 2.0)
            if 2.0 - 0.5 * pv0**2 + eps * v0**2 > 0.03:
                break
        vs.append(v0); pvs.append(pv0)
    v0 = np.array(vs); pv0 = np.array(pvs)
    pu0 = np.sqrt(np.clip(2.0 * (2.0 - 0.5 * pv0**2 + eps * v0**2), 0, None))
    q = np.column_stack((np.zeros_like(v0), v0))
    p = np.column_stack((pu0, pv0))
    h0 = _h(q, p, eps)
    alive = np.ones(len(q), bool)
    hits = [([], []) for _ in range(len(q))]
    F = _force(q, eps)
    for _ in range(nsteps):
        q_old = q[:, 0].copy()
        p_half = p + 0.5 * dt * F
        q_new = q + dt * p_half
        F_new = _force(q_new, eps)
        p_new = p_half + 0.5 * dt * F_new
        q_new[~alive] = q[~alive]; p_new[~alive] = p[~alive]
        cross = alive & (q_old < 0) & (q_new[:, 0] >= 0)
        if cross.any():
            f = (-q_old[cross]) / (q_new[cross, 0] - q_old[cross])
            v_c = q[cross, 1] + f * (q_new[cross, 1] - q[cross, 1])
            pv_c = p[cross, 1] + f * (p_new[cross, 1] - p[cross, 1])
            for jj, j in enumerate(np.where(cross)[0]):
                hits[j][0].append(v_c[jj]); hits[j][1].append(pv_c[jj])
        q, p, F = q_new, p_new, F_new
        hh = _h(q, p, eps)
        bad = alive & (~np.isfinite(hh) | (np.abs(hh - h0) > 0.05)
                       | (np.abs(q).max(1) > 40))
        alive &= ~bad
    return [(np.array(a), np.array(b)) for a, b in hits if len(a) > 8]


# ── Hénon–Heiles quantum eigenstates on a finite-difference grid ───────────
# H = ½p² + ½(x²+y²) + λ(x²y − y³/3);  ℏ = m = 1.  λ = 1/√80 (Noid–Marcus),
# so E_diss = 1/(6λ²) = 40/3 ≈ 13.33 and a few dozen states sit below it.
LAM_HH = 1.0 / np.sqrt(80.0)
E_DISS = 1.0 / (6.0 * LAM_HH**2)


def henon_heiles_states(sigmas=(5.5, 12.7), k=20, n=320, L=9.0, lam=LAM_HH):
    x = np.linspace(-L, L, n); h = x[1] - x[0]
    X, Y = np.meshgrid(x, x, indexing='ij')
    V = 0.5 * (X**2 + Y**2) + lam * (X**2 * Y - Y**3 / 3.0)
    lap1 = diags([1.0, -2.0, 1.0], [-1, 0, 1], shape=(n, n)) / h**2
    I = identity(n)
    H = (-0.5 * (kron(lap1, I) + kron(I, lap1)) + diags(V.ravel())).tocsc()
    out = []
    for sig in sigmas:
        w, u = eigsh(H, k=k, sigma=sig, which='LM')
        j = int(np.argmin(np.abs(w - sig)))
        out.append((w[j], u[:, j].reshape(n, n), X, Y, V))
    return out


def main():
    fig = plt.figure(figsize=(15.5, 9.0))
    gs = fig.add_gridspec(2, 4, hspace=0.40, wspace=0.26,
                          left=0.055, right=0.975, top=0.80, bottom=0.07)
    fig.suptitle('Break the SO(4) symmetry — the toroidal bifurcation and the '
                 'self-similar maths it leaves',
                 color=FG, fontsize=14, x=0.055, ha='left', y=0.975)
    fig.text(0.055, 0.94,
             'top: scaled diamagnetic hydrogen, Poincaré section at u = 0.  the '
             'diamagnetic term (γ²/8)ρ² is a torus around the field axis; it '
             'deletes Runge–Lenz (SO(4)→SO(2)).  nested loops = surviving KAM '
             'tori,\nspeckle = chaotic sea.  bottom: the quantum shadow — '
             'Hénon–Heiles nodal lines (ψ = 0, silver), a regular state vs. one '
             'near the dissociation energy E_diss = 40/3 (gold dashed).',
             color=GREY, fontsize=9, va='top')

    for c, eps in enumerate([-0.60, -0.35, -0.20, -0.115]):
        ax = fig.add_subplot(gs[0, c])
        orbits = poincare(eps)
        cols = plt.cm.twilight(np.linspace(0.05, 0.95, max(len(orbits), 1)))
        for (vv, pv), col in zip(orbits, cols):
            ax.plot(vv, pv, '.', ms=0.7, color=col, alpha=0.85, rasterized=True)
        ax.set_title(f'ε = {eps:+.3f}', color=FG, fontsize=11)
        ax.set_xlabel('v'); ax.set_ylabel('p_v' if c == 0 else '')
        ax.set_facecolor('#0b0b18')

    # bottom-left: zoom on an island chain
    axz = fig.add_subplot(gs[1, 0])
    orb = poincare(-0.235, n_ic=60, nsteps=150000, seed=7)
    cols = plt.cm.twilight(np.linspace(0.05, 0.95, max(len(orb), 1)))
    for (vv, pv), col in zip(orb, cols):
        axz.plot(vv, pv, '.', ms=0.7, color=col, alpha=0.9, rasterized=True)
    axz.set_title('ε = −0.235 — island chains\n(islands around islands)',
                  color=FG, fontsize=10)
    axz.set_xlabel('v'); axz.set_ylabel('p_v'); axz.set_facecolor('#0b0b18')

    # bottom middle: Hénon–Heiles nodal lines
    try:
        states = henon_heiles_states()
        titles = ['regular regime\nnested nodal curves',
                  'near E_diss = 40/3\nirregular nodal domains']
        for i, (E, psi, X, Y, V) in enumerate(states):
            ax = fig.add_subplot(gs[1, 1 + i])
            psi = psi / np.max(np.abs(psi))
            psi = np.where(V <= E + 0.6, psi, np.nan)     # drop the forbidden tail
            ax.contourf(X, Y, psi, levels=np.linspace(-1, 1, 40),
                        cmap='twilight', alpha=0.55)
            ax.contour(X, Y, psi, levels=[0.0], colors=[SILVER], linewidths=0.6)
            ax.contour(X, Y, V, levels=[E], colors=[GOLD], linewidths=0.9,
                       linestyles='--')  # this state's classical turning boundary
            ax.set_title(f'{titles[i]}   (E = {E:.3f})', color=FG, fontsize=9.5)
            ax.set_aspect('equal'); ax.set_xlim(-7, 7); ax.set_ylim(-7, 7)
            ax.set_xticks([]); ax.set_yticks([])
    except Exception as e:                                            # noqa: BLE001
        ax = fig.add_subplot(gs[1, 1:3])
        ax.text(0.5, 0.5, f'Hénon–Heiles solve skipped:\n{e}',
                color=RED, ha='center', va='center', fontsize=9); ax.axis('off')

    # bottom-right: the reading
    axt = fig.add_subplot(gs[1, 3]); axt.axis('off')
    axt.text(0.0, 1.0,
             'THE SELF-SIMILAR RESIDUE\n\n'
             '• the perturbation is purely axial —\n'
             '  a torus around the axis, angle-\n'
             '  dependent only through sin(kθ).\n\n'
             '• it removes the hidden symmetry\n'
             '  (Runge–Lenz, for 1/r), so the tori\n'
             '  are no longer protected.\n\n'
             '• they do not disappear — they\n'
             '  bifurcate: a KAM chain of islands,\n'
             '  each island ringed by a smaller\n'
             '  chain, at every scale.\n\n'
             '• 1/r² is shared with Newtonian\n'
             '  gravity — so the same nested-\n'
             '  resonance maths runs the perturbed\n'
             '  Kepler / three-body problem\n'
             '  (Poincaré, 1890).',
             color=FG, fontsize=8.4, va='top', family='monospace')

    out = os.path.join(_HERE, 'broken_so4_diamagnetic.png')
    fig.savefig(out, dpi=140); plt.close(fig)
    print('written:', out)


if __name__ == '__main__':
    main()
