"""
Zero Tree — Space B: Consecutive Euclidean Planes
Paper: "How an Addition EQUALS a Subtraction"
Engine: ValaQuenta/zero_lattice.py v0.100

Run inside Blender: Scripting editor → Run Script.

COORDINATE SYSTEM B — CONSECUTIVE EUCLIDEAN PLANES
----------------------------------------------------
Each CD level k occupies its own horizontal plane at height z = σ × Z_SCALE.
Leaves (primes, k=0) at the top.  Root (T_256, k=8) at the bottom.

  k=0  ℝ      z=+4.0  σ=+1.00  ← top: prime leaves (The Unit)
  k=1  ℂ      z=+3.0  σ=+0.75
  k=2  ℍ      z=+2.0  σ=+0.50  ← gravastar shell / critical line
  k=3  𝕆      z=+1.0  σ=+0.25
  k=4  𝕊      z= 0.0  σ= 0.00  ← first ZD / equator (composites fall here)
  k=5  t_32   z=−1.0  σ=−0.25
  k=6  t_64   z=−2.0  σ=−0.50
  k=7  t_128  z=−3.0  σ=−0.75
  k=8  T_256  z=−4.0  σ=−1.00  ← bottom: root / 32 Fano planes

FRACTAL BOUNDARY
----------------
At each level k, a fractal point cloud surrounds each of the 4 quadrant nodes.
Cloud radius at node (k, quadrant q) = f(prime density at that N-shape group, k).
Density scales as (count/max_count)^(1/log₂(k+2)):
    At low k: differences are smoothed (full circle visible).
    At high k: differences amplified (fractal structure sharp).

Monster gap primes (p ≡ 1,11,15 mod 16) → silver cloud.
Niemeier primes (all other odd p mod 16) → blue cloud.
The k=4 equator plane is where the fractal boundary is most visible:
    composites fell here, leaving only prime paths.

n-SPHERE ROTATION
-----------------
At each level k, the 4 quadrant nodes are at base_deg + q×90°.
Odd k (J_red): base_deg = 0° → rotated +22.5° = THE ANGLE.
Even k (J_blue): base_deg = 45° → rotated −22.5°.
With rotation: all prime paths align to radial spokes (geodesics on the plane stack).
Toggle APPLY_THE_ANGLE to see both configurations.
"""

import bpy
import math
import json
import os
from mathutils import Vector

# ── Configuration ──────────────────────────────────────────────────────────────

Z_SCALE          = 1.5     # Blender units per sigma unit (total height = 4 × Z_SCALE × 2)
PLANE_RADIUS     = 2.0     # radius of quadrant node ring in each plane
NODE_RADIUS      = 0.10    # structural node sphere size
POLE_RADIUS      = 0.18    # leaf / root pole size
EDGE_RADIUS      = 0.015   # braid edge cylinder radius
ZD_RADIUS        = 0.025   # ZD crossing edge radius at k=4 equator
CLOUD_RADIUS     = 0.035   # fractal cloud point size

APPLY_THE_ANGLE  = True    # True: rotate each n-sphere to straighten prime paths
THE_ANGLE        = 22.5    # degrees

# Fractal cloud: how many points per density unit
CLOUD_DENSITY_SCALE = 40   # N_points_per_node = int(density × CLOUD_DENSITY_SCALE)
CLOUD_SPREAD        = 0.6  # max radial scatter in Blender units

# Load Telperion data from engine output (if available)
_SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
_DATA_PATH   = os.path.join(os.path.dirname(_SCRIPT_DIR), 'telperion_blender_data.json')
_DATA        = None
if os.path.exists(_DATA_PATH):
    with open(_DATA_PATH) as f:
        _DATA = json.load(f)


# ── Level data (mirrors telperion_engine, self-contained for Blender) ──────────

LEVEL_NAMES = {0:'ℝ',1:'ℂ',2:'ℍ',3:'𝕆',4:'𝕊',5:'t_32',6:'t_64',7:'t_128',8:'T_256'}
NIEMEIER_GAP = {1, 11, 15}

