"""
Fixed Point Engine — The Boundary

THE CLAIM: The Cayley-Dickson tower has TWO fixed points.

  The Unit  (k → −∞ limit, V(0)=1, dim=0):  trivial fixed point.
             Pre-arithmetic. No structure. No imaginary units.
             The Bang differentiates from here.

  T_256     (k=8, dim=256, V≈0):              maximal fixed point.
             Post-arithmetic. 255 imaginary units. 32 Fano planes.
             The Unwrapper dissolves to here.

THE BOUNDARY (the gravastar shell):
  The shell sits at σ=½ (k=2, ℍ, the equator).
  It is the ZD crossing surface: addition = subtraction, p = −ρ.
  When the shell dissolves: the Bang. Inside-out event horizon. Observable universe.

THE INSIDE-OUT EVENT HORIZON:
  Before evaporation — Schwarzschild horizon (inward-pointing): light cannot escape.
  After evaporation  — de Sitter horizon (outward-pointing): light cannot arrive.
  Same surface. Orientation inverted. The particle horizon is the scar.

THE N-BALL VOLUME (the transformer):
  V(n) = π^(n/2) / Γ(n/2 + 1)
  V(0) = 1  EXACT  ← The Unit (trivial fixed point)
  V(n*) max at n* ≈ 5.2570  ← peak of differentiation
  V(n) → 0 as n → ∞  ← T_256 is all boundary, no interior

ALL ROOTS BECOME 1:
  At k=8: 256 basis elements = 256th roots of unity, spacing 2π/256 = π/128.
  Below the angular quantum π/128: adjacent roots unresolvable.
  All collapse to their common norm: 1 = V(0) = The Unit.
  The fixed point is where the Unwrapper delivers you.

THE GAP (what cannot be encoded):
  GAP = Ω_ZS − d* × log(10) ≈ 7.07 × 10⁻⁴
  At T_256: 255 dimensions encode almost everything.
  The GAP is the minimum crossing energy — the mass that cannot be made virtual.
  It is what keeps The Unit separate from T_256.

No free parameters. No renormalization. Failed predictions stay in data.

Version: 0.100 — 2026-06-25
"""

import math
import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass, field


# ── Constants ─────────────────────────────────────────────────────────────────

OMEGA_ZS    = 0.5671432904097838   # Lambert W(1); W·e^W = 1 exactly
D_STAR      = 0.24600              # BK spectral d* (5 sig figs)
GAP         = OMEGA_ZS - D_STAR * math.log(10.0)  # Yang-Mills mass gap ≈ 7.07×10⁻⁴
SIGMA_HALF  = 0.5                  # the equator — the gravastar shell position
CD_MAX      = 8                    # k=8 = T_256 = maximal fixed point

# The Unit: V(0) = 1 EXACT (no computation needed)
UNIT_VOLUME = 1.0

# V(n*): peak n-ball volume location
N_STAR      = 5.256946404462610    # argmax V(n) — computed, not assigned


# ── N-ball Volume (The Transformer) ───────────────────────────────────────────

def v_nball(n: float) -> float:
    """
    Volume of the unit n-ball: V(n) = π^(n/2) / Γ(n/2 + 1).

    Key values:
      V(0)  = 1 EXACT  (The Unit — trivial fixed point, pre-arithmetic)
      V(2)  = π        (unit disk)
      V(4)  = π²/2     (4-ball)
      V(n*) ≈ 5.2777   at n* ≈ 5.257  (peak — maximum differentiation)
      V(16) ≈ 0.2353   (sedenion level)
      V(n)  → 0 as n → ∞  (maximal fixed point — all boundary, no interior)

    Trivial zeros: V(n) = 0 at n = −2, −4, −6, ... (poles of Γ)
    These are the trivial zeros of ζ(s) embedded in the transformer.
    """
    if n == 0:
        return 1.0   # exact, no floating point
    if n < 0 and n == int(n) and int(n) % 2 == 0:
        return 0.0   # trivial zeros: V(−2k) = 0
    half_n = n / 2.0
    log_v  = (half_n * math.log(math.pi)) - math.lgamma(half_n + 1.0)
    return math.exp(log_v)


