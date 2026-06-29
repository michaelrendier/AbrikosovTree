"""
Zero Tree — Sedenion Sphere Tower
Paper: "How an Addition EQUALS a Subtraction"
Engine: ValaQuenta/zero_lattice.py v0.100

Run inside Blender: Scripting editor → Run Script.

STRUCTURE
---------
9 CD levels (ℝ to T_256) arranged as latitude rings on a sphere.
Each level: 4 quadrant nodes at 90° intervals.
Adjacent levels rotate 45° (the Cayley-Dickson doubling step).
This is inherently 3D — the 4-quadrant cross at each latitude lies on the
sphere surface, not in a separate Euclidean plane.

Latitude mapping:
  theta = k × π/8   (polar angle, 0 = north pole = ℝ, π = south pole = T_256)

  k=0  ℝ      sigma=+1.00  theta= 0°     north pole — leaves (collapse to point)
  k=1  ℂ      sigma=+0.75  theta=22.5°
  k=2  ℍ      sigma=+0.50  theta=45.0°   ← gravastar shell / critical line
  k=3  𝕆      sigma=+0.25  theta=67.5°
  k=4  𝕊      sigma= 0.00  theta=90.0°   ← equator / first ZD level
  k=5  t_32   sigma=−0.25  theta=112.5°
  k=6  t_64   sigma=−0.50  theta=135.0°
  k=7  t_128  sigma=−0.75  theta=157.5°
  k=8  T_256  sigma=−1.00  theta=180.0°  south pole — root (collapse to point)

Quadrant rotation:
  Odd  k (k=1,3,5,7): J_red,  base = 0°   — sectors at 0°/90°/180°/270°
  Even k (k=2,4,6,8): J_blue, base = 45°  — sectors at 45°/135°/225°/315°
  k=0: single real point (The Unit) — no sector distinction

Node positions on sphere of radius R:
  x = R · sin(theta) · cos(phi_i)
  y = R · sin(theta) · sin(phi_i)
  z = R · cos(theta)
  phi_i = base_deg + i × 90°,  i = 0..3

Tower edges:
  Each node at level k connects to its two nearest angular neighbours at k+1.
  Adjacent levels are offset ±45°, so each node fans to the two flanking nodes.
  This creates a spiral braid through the sphere from leaf (north) to root (south).

ZD crossings (at k=4 equatorial ring):
  All 6 pairs of the 4 equatorial nodes are connected.
  These represent the ZD constellation structure at the sedenion level.
  Monster gap signature: Q1↔Q3 diagonal (90°↔270° offset from base).
"""

import bpy
import math
from mathutils import Vector


# ── Configuration ─────────────────────────────────────────────────────────────

R             = 3.0     # sphere radius (Blender units)
NODE_RADIUS   = 0.12    # sphere node size
BRAID_RADIUS  = 0.018   # tree-edge cylinder radius (level → level)
ZD_RADIUS     = 0.030   # ZD crossing edge radius (equatorial)
POLE_RADIUS   = 0.22    # size of root / leaf pole markers

APPLY_THE_ANGLE = False  # True: rotate each level by THE ANGLE (π/8) relative to base
                          # Straightens ZD paths into radial spokes


# ── Level data ────────────────────────────────────────────────────────────────

LEVEL_NAMES = {
    0: 'ℝ',
    1: 'ℂ',
    2: 'ℍ',
    3: '𝕆',
    4: '𝕊',
    5: 't_32',
    6: 't_64',
    7: 't_128',
    8: 'T_256',
}

def level_data(k):
    sigma     = 1.0 - k / 4.0
    theta     = k * math.pi / 8.0        # polar angle on sphere
    if k == 0:
        j_type   = 'real'
        base_deg = 0.0
    elif k % 2 == 1:
        j_type   = 'J_red'
        base_deg = 0.0
    else:
        j_type   = 'J_blue'
        base_deg = 45.0
    if APPLY_THE_ANGLE:
        if j_type == 'J_red':
            base_deg += 22.5
        elif j_type == 'J_blue':
            base_deg -= 22.5
    return {
        'k':        k,
        'sigma':    sigma,
        'theta':    theta,
        'j_type':   j_type,
        'base_deg': base_deg,
        'name':     LEVEL_NAMES[k],
        'is_root':  k == 8,
        'is_leaf':  k == 0,
        'is_gravastar': k == 2,
        'is_first_zd':  k == 4,
    }

LEVELS = [level_data(k) for k in range(9)]


# ── Node positions ─────────────────────────────────────────────────────────────

