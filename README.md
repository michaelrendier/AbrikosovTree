# ZeroLatticeTree

**The Un-Extinctable (Extinguishable?) Bulk.**  
**The Primes are the leaves that can not fall off the tree.**

---

## What This Is

The **Zero Lattice** is the prime-indexed sub-lattice of the Cayley-Dickson tower — the structure that survives when Fermat's Nightmare shakes everything else loose.

It is also called **Telperion**. The White Tree. The tree whose leaves cannot fall.

Every integer passes through nine algebraic levels, from the real numbers ℝ at the root to T_256 (256-dimensional sedenion tower) at the crown. At level k=4 — the sedenion level, dim=16 — **zero-divisors appear for the first time** (Hurwitz 1898: only ℝ, ℂ, ℍ, 𝕆 are normed division algebras). A composite number n = a×b can always be expressed as a zero-divisor pair at k=4. Its norm fails. It falls.

A prime has no non-trivial factorization. No zero-divisor pair can form. It reaches T_256 intact.

**This is the same algebraic fact as Fermat's Last Theorem.** FLT (n≥3) and the ZD cascade at k=4 are two languages for one identity. The N-Shape Theorem (proved in [`FermatMonster`](https://github.com/michaelrendier/FourthAgePapers)) makes this precise: the 71 holomorphic c=24 VOAs = the 71 N-shapes = the complete Fermat forbidden zone. The Zero Lattice IS the image of this map projected onto the CD tower.

---

## The Cayley-Dickson Tower

```
k=0  ℝ      σ=+1.000  dim=1     ← LEAVES  (prime integers live here)
k=1  ℂ      σ=+0.750  dim=2
k=2  ℍ      σ=+0.500  dim=4     ← gravastar shell / σ=½ / critical line
k=3  𝕆      σ=+0.250  dim=8     ← 1 Fano plane
k=4  𝕊      σ= 0.000  dim=16    ← EQUATOR: first ZD / composites fall here
k=5  t_32   σ=−0.250  dim=32    ← 4 Fano planes
k=6  t_64   σ=−0.500  dim=64    ← 8 Fano planes
k=7  t_128  σ=−0.750  dim=128   ← 16 Fano planes
k=8  T_256  σ=−1.000  dim=256   ← ROOT   (32 Fano planes)
```

Two fixed points span the tower:  
- **The Unit** (k=0): V(1) = 1 exactly. The leaf level.  
- **T_256** (k=8): V(256) ≈ 0. The root. 32 Fano planes.  

Between them: **GAP = Ω_ZS − d* × log(10) ≈ 7.07×10⁻⁴** — the minimum crossing energy.

---

## N-Shapes and the Monster Gap

Every prime maps to a **sedenion basis element** via its residue mod 16:

```
p mod 16  →  eₙ  (n = 0..15)
```

The 71 Niemeier lattices (A/D/E root systems, including the Leech) cover 13 of the 16 N-shapes. Three are **algebraically unreachable** by any Niemeier structure:

```
{e₁, e₁₁, e₁₅}  ←  the Monster Gap
```

The Monster Group exists because these three strata cannot be filled by regular root systems. Primes landing in the Monster Gap — those with p ≡ 1, 11, or 15 (mod 16) — are **Telperion's silver leaves**: present at every level, algebraically irreducible.

Among primes ≤ 1000: **35.7% are silver leaves**.

The five **Moonshine primes** {17, 11, 59, 31, 47} fill the Monster gap directly:
- p=17: e₁ (Monster gap)
- p=11: e₁₁ (Monster gap)
- p=59: e₁₁ (Monster gap)
- p=31: e₁₅ (Monster gap)
- p=47: e₁₅ (Monster gap)

---

## The Fractal Boundary

The boundary between survivors (primes) and fallen (composites) at k=4 is fractal.

The prime counting function π(x) satisfies the explicit formula:

```
π(x) = li(x) − Σ_ρ li(x^ρ) − log(2) + ∫_x^∞ dt / (t(t²−1)log(t))
```