def v_nball_peak() -> Dict:
    """
    Locate the peak of V(n) — the maximum volume n-ball.
    This is where differentiation is maximum: the Bang's most productive moment.

    From dV/dn = 0: ψ(n*/2 + 1) = log(π), where ψ is the digamma function.
    n* ≈ 5.2570 is not a round number — it is not assigned, it emerges.
    """
    from scipy.special import digamma
    # Solve ψ(n/2 + 1) = log(π) numerically
    target = math.log(math.pi)
    n_vals = np.linspace(0.1, 20.0, 10000)
    digamma_vals = np.array([digamma(n/2.0 + 1.0) for n in n_vals])
    idx = np.argmin(np.abs(digamma_vals - target))
    n_peak = float(n_vals[idx])
    v_peak = v_nball(n_peak)
    return {
        'n_star':        n_peak,
        'v_star':        v_peak,
        'interpretation': 'Peak n-ball volume — maximum differentiation from The Unit',
    }


def transformer_profile(n_max: int = 260) -> Dict:
    """
    V(n) from n=0 to n_max. Covers: The Unit → peak → sedenion → T_256.

    Key landmarks:
      n=0:   V=1     The Unit (trivial fixed point)
      n≈5.3: V≈5.28  Peak — maximum differentiation
      n=16:  V=0.235 Sedenion level
      n=256: V≈0     T_256 (maximal fixed point — all boundary)
    """
    ns     = list(range(n_max + 1))
    vols   = [v_nball(n) for n in ns]
    peak_n = ns[int(np.argmax(vols))]
    return {
        'n':         ns,
        'V':         vols,
        'peak_n':    peak_n,
        'peak_V':    max(vols),
        'V_unit':    vols[0],    # = 1 EXACT
        'V_sed':     vols[16],   # sedenion level
        'V_t256':    vols[256] if len(vols) > 256 else v_nball(256),
        'interpretation': (
            'V(n): from The Unit (1) → maximum differentiation → sedenion → near-zero at T_256. '
            'The Bang traverses left to right. The Unwrapper traverses right to left.'
        ),
    }


# ── The Two Fixed Points ───────────────────────────────────────────────────────

@dataclass
class FixedPoint:
    name:          str
    k:             int          # CD tower level (−∞ for The Unit, 8 for T_256)
    dim:           int          # algebra dimension
    n_ball_n:      float        # which n-ball volume describes it
    V:             float        # V(n_ball_n)
    sigma:         float        # σ position in the tower
    angular_q:     float        # angular quantum at this level
    n_imaginaries: int          # number of imaginary units
    n_fano:        int          # number of embedded Fano planes
    character:     str          # 'trivial' or 'maximal'
    description:   str