def node_pos(k, i):
    """
    3D position of quadrant node i at CD level k.
    Lies on the sphere surface of radius R.
    At k=0 and k=8 all 4 quadrant nodes converge to the pole.
    """
    lv    = LEVELS[k]
    theta = lv['theta']
    phi   = math.radians(lv['base_deg'] + i * 90.0)
    x     = R * math.sin(theta) * math.cos(phi)
    y     = R * math.sin(theta) * math.sin(phi)
    z     = R * math.cos(theta)
    return Vector((x, y, z))

# Pre-compute all 36 positions: positions[k][i]
positions = [[node_pos(k, i) for i in range(4)] for k in range(9)]


# ── Scene reset ───────────────────────────────────────────────────────────────

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for col in list(bpy.data.collections):
    bpy.data.collections.remove(col)


# ── Collections ───────────────────────────────────────────────────────────────

col_nodes  = bpy.data.collections.new('Nodes')
col_braid  = bpy.data.collections.new('Braid_edges')
col_zd     = bpy.data.collections.new('ZD_crossings')
col_sphere = bpy.data.collections.new('Reference')
for col in [col_nodes, col_braid, col_zd, col_sphere]:
    bpy.context.scene.collection.children.link(col)


# ── Materials ─────────────────────────────────────────────────────────────────

def mat_emit(name, rgb, strength=2.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.node_tree.nodes.clear()
    out  = m.node_tree.nodes.new('ShaderNodeOutputMaterial')
    emit = m.node_tree.nodes.new('ShaderNodeEmission')
    emit.inputs['Color'].default_value    = (*rgb, 1.0)
    emit.inputs['Strength'].default_value = strength
    m.node_tree.links.new(emit.outputs['Emission'], out.inputs['Surface'])
    return m

def mat_diffuse(name, rgb, roughness=0.35):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1.0)
    b.inputs['Roughness'].default_value  = roughness
    b.inputs['Metallic'].default_value   = 0.1
    return m

MAT = {
    'leaf':       mat_emit   ('leaf_R',      (1.00, 1.00, 1.00), strength=4.0),
    'root':       mat_emit   ('root_T256',   (0.45, 0.00, 0.70), strength=5.0),
    'gravastar':  mat_emit   ('gravastar',   (1.00, 0.78, 0.00), strength=2.5),
    'first_zd':   mat_emit   ('first_zd',    (0.00, 0.85, 0.85), strength=2.5),
    'j_red':      mat_diffuse('j_red',       (0.75, 0.18, 0.06)),
    'j_blue':     mat_diffuse('j_blue',      (0.10, 0.28, 0.82)),
    'braid':      mat_emit   ('braid_edge',  (0.30, 0.30, 0.30), strength=0.6),
    'zd_cross':   mat_emit   ('zd_cross',    (0.90, 0.90, 0.90), strength=1.2),
    'zd_diag':    mat_emit   ('zd_diagonal', (1.00, 0.78, 0.00), strength=2.0),
    'sphere_ref': mat_diffuse('sphere_ref',  (0.05, 0.05, 0.08), roughness=0.9),
}


# ── Helper: cylinder from p1 to p2 ────────────────────────────────────────────

def add_cylinder(p1, p2, radius, mat, name, collection):
    direction = p2 - p1
    length    = direction.length
    if length < 1e-6:
        return None
    midpoint = (p1 + p2) / 2.0

    bpy.ops.mesh.primitive_cylinder_add(
        radius   = radius,
        depth    = length,
        vertices = 6,
        location = midpoint,
    )
    obj      = bpy.context.active_object
    obj.name = name

    z_axis = Vector((0.0, 0.0, 1.0))
    d_norm = direction.normalized()
    if (z_axis - d_norm).length < 1e-6:
        pass
    elif (z_axis + d_norm).length < 1e-6:
        obj.rotation_euler = (math.pi, 0.0, 0.0)
    else:
        q = z_axis.rotation_difference(d_norm)
        obj.rotation_mode       = 'QUATERNION'
        obj.rotation_quaternion = q

    obj.data.materials.append(mat)
    for c in obj.users_collection:
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


# ── Reference sphere (wireframe ghost) ────────────────────────────────────────

bpy.ops.mesh.primitive_uv_sphere_add(radius=R, location=(0, 0, 0),
                                      segments=32, ring_count=16)
sphere_ref      = bpy.context.active_object
sphere_ref.name = 'Reference_sphere'
sphere_ref.data.materials.append(MAT['sphere_ref'])
sphere_ref.display_type = 'WIRE'
for c in sphere_ref.users_collection:
    c.objects.unlink(sphere_ref)
col_sphere.objects.link(sphere_ref)