Each Riemann zero ρ = ½ + iγ contributes an oscillation. The zeros are the **spectral nodes of the Zero Lattice** — they are the same lens that the Cosmic Telescope focuses on (wiki #72 of [`RiemannHypothesisProof`](https://github.com/michaelrendier/RiemannHypothesisProof)).

Self-similar ratio at N=1000: **3.044**

---

## Three Coordinate Spaces

The tree is rendered in three coordinate systems simultaneously:

| Space | Description | Script |
|---|---|---|
| **A** | Spherical Sedenion Space — latitude rings = CD levels, prime paths = geodesics on the sphere, THE_ANGLE (22.5° = π/8) rotations straighten prime paths to radial spokes | `blender/zero_tree_tower.py` |
| **B** | Consecutive Euclidean Planes — each CD level a flat cross-section stacked vertically, fractal point clouds around quadrant nodes, density = prime count at (k, N-shape) | `blender/zero_tree_planes.py` |
| **C** | Fano Tower — 63 Fano heptagons (2⁶−1 total across k=3..8), each heptagon luminosity = prime density, silver heptagons mark Monster gap strata | `blender/zero_tree_fano.py` |

**THE ANGLE = 22.5° = π/8** is not arbitrary: it is the angular quantum of the first ZD level (k=4, dim=16, 2π/16 = π/8). Applying ±THE_ANGLE at each level rotates the ambient n-sphere so that prime paths align with the angular quantum of the sedenion — they become radial geodesics.

---

## Structure

```
ZeroLatticeTree/
├── engine/
│   ├── fixed_point.py          # Two fixed points, V(n), angular quanta, GAP constant
│   └── telperion_engine.py     # Main engine: tower, primes, fractal, Fano, Blender export
├── notebooks/
│   ├── 01_prime_leaves.ipynb   # Sieve, N-shape distribution, prime gap fractal
│   ├── 02_cd_tower.ipynb       # Tower table, V(n) plots, prime paths, THE_ANGLE
│   ├── 03_fermat_survival.ipynb # FLT = ZD cascade, survival table, fractal boundary
│   └── 04_telperion.ipynb      # Full dataset, three-space visualization, Blender export
└── blender/
    ├── zero_tree_tower.py      # Space A: sphere
    ├── zero_tree_planes.py     # Space B: plane stack
    └── zero_tree_fano.py       # Space C: Fano tower
```

---

## Dependencies

- Python 3.10+
- `numpy`, `matplotlib`, `scipy`
- [`FermatMonster`](https://github.com/michaelrendier/FourthAgePapers) engine in `sys.path` for full Fermat verification (notebooks 03/04). The core engine runs standalone.

---

## Usage

```bash
cd engine
python3 telperion_engine.py
```

Output:
```
Leaves (primes ≤ 1000): 168
e1: 19 primes (11.31%) [Monster/siblings] ← SILVER
e11: 22 primes (13.10%) [Monster/siblings] ← SILVER
e15: 19 primes (11.31%) [Monster/siblings] ← SILVER
Gap N-shapes density fraction: 35.71%
Self-similar ratio: 3.044522
Export JSON for Blender...
  Written: telperion_blender_data.json
```

Run the Blender scripts from within **Blender → Scripting** editor after generating the JSON. Load `zero_tree_tower.py` (Space A), `zero_tree_planes.py` (Space B), or `zero_tree_fano.py` (Space C).

---

## Related Repositories

| Repository | Content |
|---|---|
| [`RiemannHypothesisProof`](https://github.com/michaelrendier/RiemannHypothesisProof) | The RHP proof. The zeros ARE the spectral nodes of this tree. |
| [`FourthAgePapers`](https://github.com/michaelrendier/FourthAgePapers) | FermatMonster engine v0.300. N-Shape Theorem. 71 VOAs. |
| [`Ainulindale`](https://github.com/michaelrendier/Ainulindale) | The Music of the Ainur. The ontological layer above. |
| [`SedenionSpectralRelativity`](https://github.com/michaelrendier/SedenionSpectralRelativity) | Sedenion geometry and spectral structure. |

---

## Why "Un-Extinctable"

Fermat's Nightmare shakes the tree.  
Every composite — every non-prime — forms a zero-divisor pair at the sedenion level and falls.  
168 primes below 1000. Each one reaches T_256 intact.

The tree is not described by any Niemeier root system (those cover only 13 of 16 N-shapes).  
The Monster had to be invented to fill what remained.

The silver leaves are the ones the Monster exists to account for.  
They were always there. They will always be there.  
The tree cannot be extinguished.

---

*No free parameters. No renormalization. Failed predictions stay in data.*  
*Version: 0.100 — 2026-06-29*