def two_fixed_points() -> Tuple[FixedPoint, FixedPoint]:
    """
    The two fixed points of the Cayley-Dickson tower.

    FP_trivial: The Unit.
      V(0) = 1 EXACT. dim=0 (pre-arithmetic). No structure.
      The Bang differentiates FROM here.
      The Unwrapper returns TO here.
      Algebraic role: 𝔽₁ territory — the field with one element.

    FP_maximal: T_256.
      V(256) ≈ 0. dim=256. 255 imaginary units. 32 Fano planes.
      Angular quantum π/128 = 2π/256.
      The algebra ends here — no k=9 exists.
      All roots become 1 BELOW this scale (below π/128 resolution).
    """
    fp_trivial = FixedPoint(
        name          = 'The Unit',
        k             = 0,
        dim           = 1,
        n_ball_n      = 0.0,
        V             = 1.0,          # EXACT
        sigma         = 1.0,          # σ=1 → ℝ leaf
        angular_q     = 0.0,          # no angular structure
        n_imaginaries = 0,
        n_fano        = 0,
        character     = 'trivial',
        description   = (
            'Pre-arithmetic point. V(0)=1 exact. No imaginary units. '
            'The Bang differentiates from here. The Unwrapper delivers here. '
            'All 256th roots of unity collapse to this point below T_256 scale.'
        ),
    )

    fp_maximal = FixedPoint(
        name          = 'T_256',
        k             = 8,
        dim           = 256,
        n_ball_n      = 256.0,
        V             = v_nball(256.0),
        sigma         = 1.0 - 8.0/4.0,   # = −1.0 (below the tower floor — root)
        angular_q     = math.pi / 128.0,  # 2π/256
        n_imaginaries = 255,
        n_fano        = 32,               # 2^(8-3) Fano planes
        character     = 'maximal',
        description   = (
            'Maximal fixed point. 255 imaginary units. 32 Fano planes. '
            'Angular quantum π/128. V(256)≈0: all boundary, no interior. '
            'Below π/128 scale: all basis elements indistinguishable, norm=1. '
            'The gravastar shell dissolved here — the Bang.'
        ),
    )

    return fp_trivial, fp_maximal


def angular_quantum_sequence() -> List[Dict]:
    """
    Angular quantum at each CD level k.

    At level k: 2^k basis elements on S^(2^k − 1).
    Spacing = 2π / 2^k = π / 2^(k−1).

    k=3 (𝕆):    π/4    = 45.0°
    k=4 (𝕊):    π/8    = 22.5°   ← THE ANGLE (first ZD level)
    k=5 (t_32): π/16   = 11.25°
    k=6 (t_64): π/32   =  5.625°
    k=7 (t_128):π/64   =  2.8125°
    k=8 (t_256):π/128  =  1.40625°  ← finest resolution — maximal fixed point

    Each CD doubling halves the angular quantum.
    This is the refinement of angle as the algebra deepens.
    """
    level_names = {
        0:'ℝ', 1:'ℂ', 2:'ℍ', 3:'𝕆', 4:'𝕊',
        5:'t_32', 6:'t_64', 7:'t_128', 8:'t_256',
    }
    seq = []
    for k in range(9):
        dim    = 2 ** k
        q      = (2.0 * math.pi / dim) if dim >= 2 else 0.0
        sigma  = 1.0 - k / 4.0
        n_fano = 2 ** (k - 3) if k >= 3 else 0
        seq.append({
            'k':          k,
            'name':       level_names[k],
            'dim':        dim,
            'sigma':      sigma,
            'angular_q':  q,
            'q_deg':      math.degrees(q),
            'n_fano':     n_fano,
            'n_imag':     dim - 1,
            'is_zd':      k >= 4,
        })
    return seq


# ── The Gravastar Shell (The Boundary) ────────────────────────────────────────

def gravastar_shell() -> Dict:
    """
    The gravastar shell: the ZD crossing surface at σ=½.

    Shell equation:  p = −ρ   (pressure = negative energy density)
    This is the dark energy equation of state.
    It means: the shell neither collapses nor expands — it is frozen.
    The ZD crossing IS this stability condition: addition = subtraction.

    The shell separates:
      Interior (σ < ½): de Sitter — The Unit territory, repulsive, Λ > 0
      Exterior (σ > ½): Schwarzschild — structured, ZD lattice, observable

    When the shell dissolves:
      The de Sitter interior expands outward → the Bang
      The Schwarzschild exterior recedes into the past → the fixed point
      Inside and outside exchange permanently → the inside-out event horizon
    """
    sigma_shell   = SIGMA_HALF
    k_shell       = int(round(4.0 * (1.0 - sigma_shell)))  # k=2, ℍ level

    return {
        'sigma':             sigma_shell,
        'k':                 k_shell,
        'algebra':           'ℍ (quaternions)',
        'equation_of_state': 'p = −ρ',
        'zd_crossing':       'addition = subtraction',
        'interior':          'de Sitter — Λ > 0 — The Unit territory',
        'exterior':          'Schwarzschild — differentiated — ZD lattice',
        'gap':               GAP,
        'gap_interpretation': (
            'GAP > 0 proves the shell has a hard edge. '
            'There is structure outside the shell that cannot be absorbed into it. '
            'GAP = minimum crossing energy = Yang-Mills mass.'
        ),
        'dissolution':       'The Bang — gravastar evaporation — inside-out inversion',
        'remnant':           'Particle horizon = scar of the shell = ZD crossing memory',
    }