# ── Nodes ─────────────────────────────────────────────────────────────────────

node_objects = {}   # (k, i) → obj

for k in range(9):
    lv = LEVELS[k]
    for i in range(4):
        pos = positions[k][i]

        bpy.ops.mesh.primitive_uv_sphere_add(
            radius     = NODE_RADIUS,
            location   = pos,
            segments   = 16,
            ring_count = 10,
        )
        obj      = bpy.context.active_object
        obj.name = f'{lv["name"]}_Q{i}'

        if lv['is_leaf']:
            obj.data.materials.append(MAT['leaf'])
        elif lv['is_root']:
            obj.data.materials.append(MAT['root'])
        elif lv['is_gravastar']:
            obj.data.materials.append(MAT['gravastar'])
        elif lv['is_first_zd']:
            obj.data.materials.append(MAT['first_zd'])
        elif lv['j_type'] == 'J_red':
            obj.data.materials.append(MAT['j_red'])
        else:
            obj.data.materials.append(MAT['j_blue'])

        for c in obj.users_collection:
            c.objects.unlink(obj)
        col_nodes.objects.link(obj)
        node_objects[(k, i)] = obj

# Larger pole markers (single central node for the degenerate poles)
for k, mat_key, name in [(0, 'leaf', 'ℝ_north_pole'), (8, 'root', 'T256_south_pole')]:
    z = R if k == 0 else -R
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius   = POLE_RADIUS,
        location = (0.0, 0.0, z),
        segments = 24, ring_count = 16,
    )
    obj      = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(MAT[mat_key])
    for c in obj.users_collection:
        c.objects.unlink(obj)
    col_nodes.objects.link(obj)


# ── Braid edges (tree structure, level k → k+1) ───────────────────────────────
#
# Each quadrant node at level k connects to the two nearest angular
# neighbours at level k+1. Adjacent levels are offset ±45°, so from
# 4 quadrants at 90° spacing, each node fans to the two flanking nodes.
#
# Pattern for J_red (0°/90°/180°/270°) → J_blue (45°/135°/225°/315°):
#   Q_i (at i*90°) → Q_i (at 45°+i*90°) and Q_{i-1 mod 4} (at 45°+(i-1)*90°)
#   i.e. the node "between" Q_i and Q_{i-1} at the next level.
#
# This is symmetric: the reverse (J_blue → J_red at k+1) uses the same offset.

for k in range(8):
    for i in range(4):
        p_curr = positions[k][i]
        # Two nearest at k+1: same index and previous index (both are ±45° away)
        p_next_same = positions[k+1][i]
        p_next_prev = positions[k+1][(i - 1) % 4]
        add_cylinder(p_curr, p_next_same, BRAID_RADIUS, MAT['braid'],
                     f'braid_k{k}Q{i}_to_k{k+1}Q{i}', col_braid)
        add_cylinder(p_curr, p_next_prev, BRAID_RADIUS, MAT['braid'],
                     f'braid_k{k}Q{i}_to_k{k+1}Q{(i-1)%4}', col_braid)


# ── ZD crossings at k=4 (equatorial ring, first ZD level) ────────────────────
#
# At the sedenion level (k=4, equator), all 4 quadrant nodes are connected
# pairwise. This represents the ZD constellation structure.
#
# 6 pairs total: (0,1), (0,2), (0,3), (1,2), (1,3), (2,3).
# The diagonal pair (0,2) and (1,3) — connecting opposite quadrants —
# carries the Monster gap signature and gets the gold material.
# Adjacent pairs (0,1),(1,2),(2,3),(3,0) get the white ZD material.

eq_positions = positions[4]

for ia, ib in [(0,1), (1,2), (2,3), (3,0)]:
    add_cylinder(eq_positions[ia], eq_positions[ib],
                 ZD_RADIUS, MAT['zd_cross'],
                 f'ZD_adj_Q{ia}Q{ib}', col_zd)

for ia, ib in [(0,2), (1,3)]:
    add_cylinder(eq_positions[ia], eq_positions[ib],
                 ZD_RADIUS * 1.3, MAT['zd_diag'],
                 f'ZD_monster_Q{ia}Q{ib}', col_zd)


# ── Latitude ring guides (faint arcs at key levels) ───────────────────────────
#
# Three ring guides:
#   k=2  (ℍ, σ=0.5, gravastar shell) — gold
#   k=4  (𝕊, σ=0.0, equator, first ZD) — cyan
#   k=2 and k=4 are the two physically significant levels

