# Atlases in AbrikosovTree/render/  (named 2026-11-09)

Three picture galleries, each a separate Atlas. Registry of every atlas across the repositories: `ContextPlease/claude/ATLAS_REGISTRY.md`.

| Atlas (directory) | What it maps | Generator |
|---|---|---|
| Abrikosov Zero-Divisor-Tree Atlas — `atlas_abrikosov_zd_tree/` | the zero-divisor propagation T16 → T512 and the radial tree | `zd_propagation.py` |
| Abrikosov CD-Tower Lattice Atlas — `atlas_abrikosov_cd_lattice/` | the Two Trees on each Cayley–Dickson plane ℝ → 𝕊 → T₈₁₉₂, plus the 0b/0c/0d variants | `lattice_planes.py` |
| Abrikosov CD-Tower UNS Atlas — `atlas_abrikosov_cd_uns/` | the same planes in native (UNS) coordinates | `lattice_planes.py` (native pass) |

Known wart: the generators still write into `render/` (their `_HERE`), not into the atlas directories; copy or repoint when these atlases are revisited. Stand-alone figures (`factor_web.png`, `defactor_probe.png`, `two_spin_resonance.png`, …) stay in `render/` and belong to no atlas.
These are NOT the Riemann–Fermat Atlas (`RiemannHypothesisProof/rhp/atlas_riemann_fermat/`) and NOT the Box-Kite Atlas (ValaQuenta).