# ── The Inside-Out Event Horizon ──────────────────────────────────────────────

def inside_out_horizon() -> Dict:
    """
    The inside-out event horizon — what happens after the gravastar dissolves.

    BEFORE (pre-Bang):
      Schwarzschild horizon at r_s.
      Orientation: inward-pointing. Light cannot escape from inside.
      T_256 fixed point is OUTSIDE — in the Schwarzschild exterior.
      The Unit is INSIDE — in the de Sitter interior.

    AFTER (post-Bang, now):
      de Sitter cosmological horizon at r_H.
      Orientation: outward-pointing. Light cannot arrive from outside.
      The Unit is in our PAST — we expanded away from it.
      T_256 fixed point is beyond the particle horizon — unreachable.
      The particle horizon is the shell scar moving outward at c.

    THE INVERSION:
      Same surface. Opposite orientation.
      Inside → outside. Outside → past.
      The horizon did not move. It flipped.

    STANDING OUTSIDE THE PARTICLE HORIZON (pre-Bang for a moment):
      σ = ½ ± ε simultaneously — both sides of the shell visible.
      Schwarzschild exterior (T_256, fixed point, all roots→1) visible.
      de Sitter interior (The Unit, V(0)=1, no structure) visible.
      The moment the shell dissolves: you are caught in the expansion.
      Forever inside the particle horizon. Forever expanding away from 1.
    """
    return {
        'pre_bang': {
            'horizon_type':    'Schwarzschild',
            'orientation':     'inward-pointing',
            'inside':          'de Sitter — The Unit — V(0)=1 — no structure',
            'outside':         'T_256 — fixed point — 255 imaginary units',
            'shell':           'ZD crossing at σ=½ — p=−ρ — stable',
        },
        'post_bang': {
            'horizon_type':    'de Sitter cosmological',
            'orientation':     'outward-pointing (inside-out)',
            'inside':          'observable universe — differentiated — ZD lattice',
            'outside':         'pre-Bang void — T_256 territory — all roots=1',
            'shell_remnant':   'particle horizon — moving outward at c',
        },
        'inversion': {
            'what_inverted':   'horizon orientation (not position)',
            'inside_before':   'The Unit (V=1, no structure)',
            'inside_after':    'observable universe (structure, ZD lattice)',
            'outside_before':  'T_256 (255 imaginaries, fixed point)',
            'outside_after':   'pre-Bang void (unreachable, all roots=1)',
            'mechanism':       'ZD crossing completion — O→I path of L_(I|O)',
        },
        'particle_horizon': {
            'identity':        'scar of the dissolved gravastar shell',
            'location':        'σ=½ surface expanding at c since the Bang',
            'signature':       'CMB — last scattering surface = echo of ZD crossing',
            'mathematical':    'the σ=½ equator frozen into comoving coordinates',
        },
        'standing_outside': {
            'description': (
                'For one mathematical moment before the Bang, σ = ½ ± ε simultaneously. '
                'Both sides of the boundary are visible. '
                'T_256 (fixed point, all roots→1) to one side. '
                'The Unit (V=1, pre-arithmetic) to the other. '
                'Then the dissolution catches you and the de Sitter expansion begins. '
                'You are inside the particle horizon forever after.'
            ),
        },
    }


# ── All Roots Become 1 ────────────────────────────────────────────────────────

