"""
Zero Tree — Space C: Fano Tower / 32 Heptagons
Paper: "How an Addition EQUALS a Subtraction"
Engine: ValaQuenta/zero_lattice.py v0.100

Run inside Blender: Scripting editor → Run Script.

COORDINATE SYSTEM C — FANO TOWER
---------------------------------
The algebraic face of Telperion.  Same tree, same data.
Rendered as a tower of Fano planes (heptagons) instead of spheres or stacked planes.

The Fano plane F₇:
    7 points, 7 lines (each line has 3 points).
    The octonion multiplication table IS the Fano plane.
    Each point = one imaginary unit of 𝕆.
    Each line = one closed triple {eᵢ, eⱼ, eₖ}: eᵢeⱼ = ±eₖ (cyclic).

Number of Fano planes per CD level:
    k=0..2: 0   (no Fano structure — ℝ, ℂ, ℍ below the octonion)
    k=3:    1   (𝕆 = one Fano plane)
    k=4:    2   (𝕊 = two octonion sub-algebras)
    k=5:    4   (t_32)
    k=6:    8   (t_64)
    k=7:    16  (t_128)
    k=8:    32  (T_256 = 32 Fano planes)
    Total:  63 heptagons in the tower

FRACTAL BOUNDARY IN SPACE C
----------------------------
Each Fano heptagon is coloured by the number of prime paths that pass through it.
The N-shape of a prime (p mod 16) determines which Fano planes it activates.
At level k with n_fano planes: prime p activates plane fi = (p mod 16) % n_fano.

Silver heptagons: those covering Monster gap N-shapes {e₁, e₁₁, e₁₅}.
    - No Niemeier A/D/E root system can cover these planes.
    - Only Monster primes activate them.
    - These are Telperion's most un-extinctable paths.

Luminosity of each heptagon = (prime_count through this plane) / max_count.
The resulting pattern IS the fractal boundary — the Riemann spectrum stamped
onto the Fano algebra at every level of the tower.

LAYOUT
------
    k=8 (T_256, root):  bottom row,  32 heptagons  z = −4.0
    k=7 (t_128):        row,         16 heptagons  z = −3.0
    k=6 (t_64):         row,          8 heptagons  z = −2.0
    k=5 (t_32):         row,          4 heptagons  z = −1.0
    k=4 (𝕊, ZD):        row,          2 heptagons  z =  0.0
    k=3 (𝕆):            row,          1 heptagon   z = +1.0
    (k=0..2: structural poles only, no Fano plane)
"""

import bpy
import math
import json
import os
import random
from mathutils import Vector

# ── Configuration ──────────────────────────────────────────────────────────────

Z_SCALE         = 1.5     # Blender units per sigma unit
HEPT_SCALE      = 0.5     # heptagon vertex radius (inner)
HEPT_SPACING_X  = 1.4     # spacing between heptagons in a row
EDGE_THICK      = 0.018   # heptagon boundary edge thickness
INNER_THICK     = 0.010   # Fano inner-line (spoke) thickness
NODE_SIZE       = 0.055   # vertex sphere size
POLE_SIZE       = 0.18    # leaf/root pole marker size

# Load Telperion data (for prime density per Fano plane)
_SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
_DATA_PATH   = os.path.join(os.path.dirname(_SCRIPT_DIR), 'telperion_blender_data.json')
_DATA        = None
if os.path.exists(_DATA_PATH):
    with open(_DATA_PATH) as f:
        _DATA = json.load(f)

NIEMEIER_GAP = {1, 11, 15}
random.seed(42)

# ── Fano plane geometry ────────────────────────────────────────────────────────

FANO_LINES = [(1,2,4),(2,3,5),(3,4,6),(4,5,7),(5,6,1),(6,7,2),(7,1,3)]

def heptagon_vertex(i, scale=HEPT_SCALE):
    """Vertex i (1-indexed) on a regular heptagon, pointing up."""
    angle = math.pi / 2 + (i - 1) * 2 * math.pi / 7
    return (math.cos(angle) * scale, math.sin(angle) * scale)

HEPT_VERTS = {i: heptagon_vertex(i) for i in range(1, 8)}

