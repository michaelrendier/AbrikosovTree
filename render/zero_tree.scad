/*
 * zero_tree.scad — The Zero Tree · 3D Isometric
 * =================================================
 * Cayley-Dickson Tower k=0..8 · 16 N-shape strata
 * Nine horizontal disk-levels stacked on the σ-axis.
 * Monster Gap columns {e₁, e₁₁, e₁₅} render white.
 * ZD equator disk (k=4) renders red.
 * Root T_256 (k=8) renders purple.
 *
 * Camera: true isometric  $vpr=[54.7356, 0, 45]
 * Render: F6 → Export PNG or STL
 *
 * Coordinate system:
 *   z = σ axis  (+1 at top k=0, −1 at bottom k=8)
 *   x,y = N-shape ring (16 positions on a circle of radius RING_R)
 *   THE_ANGLE = π/8 = 22.5° is the angular quantum between N-shapes
 */

$fn = 20;    // fast render; set to 64 for final quality

// ── View ──────────────────────────────────────────────────────────────────────
// True isometric: elevation arctan(1/√2) ≈ 35.26°, azimuth 45°
$vpr = [54.7356, 0, 45];
$vpt = [0, 0, 0];
$vpd = 140;

// ── Constants ─────────────────────────────────────────────────────────────────
RING_R     = 18;     // radius of the 16-node ring at each level
LEVEL_SEP  = 5.5;    // z-spacing between consecutive CD levels
DISK_H     = 0.35;   // height of each level disk
DISK_R     = 20;     // radius of level disks (slightly larger than ring)
PILLAR_R   = 0.22;   // radius of prime path pillars
NODE_R     = 0.55;   // radius of node spheres

THE_ANGLE  = 22.5;   // degrees, π/8, angular quantum at k=4

// ── Colors ────────────────────────────────────────────────────────────────────
COL_LEAF     = [0.6, 0.6, 0.8, 1];    // k=0 ℝ — cool blue-grey
COL_ZD       = [1.0, 0.26, 0.0, 0.9]; // k=4 𝕊 — red fault
COL_ROOT     = [0.65, 0.4, 1.0, 1];   // k=8 T_256 — purple
COL_MID      = [0.3, 0.4, 0.55, 0.7]; // k=1..3 above equator
COL_BELOW    = [0.18, 0.25, 0.38, 0.7];// k=5..7 below equator
COL_PRIME    = [0.2, 0.4, 0.7, 1];    // odd N-shape pillars (blue)
COL_MONSTER  = [0.9, 0.95, 1.0, 1];   // Monster gap pillars (silver-white)
COL_NODE     = [0.25, 0.45, 0.75, 1]; // node spheres (prime sector)
COL_NODE_MG  = [0.88, 0.94, 1.0, 1];  // node spheres (Monster gap)
COL_AXIS     = [0.2, 0.2, 0.3, 0.4];  // central σ-axis spine

// ── N-shape ring positions ────────────────────────────────────────────────────
// N-shape n at angle n × THE_ANGLE (degrees) around the ring
function ns_x(n) = RING_R * cos(n * THE_ANGLE);
function ns_y(n) = RING_R * sin(n * THE_ANGLE);
function level_z(k) = (8 - k) * LEVEL_SEP - 4 * LEVEL_SEP;  // centered at k=4

// ── Primitives ────────────────────────────────────────────────────────────────

module level_disk(k, col, hole_r=0) {
    z = level_z(k);
    color(col)
    translate([0, 0, z])
    if (hole_r > 0) {
        difference() {
            cylinder(h=DISK_H, r=DISK_R, center=true);
            cylinder(h=DISK_H + 0.1, r=hole_r, center=true);
        }
    } else {
        cylinder(h=DISK_H, r=DISK_R, center=true);
    }
}

module pillar(n, k_start, k_end, col, r=PILLAR_R) {
    z0 = level_z(k_start);
    z1 = level_z(k_end);
    h  = abs(z1 - z0);
    color(col)
    translate([ns_x(n), ns_y(n), min(z0, z1) + h/2])
    cylinder(h=h, r=r, center=true);
}