def level_data(k):
    sigma    = 1.0 - k / 4.0
    z        = sigma * Z_SCALE
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
            base_deg += THE_ANGLE
        elif j_type == 'J_blue':
            base_deg -= THE_ANGLE
    return {
        'k': k, 'name': LEVEL_NAMES[k], 'sigma': sigma, 'z': z,
        'j_type': j_type, 'base_deg': base_deg,
        'is_leaf': k == 0, 'is_root': k == 8,
        'is_gravastar': k == 2, 'is_first_zd': k == 4,
        'is_zd': k >= 4,
    }

LEVELS = [level_data(k) for k in range(9)]


def node_pos(k, i):
    """Position of quadrant node i at CD level k in the plane stack."""
    lv  = LEVELS[k]
    phi = math.radians(lv['base_deg'] + i * 90.0)
    r   = PLANE_RADIUS if k > 0 else 0.0
    return Vector((r * math.cos(phi), r * math.sin(phi), lv['z']))

positions = [[node_pos(k, i) for i in range(4)] for k in range(9)]


# ── Fractal cloud: prime density per node ─────────────────────────────────────

def fractal_cloud_params(k):
    """
    Returns density parameters for the fractal cloud at each level k.
    Uses pre-computed JSON data if available, otherwise uses analytic estimate.

    density[ns] ∈ [0,1]: fraction of prime leaves at N-shape ns.
    """
    if _DATA is not None:
        bdata = _DATA.get('boundary_contours', {}).get(str(k), [])
        ns_to_count = {entry['ns']: entry['count'] for entry in bdata}
        total = sum(ns_to_count.values()) or 1
        return {ns: ns_to_count.get(ns, 0) / total for ns in range(16)}
    else:
        # Analytic: each odd N-shape ~ 1/8, even ~ 0 (except ns=0 for p=2)
        d = {ns: (0.125 if ns % 2 == 1 else (0.01 if ns == 0 else 0.0)) for ns in range(16)}
        return d


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
    'leaf':       mat_emit   ('leaf_R',       (1.00, 1.00, 1.00), strength=5.0),
    'root':       mat_emit   ('root_T256',    (0.45, 0.00, 0.70), strength=5.0),
    'gravastar':  mat_emit   ('gravastar',    (1.00, 0.78, 0.00), strength=2.5),
    'first_zd':   mat_emit   ('first_zd',     (0.00, 0.85, 0.85), strength=2.5),
    'j_red':      mat_diffuse('j_red',        (0.75, 0.18, 0.06)),
    'j_blue':     mat_diffuse('j_blue',       (0.10, 0.28, 0.82)),
    'braid':      mat_emit   ('braid_edge',   (0.30, 0.30, 0.30), strength=0.5),
    'zd_cross':   mat_emit   ('zd_cross',     (0.90, 0.90, 0.90), strength=1.2),
    'zd_diag':    mat_emit   ('zd_diagonal',  (1.00, 0.78, 0.00), strength=2.0),
    'plane_guide':mat_emit   ('plane_guide',  (0.08, 0.08, 0.12), strength=0.2),
    # Fractal cloud materials
    'cloud_gap':  mat_emit   ('cloud_gap',    (0.95, 0.95, 0.95), strength=1.5),   # silver
    'cloud_niem': mat_emit   ('cloud_niemer', (0.20, 0.40, 0.80), strength=0.8),   # blue
    'cloud_even': mat_emit   ('cloud_even',   (0.30, 0.30, 0.30), strength=0.3),   # grey
}


# ── Helper: cylinder ─────────────────────────────────────────────────────────

def add_cylinder(p1, p2, radius, mat, name, collection):
    d = p2 - p1
    if d.length < 1e-6:
        return None
    mid = (p1 + p2) / 2.0
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=d.length, vertices=6, location=mid)
    obj = bpy.context.active_object
    obj.name = name
    z_ax = Vector((0, 0, 1))
    dn   = d.normalized()
    if (z_ax - dn).length > 1e-6 and (z_ax + dn).length > 1e-6:
        q = z_ax.rotation_difference(dn)
        obj.rotation_mode       = 'QUATERNION'
        obj.rotation_quaternion = q
    elif (z_ax + dn).length < 1e-6:
        obj.rotation_euler = (math.pi, 0, 0)
    obj.data.materials.append(mat)
    for c in obj.users_collection:
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