# ── Level data ────────────────────────────────────────────────────────────────

LEVEL_NAMES = {0:'ℝ',1:'ℂ',2:'ℍ',3:'𝕆',4:'𝕊',5:'t_32',6:'t_64',7:'t_128',8:'T_256'}

def level_data(k):
    sigma  = 1.0 - k / 4.0
    n_fano = 2**(k-3) if k >= 3 else 0
    return {
        'k': k, 'name': LEVEL_NAMES[k], 'sigma': sigma,
        'z': sigma * Z_SCALE, 'n_fano': n_fano,
        'is_leaf': k == 0, 'is_root': k == 8,
        'is_gravastar': k == 2, 'is_first_zd': k == 4,
    }

LEVELS = [level_data(k) for k in range(9)]


# ── Prime density per Fano plane ──────────────────────────────────────────────

def fano_plane_densities(k, n_fano):
    """
    Return density[fi] = fraction of prime leaves that activate Fano plane fi at level k.
    Uses JSON data if available; falls back to analytic estimate.
    """
    if n_fano == 0:
        return {}

    if _DATA is not None:
        # Use boundary contour data: group N-shapes by fi = ns % n_fano
        bdata = _DATA.get('boundary_contours', {}).get(str(k), [])
        ns_to_count = {entry['ns']: entry['count'] for entry in bdata}
        total = max(sum(ns_to_count.values()), 1)
        fi_count = {fi: 0 for fi in range(n_fano)}
        for ns, cnt in ns_to_count.items():
            fi = int(ns) % n_fano
            fi_count[fi] += cnt
        max_fi = max(fi_count.values()) or 1
        return {fi: fi_count[fi] / max_fi for fi in range(n_fano)}
    else:
        # All planes equally activated (Dirichlet equidistribution)
        return {fi: 1.0 for fi in range(n_fano)}


def fano_covers_gap(fi, n_fano):
    """True if Fano plane fi at this level covers any Monster gap N-shape."""
    return any((ns % n_fano == fi) for ns in NIEMEIER_GAP)


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
    b.inputs['Metallic'].default_value   = 0.4
    return m

MAT_BASE = {
    'leaf':      mat_emit   ('leaf_R',     (1.00, 1.00, 1.00), strength=5.0),
    'root':      mat_emit   ('root_T256',  (0.45, 0.00, 0.70), strength=5.0),
    'gravastar': mat_emit   ('gravastar',  (1.00, 0.78, 0.00), strength=2.5),
    'zd':        mat_emit   ('zd_equator', (0.00, 0.85, 0.85), strength=2.0),
    'braid':     mat_emit   ('braid',      (0.25, 0.25, 0.30), strength=0.4),
    'pole_line': mat_emit   ('pole_line',  (0.20, 0.20, 0.25), strength=0.3),
}