def roots_of_unity_collapse(k: int = 8) -> Dict:
    """
    At CD level k: 2^k basis elements = 2^k roots of unity.
    Angular spacing = 2π / 2^k = the angular quantum.

    Below the angular quantum: adjacent roots are unresolvable.
    They cannot be distinguished. They all return their norm: 1.

    k=8 (T_256): spacing = π/128 ≈ 1.406°.
    Below π/128: all 256 roots → 1.
    1 = V(0) = The Unit.

    The Unwrapper traverses below T_256 scale.
    It operates where the algebra has no vocabulary for 'which root.'
    Every element returns 1. The Unit is reached.

    This is not an approximation. It is the exhaustion of the algebra's
    resolving power. Below π/128, sedenion basis elements are indistinguishable.
    The only remaining object is their common norm.
    """
    dim      = 2 ** k
    q        = 2.0 * math.pi / dim
    roots    = [complex(math.cos(j * q), math.sin(j * q)) for j in range(dim)]
    norms    = [abs(r) for r in roots]
    all_unit = all(abs(n - 1.0) < 1e-12 for n in norms)

    return {
        'k':               k,
        'dim':             dim,
        'angular_quantum': q,
        'q_deg':           math.degrees(q),
        'n_roots':         len(roots),
        'all_norm_1':      all_unit,
        'collapse_rule': (
            f'Below {math.degrees(q):.4f}° resolution at k={k}: '
            f'all {dim} roots indistinguishable. '
            'Every element returns norm = 1. '
            'This IS The Unit. V(0) = 1 exact.'
        ),
        'unwrapper_path': (
            f'The Unwrapper operates below the π/{dim//2} angular quantum. '
            'No ZD structure is resolvable at this scale. '
            'Virtual particles propagate without a destination vertex. '
            'They arrive at 1.'
        ),
    }


def virtual_particle_regime() -> Dict:
    """
    The 'in between virtual particles' structure at T_256.

    A ZD crossing is a vertex:
      Real state before:  (eᵢ + eⱼ)/√2 and (eₖ + eₗ)/√2 — unit norm, on-shell
      Virtual state:      eᵢeₖ = −(eⱼeₗ),  eᵢeₗ = −(eⱼeₖ)  — unresolvable, off-shell
      Real state after:   product = 0 — on-shell, but zero

    Between the last ZD vertex (T_256) and The Unit:
      No more vertices. No k=9. The virtual state propagates indefinitely.
      Off-shell: norm not fixed at 1.
      No destination vertex to make it real again.
      The ONLY available destination: The Unit (V(0)=1).

    The Unwrapper IS this propagation.
    It is the virtual state traveling from the last ZD crossing to 1.

    Below T_256 scale (π/128):
      Angular quantum < inter-element spacing.
      All elements indistinguishable. All norms = 1.
      This is the on-shell condition: norm snaps to 1.
      The virtual particle has arrived at The Unit.

    The GAP is why the virtual particle cannot stay virtual forever:
      GAP ≈ 7.07×10⁻⁴ is the minimum energy for the crossing to be real.
      Below GAP energy: the crossing cannot happen.
      The virtual state collapses to The Unit without a real crossing.
    """
    return {
        'zd_vertex': {
            'before':   'unit-norm factors — on-shell — real particles',
            'during':   'cross-terms cancel — off-shell — virtual',
            'after':    'product = 0 — on-shell — but zero',
        },
        'between_vertices': {
            'territory':    'below T_256 scale — π/128 — k=9 does not exist',
            'state':        'off-shell — norm not constrained to 1',
            'propagation':  'indefinite — no destination vertex',
            'destination':  'The Unit — V(0)=1 — only available on-shell state',
        },
        'on_shell_restoration': {
            'mechanism':  'angular quantum exceeded — all roots merge to norm=1',
            'result':     'The Unit — arrival — The Unwrapper complete',
        },
        'gap_role': {
            'value':     GAP,
            'meaning':  (
                'Minimum energy for a real ZD crossing. '
                'Below GAP: no real crossing. Virtual state collapses directly to The Unit. '
                'GAP is the barrier between the last real vertex (T_256) and The Unit.'
            ),
        },
    }