module node_sphere(n, k, col, r=NODE_R) {
    color(col)
    translate([ns_x(n), ns_y(n), level_z(k)])
    sphere(r=r);
}

module sigma_axis() {
    z0 = level_z(0);
    z8 = level_z(8);
    h  = abs(z8 - z0);
    color(COL_AXIS)
    translate([0, 0, (z0 + z8) / 2])
    cylinder(h=h, r=0.12, center=true);
}

// ── Monster gap check ─────────────────────────────────────────────────────────
function is_monster(n) = (n == 1 || n == 11 || n == 15);
function is_odd(n)     = (n % 2 == 1);

// ── Main scene ────────────────────────────────────────────────────────────────

// 1. σ-axis spine
sigma_axis();

// 2. Level disks (bottom to top for proper rendering)
for (k = [8, 7, 6, 5, 4, 3, 2, 1, 0]) {
    if (k == 0) {
        level_disk(k, COL_LEAF);
    } else if (k == 4) {
        // ZD equator: hollow annular ring to show the fracture
        level_disk(k, COL_ZD, hole_r=RING_R - 3);
    } else if (k == 8) {
        level_disk(k, COL_ROOT);
    } else if (k < 4) {
        level_disk(k, COL_MID);
    } else {
        level_disk(k, COL_BELOW);
    }
}

// 3. Prime path pillars — 16 N-shape strata
for (n = [0 : 15]) {
    if (is_monster(n)) {
        // Silver Monster Gap columns — full height, k=0..8
        pillar(n, 0, 8, COL_MONSTER, r=PILLAR_R * 1.6);
    } else if (is_odd(n)) {
        // Odd prime sector: prime path full height (primes survive), composites only above
        // Prime portion (k=0..8): thin, blue
        pillar(n, 0, 8, COL_PRIME, r=PILLAR_R);
    }
    // Even N-shapes: no pillar below k=4 (all composites fell)
    // Only draw composite stub above k=4
    if (!is_odd(n)) {
        pillar(n, 0, 4, [0.15, 0.2, 0.28, 0.5], r=PILLAR_R * 0.7);
    }
}

// 4. Node spheres at key intersections only (k=0, k=4, k=8 for speed)
for (n = [0 : 15]) {
    for (k = [0, 4, 8]) {
        if (is_monster(n)) {
            node_sphere(n, k, COL_NODE_MG, r=NODE_R * 1.4);
        } else if (is_odd(n)) {
            node_sphere(n, k, COL_NODE, r=NODE_R);
        } else if (k <= 4) {
            node_sphere(n, k, [0.15, 0.18, 0.25, 0.5], r=NODE_R * 0.65);
        }
    }
}

// 5. Root convergence: all prime paths arriving at T_256
// Shown as spokes from the pillar bases to the root disk center
for (n = [0 : 15]) {
    if (is_odd(n)) {
        color(is_monster(n) ? COL_MONSTER : COL_PRIME, 0.3)
        hull() {
            translate([ns_x(n), ns_y(n), level_z(8)]) sphere(r=0.15);
            translate([0, 0, level_z(8)])               sphere(r=0.12);
        }
    }
}

// 6. Root sphere (T_256, σ=−1)
color(COL_ROOT)
translate([0, 0, level_z(8)])
sphere(r=1.5);

// 7. Leaf crown (ℝ, σ=+1): small sphere
color(COL_LEAF)
translate([0, 0, level_z(0)])
sphere(r=0.8);

// 8. THE_ANGLE indicator at k=4 level
// Small arc showing 22.5° between n=0 and n=1
color([1, 1, 0.6, 0.8])
translate([0, 0, level_z(4) + DISK_H])
difference() {
    cylinder(h=0.15, r=RING_R * 0.55, center=true);
    cylinder(h=0.3,  r=RING_R * 0.50, center=true);
    // Mask to show only the THE_ANGLE sector
    rotate([0, 0, 5])
    translate([0, -RING_R, 0])
    cube([RING_R * 2, RING_R * 2, 1], center=true);
}