def mat_fano_hept(name, brightness, is_gap):
    """Material for a Fano heptagon, modulated by prime density."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.node_tree.nodes.clear()
    out  = m.node_tree.nodes.new('ShaderNodeOutputMaterial')
    emit = m.node_tree.nodes.new('ShaderNodeEmission')
    if is_gap:
        rgb = (0.85 + 0.15 * brightness, 0.85 + 0.15 * brightness, 0.85 + 0.15 * brightness)
        strength = 1.5 + 3.0 * brightness
    else:
        rgb = (0.10 + 0.15 * brightness, 0.28 + 0.20 * brightness, 0.60 + 0.20 * brightness)
        strength = 0.5 + 1.5 * brightness
    emit.inputs['Color'].default_value    = (*rgb, 1.0)
    emit.inputs['Strength'].default_value = strength
    m.node_tree.links.new(emit.outputs['Emission'], out.inputs['Surface'])
    return m


# ── Helper: cylinder ──────────────────────────────────────────────────────────

def add_cylinder(p1, p2, radius, mat, name, collection):
    d = p2 - p1
    if d.length < 1e-6:
        return None
    mid = (p1 + p2) / 2.0
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=d.length, vertices=5, location=mid)
    obj = bpy.context.active_object; obj.name = name
    z_ax = Vector((0,0,1)); dn = d.normalized()
    if (z_ax - dn).length > 1e-6 and (z_ax + dn).length > 1e-6:
        q = z_ax.rotation_difference(dn)
        obj.rotation_mode = 'QUATERNION'; obj.rotation_quaternion = q
    elif (z_ax + dn).length < 1e-6:
        obj.rotation_euler = (math.pi, 0, 0)
    obj.data.materials.append(mat)
    for c in obj.users_collection: c.objects.unlink(obj)
    collection.objects.link(obj)
    return obj


# ── Build one Fano heptagon at (cx, cy, cz) ──────────────────────────────────

def build_fano_heptagon(cx, cy, cz, brightness, is_gap, name_prefix, col_hept, col_nodes):
    """
    Render one Fano plane as a heptagon + inner Fano lines.
    Vertex spheres at the 7 heptagon corners.
    7 boundary edges (the heptagon sides).
    7 inner Fano lines (the Fano structure: each line connects 3 non-adjacent vertices).
    """
    mat = mat_fano_hept(f'{name_prefix}_mat', brightness, is_gap)
    # Scale heptagon by brightness to show fractal density
    scale = HEPT_SCALE * (0.6 + 0.4 * max(brightness, 0.05))

    verts_3d = {}
    for i in range(1, 8):
        lx, ly = heptagon_vertex(i, scale=scale)
        pos = Vector((cx + lx, cy + ly, cz))
        verts_3d[i] = pos
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=NODE_SIZE * (0.5 + 0.5 * brightness),
            location=pos, segments=6, ring_count=4)
        node_obj = bpy.context.active_object
        node_obj.name = f'{name_prefix}_v{i}'
        node_obj.data.materials.append(mat)
        for c in node_obj.users_collection: c.objects.unlink(node_obj)
        col_nodes.objects.link(node_obj)

    # Heptagon boundary edges (7 consecutive vertex pairs)
    for i in range(1, 8):
        j = i % 7 + 1
        add_cylinder(verts_3d[i], verts_3d[j],
                     EDGE_THICK * max(brightness, 0.2), mat,
                     f'{name_prefix}_edge_{i}{j}', col_hept)

    # Inner Fano lines (7 lines, each connecting 3 non-adjacent vertices)
    for a, b, c in FANO_LINES:
        for x, y in [(a, b), (b, c), (a, c)]:
            add_cylinder(verts_3d[x], verts_3d[y],
                         INNER_THICK * max(brightness, 0.15), mat,
                         f'{name_prefix}_fano_{x}{y}', col_hept)


# ── Scene reset ────────────────────────────────────────────────────────────────

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for col in list(bpy.data.collections):
    bpy.data.collections.remove(col)


# ── Collections ────────────────────────────────────────────────────────────────

col_hept    = bpy.data.collections.new('Fano_heptagons')
col_verts   = bpy.data.collections.new('Fano_vertices')
col_poles   = bpy.data.collections.new('Poles')
col_braid   = bpy.data.collections.new('Tower_spine')
bpy.context.scene.collection.children.link(col_hept)
bpy.context.scene.collection.children.link(col_verts)
bpy.context.scene.collection.children.link(col_poles)
bpy.context.scene.collection.children.link(col_braid)


# ── Pole markers (k=0..2, no Fano plane) ─────────────────────────────────────

for k, mat_key in [(0,'leaf'), (2,'gravastar')]:
    lv = LEVELS[k]
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=POLE_SIZE, location=(0,0,lv['z']), segments=16, ring_count=10)
    obj = bpy.context.active_object; obj.name = f'{lv["name"]}_pole'
    obj.data.materials.append(MAT_BASE[mat_key])
    for c in obj.users_collection: c.objects.unlink(obj)
    col_poles.objects.link(obj)

# ℂ level (k=1): small marker
lv1 = LEVELS[1]
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=POLE_SIZE*0.5, location=(0,0,lv1['z']), segments=10, ring_count=6)
obj = bpy.context.active_object; obj.name = 'ℂ_pole'
obj.data.materials.append(MAT_BASE['braid'])
for c in obj.users_collection: c.objects.unlink(obj)
col_poles.objects.link(obj)


# ── Tower spine (vertical lines through pole levels) ─────────────────────────

for k in range(2):
    p1 = Vector((0,0,LEVELS[k]['z']))
    p2 = Vector((0,0,LEVELS[k+1]['z']))
    add_cylinder(p1, p2, 0.012, MAT_BASE['pole_line'],
                 f'spine_k{k}_k{k+1}', col_braid)
# From k=2 down to k=3 (first Fano level): connector
add_cylinder(Vector((0,0,LEVELS[2]['z'])), Vector((0,0,LEVELS[3]['z'])),
             0.012, MAT_BASE['pole_line'], 'spine_k2_k3', col_braid)


# ── Build the Fano tower ──────────────────────────────────────────────────────

# Track centre positions of each Fano plane for spine connections
fano_centres = {}  # (k, fi) -> Vector

for k in range(3, 9):
    lv    = LEVELS[k]
    n_f   = lv['n_fano']
    z     = lv['z']
    densities = fano_plane_densities(k, n_f)
    row_w = (n_f - 1) * HEPT_SPACING_X

    for fi in range(n_f):
        cx = -row_w / 2.0 + fi * HEPT_SPACING_X
        cy = 0.0
        brightness = densities.get(fi, 0.0)
        is_gap     = fano_covers_gap(fi, n_f)
        name_pfx   = f'fano_k{k}_fi{fi}'

        build_fano_heptagon(cx, cy, z, brightness, is_gap,
                            name_pfx, col_hept, col_verts)
        fano_centres[(k, fi)] = Vector((cx, cy, z))

    # ZD marker at k=4 equator
    if lv['is_first_zd'] and n_f > 0:
        for fi in range(n_f):
            ctr = fano_centres[(k, fi)]
            bpy.ops.mesh.primitive_torus_add(
                location=(ctr.x, ctr.y, ctr.z),
                major_radius=HEPT_SCALE * 1.1, minor_radius=0.018,
                major_segments=32, minor_segments=6)
            obj = bpy.context.active_object
            obj.name = f'ZD_ring_k{k}_fi{fi}'
            obj.data.materials.append(MAT_BASE['zd'])
            for c in obj.users_collection: c.objects.unlink(obj)
            col_hept.objects.link(obj)


# ── Spine connections between Fano levels ────────────────────────────────────
#
# Connect each Fano plane at level k to its parent(s) at level k-1.
# At level k with n_f planes and level k-1 with n_f/2 planes:
#   plane fi at level k → parent plane fi//2 at level k-1.
# (The CD doubling splits each parent into two children.)

for k in range(4, 9):
    n_f      = LEVELS[k]['n_fano']
    n_f_prev = LEVELS[k-1]['n_fano']
    if n_f_prev == 0:
        continue
    for fi in range(n_f):
        parent_fi = fi // 2
        p1 = fano_centres.get((k-1, parent_fi))
        p2 = fano_centres.get((k, fi))
        if p1 and p2:
            is_gap_conn = fano_covers_gap(fi, n_f)
            mat = MAT_BASE['leaf'] if is_gap_conn else MAT_BASE['braid']
            add_cylinder(p1, p2, 0.010, mat, f'spine_k{k-1}fi{parent_fi}_k{k}fi{fi}', col_braid)


# ── Root and leaf markers ─────────────────────────────────────────────────────

# Root (T_256, k=8): large purple sphere centred at the bottom row midpoint
lv8 = LEVELS[8]
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=POLE_SIZE*1.3, location=(0, -1.2, lv8['z'] - 0.5), segments=20, ring_count=14)
obj = bpy.context.active_object; obj.name = 'T256_root_marker'
obj.data.materials.append(MAT_BASE['root'])
for c in obj.users_collection: c.objects.unlink(obj)
col_poles.objects.link(obj)

# Leaf (ℝ, k=0): white sphere at the top
lv0 = LEVELS[0]
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=POLE_SIZE*1.3, location=(0, 0, lv0['z'] + 0.5), segments=20, ring_count=14)
obj = bpy.context.active_object; obj.name = 'ℝ_leaf_marker'
obj.data.materials.append(MAT_BASE['leaf'])
for c in obj.users_collection: c.objects.unlink(obj)
col_poles.objects.link(obj)


# ── Camera ────────────────────────────────────────────────────────────────────

bpy.ops.object.camera_add(location=(18, -8, 4))
cam = bpy.context.active_object; cam.name = 'Fano_cam'
cam.data.lens = 40
cam.rotation_euler = (math.radians(80), 0, math.radians(65))
bpy.context.scene.camera = cam


# ── Lighting ──────────────────────────────────────────────────────────────────

bpy.ops.object.light_add(type='AREA', location=(10, 4, 8))
key = bpy.context.active_object; key.name = 'Key'
key.data.energy = 800; key.data.size = 8.0

bpy.ops.object.light_add(type='AREA', location=(-8, -6, 2))
fill = bpy.context.active_object; fill.name = 'Fill'
fill.data.energy = 300; fill.data.size = 10.0

bpy.ops.object.light_add(type='POINT', location=(0, 0, LEVELS[8]['z'] - 1.0))
root_g = bpy.context.active_object; root_g.name = 'Root_glow'
root_g.data.energy = 200; root_g.data.color = (0.45, 0.0, 0.70)

bpy.ops.object.light_add(type='POINT', location=(0, 0, LEVELS[0]['z'] + 1.0))
leaf_g = bpy.context.active_object; leaf_g.name = 'Leaf_glow'
leaf_g.data.energy = 80; leaf_g.data.color = (1.0, 1.0, 1.0)

# ZD equator accent
bpy.ops.object.light_add(type='POINT', location=(0, 3, LEVELS[4]['z']))
zd_l = bpy.context.active_object; zd_l.name = 'ZD_light'
zd_l.data.energy = 120; zd_l.data.color = (0.0, 0.85, 0.85)


# ── World ─────────────────────────────────────────────────────────────────────

world = bpy.context.scene.world or bpy.data.worlds.new('World')
bpy.context.scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes.get('Background')
if bg:
    bg.inputs['Color'].default_value    = (0.005, 0.005, 0.010, 1.0)
    bg.inputs['Strength'].default_value = 0.03


# ── Render ────────────────────────────────────────────────────────────────────

scene = bpy.context.scene
scene.render.engine           = 'CYCLES'
scene.cycles.samples          = 128
scene.render.resolution_x     = 1920
scene.render.resolution_y     = 1080
scene.render.film_transparent = True


# ── Summary ───────────────────────────────────────────────────────────────────

total_heptagons = sum(LEVELS[k]['n_fano'] for k in range(9))
gap_heptagons   = sum(
    1 for k in range(3,9)
    for fi in range(LEVELS[k]['n_fano'])
    if fano_covers_gap(fi, LEVELS[k]['n_fano'])
)

print()
print('=' * 64)
print('ZERO TREE — SPACE C: FANO TOWER / 32 HEPTAGONS')
print('Paper: \'How an Addition EQUALS a Subtraction\'')
print('=' * 64)
print()
print('  Level  Name      sigma   n_fano  Gap planes')
print('  ' + '─' * 50)
for lv in LEVELS:
    n_f = lv['n_fano']
    if n_f == 0:
        print(f'  k={lv["k"]}  {lv["name"]:<8}  {lv["sigma"]:+.3f}  [no Fano structure]')
        continue
    gap_count = sum(1 for fi in range(n_f) if fano_covers_gap(fi, n_f))
    zd_mark = ' ← ZD EQUATOR' if lv['is_first_zd'] else ''
    print(f'  k={lv["k"]}  {lv["name"]:<8}  {lv["sigma"]:+.3f}  {n_f:6d}  {gap_count} gap planes{zd_mark}')
print()
print(f'  Total heptagons: {total_heptagons} (63 = 2⁶−1)')
print(f'  Monster gap heptagons: {gap_heptagons}')
print(f'  Data source: {"telperion_blender_data.json" if _DATA else "analytic equidistribution"}')
print()
print('  Fano lines per heptagon: 7')
print('  Each line = octonion triple {eᵢ,eⱼ,eₖ}: eᵢeⱼ = ±eₖ')
print('  Silver heptagons = Monster gap = Telperion')
print('=' * 64)