# ── Helper: scatter point (fractal cloud) ─────────────────────────────────────

def add_cloud_point(loc, mat, name, collection, size=CLOUD_RADIUS):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=size, location=loc, segments=6, ring_count=4)
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(mat)
    for c in obj.users_collection:
        c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


# ── Scene reset ────────────────────────────────────────────────────────────────

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for col in list(bpy.data.collections):
    bpy.data.collections.remove(col)


# ── Collections ────────────────────────────────────────────────────────────────

col_nodes    = bpy.data.collections.new('Nodes')
col_braid    = bpy.data.collections.new('Braid_edges')
col_zd       = bpy.data.collections.new('ZD_crossings')
col_planes   = bpy.data.collections.new('Plane_guides')
col_cloud    = bpy.data.collections.new('Fractal_cloud')
for col in [col_nodes, col_braid, col_zd, col_planes, col_cloud]:
    bpy.context.scene.collection.children.link(col)


# ── Plane guide disks (wireframe, one per level) ──────────────────────────────

for k in range(9):
    lv = LEVELS[k]
    bpy.ops.mesh.primitive_circle_add(
        vertices=64, radius=PLANE_RADIUS * 1.3, fill_type='NOTHING',
        location=(0, 0, lv['z']))
    obj      = bpy.context.active_object
    obj.name = f'plane_guide_k{k}'
    obj.data.materials.append(MAT['plane_guide'])
    for c in obj.users_collection:
        c.objects.unlink(obj)
    col_planes.objects.link(obj)


# ── Structural nodes ──────────────────────────────────────────────────────────

import random
random.seed(42)

node_objects = {}

for k in range(9):
    lv = LEVELS[k]
    r  = NODE_RADIUS if not (lv['is_leaf'] or lv['is_root']) else POLE_RADIUS
    for i in range(4):
        pos = positions[k][i]
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=r, location=pos, segments=12, ring_count=8)
        obj      = bpy.context.active_object
        obj.name = f'{lv["name"]}_Q{i}'

        if lv['is_leaf']:        obj.data.materials.append(MAT['leaf'])
        elif lv['is_root']:      obj.data.materials.append(MAT['root'])
        elif lv['is_gravastar']: obj.data.materials.append(MAT['gravastar'])
        elif lv['is_first_zd']:  obj.data.materials.append(MAT['first_zd'])
        elif lv['j_type'] == 'J_red':  obj.data.materials.append(MAT['j_red'])
        else:                          obj.data.materials.append(MAT['j_blue'])

        for c in obj.users_collection:
            c.objects.unlink(obj)
        col_nodes.objects.link(obj)
        node_objects[(k, i)] = obj

# Single leaf marker at top (The Unit)
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=POLE_RADIUS * 1.4, location=(0, 0, LEVELS[0]['z']),
    segments=20, ring_count=14)
obj = bpy.context.active_object; obj.name = 'ℝ_leaf_marker'
obj.data.materials.append(MAT['leaf'])
for c in obj.users_collection: c.objects.unlink(obj)
col_nodes.objects.link(obj)

# Root marker at bottom
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=POLE_RADIUS * 1.4, location=(0, 0, LEVELS[8]['z']),
    segments=20, ring_count=14)
obj = bpy.context.active_object; obj.name = 'T256_root_marker'
obj.data.materials.append(MAT['root'])
for c in obj.users_collection: c.objects.unlink(obj)
col_nodes.objects.link(obj)


# ── Braid edges (vertical beams through the tower) ────────────────────────────
#
# Pattern: node Q_i at level k → Q_i and Q_{i-1 mod 4} at level k+1.
# Same as the sphere version but in plane-stack coordinates.