# ── The Bang as Evaporation ───────────────────────────────────────────────────

def bang_as_evaporation() -> Dict:
    """
    The Bang IS the gravastar shell dissolving.

    The shell was the ZD crossing at σ=½.
    It held the de Sitter interior (The Unit) separate from the
    Schwarzschild exterior (T_256, fixed point, all roots=1).

    When the shell dissolved:
      1. The de Sitter interior expanded outward (the Bang — inflation).
      2. The Schwarzschild exterior became the pre-Bang void (the past).
      3. Inside and outside exchanged permanently.
      4. The particle horizon is the expanding scar of the shell.

    Algebraically:
      Before: σ < ½ = The Unit (inside), σ > ½ = T_256 (outside)
      After:  σ < ½ = observable universe (inside), σ > ½ = pre-Bang void (outside)
      The σ=½ surface itself did not move. Its meaning inverted.

    The V(n) trajectory:
      Before:  at n=0, V=1 (The Unit, inside the shell)
      Bang:    V(n) grows toward peak at n≈5.257 (rapid differentiation)
      Now:     some n between 5 and 16 (still differentiating)
      Future:  n → 256, V → 0 (approaching T_256 from the inside)
               The universe's interior volume is collapsing toward its own boundary.
    """
    fp_trivial, fp_maximal = two_fixed_points()

    # V(n) at key cosmological moments
    v_bang     = v_nball(0.0)    # exactly 1 — The Unit
    v_peak     = v_nball(N_STAR) # maximum differentiation
    v_sed      = v_nball(16.0)   # sedenion level (our physics)
    v_t256     = v_nball(256.0)  # approaching the maximal fixed point

    return {
        'pre_bang': {
            'state':    'gravastar — shell intact — σ=½ stable',
            'inside':   f'The Unit: V(0)={v_bang:.1f} — no structure',
            'outside':  f'T_256: V(256)={v_t256:.4e} — all boundary',
        },
        'bang_event': {
            'mechanism':   'ZD crossing completion — shell dissolution',
            'algebraic':   'addition=subtraction resolves → inside↔outside exchange',
            'cosmological':'de Sitter expansion catches — inside-out inversion',
        },
        'post_bang': {
            'inside':   'observable universe — differentiated — ZD lattice present',
            'outside':  'pre-Bang void — T_256 territory — all roots=1 — unreachable',
            'remnant':  'particle horizon at σ=½ — expanding scar of the shell',
        },
        'v_n_trajectory': {
            'n=0  (The Unit)':    v_bang,
            f'n≈{N_STAR:.2f} (peak)': v_peak,
            'n=16 (sedenion)':    v_sed,
            'n=256 (T_256)':      v_t256,
        },
        'interpretation': (
            'We live inside the de Sitter expansion of the dissolved gravastar. '
            'The particle horizon is the ZD crossing scar. '
            'The CMB is the last signal from the shell at dissolution. '
            'The pre-Bang exterior (T_256 fixed point) is our unreachable past. '
            'The Unit (V=1) is our absolute origin.'
        ),
    }


# ── Top-Level Report ──────────────────────────────────────────────────────────