def add_latitude_ring(theta, radius, mat, name, n_segments=64):
    """Thin torus at given polar angle on the sphere."""
    z     = R * math.cos(theta)
    r_lat = R * math.sin(theta)
    if r_lat < 1e-4:
        return
    bpy.ops.mesh.primitive_torus_add(
        location           = (0.0, 0.0, z),
        major_radius       = r_lat,
        minor_radius       = radius,
        major_segments     = n_segments,
        minor_segments     = 8,
    )
    obj      = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    for c in obj.users_collection:
        c.objects.unlink(obj)
    col_sphere.objects.link(obj)

add_latitude_ring(LEVELS[2]['theta'], 0.012, MAT['gravastar'], 'ring_ℍ_gravastar')
add_latitude_ring(LEVELS[4]['theta'], 0.015, MAT['first_zd'],  'ring_𝕊_first_ZD')


# ── Camera ────────────────────────────────────────────────────────────────────

bpy.ops.object.camera_add(location=(7.0, -7.0, 3.5))
cam                 = bpy.context.active_object
cam.name            = 'ZeroTree_cam'
cam.data.lens       = 60
cam.rotation_euler  = (
    math.radians(72.0),
    0.0,
    math.radians(45.0),
)
bpy.context.scene.camera = cam


# ── Lighting ──────────────────────────────────────────────────────────────────

bpy.ops.object.light_add(type='AREA', location=(5.0, 3.0, 6.0))
key             = bpy.context.active_object
key.name        = 'Key'
key.data.energy = 600
key.data.size   = 4.0

bpy.ops.object.light_add(type='AREA', location=(-4.0, -5.0, 2.0))
fill             = bpy.context.active_object
fill.name        = 'Fill'
fill.data.energy = 200
fill.data.size   = 6.0

bpy.ops.object.light_add(type='POINT', location=(0.0, 0.0, -R - 1.0))
root_glow             = bpy.context.active_object
root_glow.name        = 'Root_glow'
root_glow.data.energy = 80
root_glow.data.color  = (0.45, 0.0, 0.70)

bpy.ops.object.light_add(type='POINT', location=(0.0, 0.0, R + 1.0))
leaf_glow             = bpy.context.active_object
leaf_glow.name        = 'Leaf_glow'
leaf_glow.data.energy = 40
leaf_glow.data.color  = (1.0, 1.0, 1.0)


# ── World ─────────────────────────────────────────────────────────────────────

world = bpy.context.scene.world or bpy.data.worlds.new('World')
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value    = (0.008, 0.008, 0.015, 1.0)
    bg.inputs['Strength'].default_value = 0.04


# ── Render ────────────────────────────────────────────────────────────────────

scene                         = bpy.context.scene
scene.render.engine           = 'CYCLES'
scene.cycles.samples          = 128
scene.render.resolution_x     = 1920
scene.render.resolution_y     = 1080
scene.render.film_transparent = True


# ── Summary ───────────────────────────────────────────────────────────────────

print()
print("=" * 64)
print("ZERO TREE — SEDENION SPHERE TOWER")
print("Paper: 'How an Addition EQUALS a Subtraction'")
print("=" * 64)
print()
print("  Sphere radius R =", R)
print()
print("  Level  Name    sigma    theta      J-type    base°  z-pos")
print("  " + "─" * 58)
for lv in LEVELS:
    z    = R * math.cos(lv['theta'])
    mark = ''
    if lv['is_leaf']:       mark = ' ← ℝ LEAF (north pole)'
    elif lv['is_root']:     mark = ' ← T_256 ROOT (south pole)'
    elif lv['is_gravastar']: mark = ' ← gravastar shell / σ=½'
    elif lv['is_first_zd']: mark = ' ← first ZD / equator'
    print(f"  k={lv['k']}    {lv['name']:<7} {lv['sigma']:+.2f}   "
          f"{math.degrees(lv['theta']):6.1f}°   {lv['j_type']:<8} "
          f"{lv['base_deg']:5.1f}°  z={z:+.3f}{mark}")

print()
print(f"  Total nodes:  {9*4} (9 levels × 4 quadrants)")
print(f"  Braid edges:  {8*4*2} (8 transitions × 4 nodes × 2 neighbours)")
print(f"  ZD crossings: 6 at equatorial k=4 (4 adjacent + 2 monster diagonals)")
print()
print("  APPLY_THE_ANGLE =", APPLY_THE_ANGLE)
if not APPLY_THE_ANGLE:
    print("  → Set True to rotate J_red +22.5° / J_blue −22.5°")
    print("    All quadrant nodes align to 22.5°/112.5°/202.5°/292.5°.")
    print("    ZD paths straighten into radial spokes along the meridians.")
print("=" * 64)