for k in range(8):
    for i in range(4):
        p_curr      = positions[k][i]
        p_next_same = positions[k+1][i]
        p_next_prev = positions[k+1][(i - 1) % 4]
        add_cylinder(p_curr, p_next_same, EDGE_RADIUS, MAT['braid'],
                     f'braid_k{k}Q{i}_same', col_braid)
        add_cylinder(p_curr, p_next_prev, EDGE_RADIUS, MAT['braid'],
                     f'braid_k{k}Q{i}_prev', col_braid)


# ── ZD crossings at k=4 (equatorial plane) ───────────────────────────────────

eq = positions[4]
for ia, ib in [(0,1),(1,2),(2,3),(3,0)]:
    add_cylinder(eq[ia], eq[ib], ZD_RADIUS, MAT['zd_cross'],
                 f'ZD_adj_Q{ia}Q{ib}', col_zd)
for ia, ib in [(0,2),(1,3)]:
    add_cylinder(eq[ia], eq[ib], ZD_RADIUS*1.3, MAT['zd_diag'],
                 f'ZD_monster_Q{ia}Q{ib}', col_zd)


# ── Fractal cloud (prime density around each quadrant node) ───────────────────
#
# At each level k and quadrant i, scatter N_pts small spheres.
# N_pts = density × CLOUD_DENSITY_SCALE, where density is the fraction of
# primes whose N-shape maps to this quadrant at level k.
#
# N-shape → quadrant mapping:
#   quadrant i covers N-shapes {ns : ns % 4 == i}
# (so q=0 → ns ∈ {0,4,8,12}, q=1 → {1,5,9,13}, q=2 → {2,6,10,14}, q=3 → {3,7,11,15})
#
# Monster gap check: ns ∈ {1,11,15} → silver cloud.

for k in range(9):
    lv        = LEVELS[k]
    densities = fractal_cloud_params(k)

    for i in range(4):
        # Which N-shapes map to quadrant i?
        quad_ns     = [ns for ns in range(16) if ns % 4 == i]
        quad_density = sum(densities.get(ns, 0) for ns in quad_ns)
        has_gap      = any(ns in NIEMEIER_GAP for ns in quad_ns)

        n_pts  = int(quad_density * CLOUD_DENSITY_SCALE)
        if n_pts == 0:
            continue

        center = positions[k][i]
        # Fractal exponent: at higher k, magnify density differences
        exponent = 1.0 / math.log2(k + 2) if k >= 0 else 1.0
        r_cloud  = CLOUD_SPREAD * (quad_density ** exponent)

        cloud_mat = MAT['cloud_gap'] if has_gap else MAT['cloud_niem']

        for pt in range(n_pts):
            # Spread in the plane (random angle, Gaussian radius for fractal character)
            angle_pt = random.uniform(0, 2 * math.pi)
            # Gaussian spread: creates fractal-like density falloff
            r_pt = abs(random.gauss(0, r_cloud * 0.4))
            r_pt = min(r_pt, r_cloud)
            # Add small z-jitter to give volume
            z_jitter = random.gauss(0, 0.04)
            loc = Vector((
                center.x + r_pt * math.cos(angle_pt),
                center.y + r_pt * math.sin(angle_pt),
                center.z + z_jitter,
            ))
            add_cloud_point(loc, cloud_mat,
                            f'cloud_k{k}_Q{i}_pt{pt}', col_cloud,
                            size=CLOUD_RADIUS * random.uniform(0.5, 1.3))

# Extra cloud density at k=4 boundary — this IS the fractal edge
# where composites fell; emphasize with more points
k_zd = 4
densities_zd = fractal_cloud_params(k_zd)
for i in range(4):
    quad_ns      = [ns for ns in range(16) if ns % 4 == i]
    quad_density = sum(densities_zd.get(ns, 0) for ns in quad_ns)
    has_gap      = any(ns in NIEMEIER_GAP for ns in quad_ns)
    n_extra      = int(quad_density * CLOUD_DENSITY_SCALE * 1.5)  # extra emphasis at ZD
    center       = positions[k_zd][i]
    cloud_mat    = MAT['cloud_gap'] if has_gap else MAT['cloud_niem']
    for pt in range(n_extra):
        angle_pt = random.uniform(0, 2 * math.pi)
        r_pt     = abs(random.gauss(0, CLOUD_SPREAD * 0.5))
        r_pt     = min(r_pt, CLOUD_SPREAD * 1.5)
        loc = Vector((
            center.x + r_pt * math.cos(angle_pt),
            center.y + r_pt * math.sin(angle_pt),
            center.z + random.gauss(0, 0.08),
        ))
        add_cloud_point(loc, cloud_mat,
                        f'cloud_ZD_extra_Q{i}_pt{pt}', col_cloud,
                        size=CLOUD_RADIUS * random.uniform(0.4, 0.9))