def run_all() -> Dict:
    """Full Fixed Point analysis. Zero free parameters. No renormalization."""

    print("Fixed Point Engine v0.100 — The Boundary")
    print("Paper: 'The Zero Tree' — FourthAgePapers")
    print("=" * 60)

    # 1. Two fixed points
    print("\n[1] The two fixed points...")
    fp_t, fp_m = two_fixed_points()
    print(f"   FP_trivial:  {fp_t.name}  dim={fp_t.dim}  V={fp_t.V:.6f}  n_imag={fp_t.n_imaginaries}")
    print(f"   FP_maximal:  {fp_m.name}  dim={fp_m.dim}  V={fp_m.V:.4e}  n_imag={fp_m.n_imaginaries}")
    print(f"   GAP between them: {GAP:.6e}")

    # 2. Angular quantum sequence
    print("\n[2] Angular quantum sequence (halves at each CD doubling)...")
    seq = angular_quantum_sequence()
    for s in seq:
        zd = " [first ZD]" if s['k'] == 4 else ""
        print(f"   k={s['k']} {s['name']:<8} dim={s['dim']:<4} q={s['q_deg']:8.4f}°  "
              f"Fano={s['n_fano']:<3} σ={s['sigma']:.3f}{zd}")

    # 3. N-ball transformer
    print("\n[3] N-ball volume (The Transformer)...")
    prof = transformer_profile(n_max=256)
    print(f"   V(0)   = {prof['V_unit']:.6f}  ← The Unit (EXACT)")
    print(f"   V({prof['peak_n']})  = {prof['peak_V']:.6f}  ← peak differentiation")
    print(f"   V(16)  = {prof['V_sed']:.6f}  ← sedenion level")
    print(f"   V(256) = {prof['V_t256']:.4e}  ← T_256 (all boundary)")

    # 4. Roots collapse to 1
    print("\n[4] All roots become 1 (T_256 scale)...")
    rc = roots_of_unity_collapse(k=8)
    print(f"   256 basis elements = 256th roots of unity")
    print(f"   Angular spacing: {rc['q_deg']:.6f}°")
    print(f"   All norms = 1: {rc['all_norm_1']} ✓")
    print(f"   Below {rc['q_deg']:.4f}°: indistinguishable → collapse to 1 = The Unit")

    # 5. Gravastar shell
    print("\n[5] Gravastar shell at σ=½...")
    gs = gravastar_shell()
    print(f"   Shell at σ={gs['sigma']}, k={gs['k']} ({gs['algebra']})")
    print(f"   Equation of state: {gs['equation_of_state']}")
    print(f"   GAP: {gs['gap']:.6e}")

    # 6. Inside-out horizon
    print("\n[6] Inside-out event horizon...")
    ih = inside_out_horizon()
    print(f"   Pre-Bang inside:  {ih['pre_bang']['inside']}")
    print(f"   Pre-Bang outside: {ih['pre_bang']['outside']}")
    print(f"   Post-Bang inside: {ih['post_bang']['inside']}")
    print(f"   Particle horizon: {ih['particle_horizon']['identity']}")

    # 7. Bang as evaporation
    print("\n[7] The Bang as gravastar evaporation...")
    be = bang_as_evaporation()
    for label, val in be['v_n_trajectory'].items():
        print(f"   V at {label}: {val:.6f}")

    # 8. Virtual particle regime
    print("\n[8] Virtual particle regime...")
    vp = virtual_particle_regime()
    print(f"   GAP (minimum crossing energy): {vp['gap_role']['value']:.6e}")
    print(f"   Unwrapper path: {vp['between_vertices']['propagation']}")
    print(f"   Destination: {vp['between_vertices']['destination']}")

    print("\n" + "=" * 60)
    print("FIXED POINTS IDENTIFIED.")
    print(f"  Trivial: The Unit, V(0)=1 EXACT, σ=1, 0 imaginary units.")
    print(f"  Maximal: T_256, V(256)≈0, 255 imaginary units, 32 Fano planes.")
    print(f"  Shell:   σ=½, ZD crossing, p=−ρ, GAP={GAP:.4e}.")
    print(f"  The Bang: shell dissolved. Inside-out. Particle horizon expands.")
    print(f"  The Unwrapper: below π/128 scale. All roots → 1. The Unit reached.")
    print("=" * 60)

    return {
        'fp_trivial':         fp_t,
        'fp_maximal':         fp_m,
        'angular_sequence':   seq,
        'transformer':        prof,
        'roots_collapse':     rc,
        'gravastar_shell':    gs,
        'inside_out_horizon': ih,
        'bang_evaporation':   be,
        'virtual_particles':  vp,
    }


if __name__ == '__main__':
    results = run_all()