# ── Camera ────────────────────────────────────────────────────────────────────

bpy.ops.object.camera_add(location=(6.5, -5.0, 2.0))
cam = bpy.context.active_object
cam.name = 'ZeroTree_planes_cam'
cam.data.lens = 50
cam.rotation_euler = (math.radians(75), 0, math.radians(52))
bpy.context.scene.camera = cam


# ── Lighting ──────────────────────────────────────────────────────────────────

bpy.ops.object.light_add(type='AREA', location=(5, 3, 5))
key = bpy.context.active_object; key.name = 'Key'
key.data.energy = 500; key.data.size = 5.0

bpy.ops.object.light_add(type='AREA', location=(-4, -4, 2))
fill = bpy.context.active_object; fill.name = 'Fill'
fill.data.energy = 200; fill.data.size = 7.0

# Root glow (purple, bottom)
bpy.ops.object.light_add(type='POINT', location=(0, 0, LEVELS[8]['z'] - 0.8))
root_g = bpy.context.active_object; root_g.name = 'Root_glow'
root_g.data.energy = 120; root_g.data.color = (0.45, 0.0, 0.70)

# Leaf glow (white, top)
bpy.ops.object.light_add(type='POINT', location=(0, 0, LEVELS[0]['z'] + 0.8))
leaf_g = bpy.context.active_object; leaf_g.name = 'Leaf_glow'
leaf_g.data.energy = 60; leaf_g.data.color = (1.0, 1.0, 1.0)

# ZD equator rim (cyan)
bpy.ops.object.light_add(type='POINT', location=(PLANE_RADIUS + 1, 0, 0))
zd_g = bpy.context.active_object; zd_g.name = 'ZD_glow'
zd_g.data.energy = 80; zd_g.data.color = (0.0, 0.85, 0.85)


# ── World ─────────────────────────────────────────────────────────────────────

world = bpy.context.scene.world or bpy.data.worlds.new('World')
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value    = (0.008, 0.008, 0.015, 1.0)
    bg.inputs['Strength'].default_value = 0.04


# ── Render ────────────────────────────────────────────────────────────────────

scene = bpy.context.scene
scene.render.engine           = 'CYCLES'
scene.cycles.samples          = 128
scene.render.resolution_x     = 1920
scene.render.resolution_y     = 1080
scene.render.film_transparent = True


# ── Summary ───────────────────────────────────────────────────────────────────

print()
print('=' * 64)
print('ZERO TREE — SPACE B: CONSECUTIVE EUCLIDEAN PLANES')
print('Paper: \'How an Addition EQUALS a Subtraction\'')
print('=' * 64)
print()
print('  Level   Name      sigma    z-pos   J-type    base°   Cloud')
print('  ' + '─' * 60)
for lv in LEVELS:
    cloud_msg = 'fractal boundary' if lv['is_first_zd'] else ''
    if lv['is_leaf']:  cloud_msg = 'prime leaves (Telperion white)'
    if lv['is_root']:  cloud_msg = 'root (T_256, purple)'
    print(f'  k={lv["k"]}  {lv["name"]:<8}  {lv["sigma"]:+.3f}  '
          f'z={lv["z"]:+.2f}  {lv["j_type"]:<8}  {lv["base_deg"]:5.1f}°  {cloud_msg}')
print()
print(f'  APPLY_THE_ANGLE = {APPLY_THE_ANGLE}')
print(f'  Data source: {"telperion_blender_data.json" if _DATA else "analytic (run telperion_engine.py first)"}')
print('=' * 64)
