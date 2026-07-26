#!/usr/bin/env python3
"""
ADVIKA 3.0 — CADQuery STL Generator
Uses EXACT dimensions from Fusion 360 generator script
Run: python generate_fusion_dims.py
Output: src/advika_description/stl/ (your official STL folder)
"""

import sys
import os
import math

try:
    import cadquery as cq
    from cadquery import exporters
except ImportError:
    print("ERROR: CadQuery not installed.")
    print("  Install: pip install cadquery")
    print("  Or on Linux: pip3 install cadquery")
    sys.exit(1)

# ═══ OUTPUT ═══
OUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "advika_description", "stl"
)
os.makedirs(OUT_DIR, exist_ok=True)

def save(stl_path, shape, name):
    """Export shape to STL and report size."""
    exporters.export(shape, stl_path)
    sz = os.path.getsize(stl_path)
    print(f"  [OK] {name:30s}  {sz//1024} KB  →  {os.path.basename(stl_path)}")

# ═══════════════════════════════════════════════════════════════
# PART 1: CHASSIS BASE — 300x240x5mm with 4 mounting holes
# ═══════════════════════════════════════════════════════════════

def make_chassis_base():
    # Main plate 300x240x5
    body = (cq.Workplane("XY")
            .rect(300, 240)
            .extrude(5)
            .edges(">Z").fillet(5.0)  # 5mm corner fillet
            )
    # 4 mounting holes at 15mm from corners
    for cx, cy in [(-135,-105), (135,-105), (135,105), (-135,105)]:
        body = (body
                .faces(">Z")
                .workplane()
                .pushPoints([(cx, cy)])
                .circle(1.5)
                .cutThruAll()
                )
    return body

# ═══════════════════════════════════════════════════════════════
# PART 2: MOTOR MOUNTS — 6mm shaft, 4× M3 at 15mm radius
# ═══════════════════════════════════════════════════════════════

def make_motor_mount():
    # Body with 6mm shaft hole + 4 mounting holes
    body = (cq.Workplane("XY")
            .circle(15)  # 30mm diameter body
            .extrude(20)
            .faces(">Z").workplane()
            .pushPoints([(0,0)])
            .circle(3.0)  # 6mm shaft hole
            .cutThruAll()
            )
    # 4× M3 holes at 15mm radius
    for angle in [45, 135, 225, 315]:
        rad = math.radians(angle)
        hx, hy = 15 * math.cos(rad), 15 * math.sin(rad)
        body = (body.faces(">Z").workplane()
                .pushPoints([(hx, hy)])
                .circle(1.5)
                .cutThruAll()
                )
    return body

# ═══════════════════════════════════════════════════════════════
# PART 3: WHEEL HUB — 65mm dia, 20mm thick, D-shaft
# ═══════════════════════════════════════════════════════════════

def make_wheel_hub():
    # Main cylinder 65mm diameter, 20mm thick
    body = (cq.Workplane("XY")
            .circle(32.5)  # 65mm diameter
            .extrude(20)
            )
    # D-shaft hole (6mm with flat)
    body = (body.faces(">Z").workplane()
            .pushPoints([(0, 0)])
            .rect(6, 5.5)  # D-profile approximation (6mm wide, 5.5mm deep flat)
            .cutThruAll()
            )
    # 4 mounting holes at 25mm radius
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        hx, hy = 25 * math.cos(rad), 25 * math.sin(rad)
        body = (body.faces(">Z").workplane()
                .pushPoints([(hx, hy)])
                .circle(1.5)
                .cutThruAll()
                )
    return body

# ═══════════════════════════════════════════════════════════════
# PART 4: LiDAR TOWER — 70mm base, 150mm tall, hollow, 2° draft
# ═══════════════════════════════════════════════════════════════

def make_lidar_tower():
    # Base circle 70mm, extruded 150mm with 2° taper
    body = (cq.Workplane("XY")
            .circle(35)  # 70mm diameter base
            .workplane(offset=150)
            .circle(35 - 150 * math.tan(math.radians(2)))  # 2° taper
            .loft()
            )
    # Shell with 2mm wall
    body = (cq.Workplane("XY")
            .circle(33)   # 70 - 2*2 = 66mm inner
            .workplane(offset=150)
            .circle(33 - 150 * math.tan(math.radians(2)))
            .loft()
            .shelledFaces(selectedFaces=[], thickness=2.0)
            )
    # Top platform 80mm diameter, 5mm thick
    top = (cq.Workplane("XY")
           .transformed(offset=(0, 0, 150))
           .circle(40)  # 80mm diameter
           .extrude(5)
           )
    body = body.union(top)
    # 4× M3 mounting holes at 25mm radius on top
    for angle in [45, 135, 225, 315]:
        rad = math.radians(angle)
        hx, hy = 25 * math.cos(rad), 25 * math.sin(rad)
        body = (body.faces(">Z").workplane()
                .pushPoints([(hx, hy)])
                .circle(1.5)
                .cutThruAll()
                )
    return body

# ═══════════════════════════════════════════════════════════════
# PART 5: TOP DOME — 115mm radius, 80mm height (revolve)
# (simplified: half-sphere-ish using loft)
# ═══════════════════════════════════════════════════════════════

def make_top_dome():
    # Dome: loft from circle at z=0 to point at z=80
    # Using sweep along arc path
    path = (cq.Workplane("XZ")
            .radiusArc((115, 0), 115)
            .straightTo(0)
            .close()
            )
    # Create a disc and loft to center point
    body = (cq.Workplane("XY")
            .circle(115)
            .workplane(offset=80)
            .circle(5)  # small top opening
            .loft()
            )
    return body

# ═══════════════════════════════════════════════════════════════
# PART 6: CAMERA MOUNTS — 25×24×8mm, M2.5 holes
# ═══════════════════════════════════════════════════════════════

def make_camera_mount():
    body = (cq.Workplane("XY")
            .rect(25, 24)
            .extrude(8)
            .edges(">Z or <Z").fillet(1.0)
            )
    # 2× M2.5 screw holes at ±5mm
    for hx in [-5, 5]:
        body = (body.faces(">Z").workplane()
                .pushPoints([(hx, 0)])
                .circle(1.25)  # 2.5mm diameter
                .cutThruAll()
                )
    return body

# ═══════════════════════════════════════════════════════════════
# PART 7: IMU MOUNT — 20×20×5mm with 3mm center hole
# ═══════════════════════════════════════════════════════════════

def make_imu_mount():
    body = (cq.Workplane("XY")
            .rect(20, 20)
            .extrude(5)
            )
    body = (body.faces(">Z").workplane()
            .pushPoints([(0, 0)])
            .circle(1.5)  # 3mm diameter center hole
            .cutThruAll()
            )
    return body

# ═══════════════════════════════════════════════════════════════
# PART 8: BATTERY TRAY — 80×70×25mm, hollow, XT60 + JST cutouts
# ═══════════════════════════════════════════════════════════════

def make_battery_tray():
    # Outer box 80x70x25
    outer = (cq.Workplane("XY")
             .rect(80, 70)
             .extrude(25)
             )
    # Inner box (hollow) = shell 2mm
    inner = (cq.Workplane("XY")
             .transformed(offset=(0,0,2))
             .rect(76, 66)
             .extrude(23)
             )
    body = outer.cut(inner)
    # XT60 cutout on front face (15x10mm)
    body = (body.faces(">Y").workplane(offset=-12)
            .pushPoints([(0, -12)])
            .rect(15, 10)
            .cutBlind(-8)
            )
    # JST cutout on side (8x4mm)
    body = (body.faces(">X").workplane(offset=-20)
            .pushPoints([(0, 0)])
            .rect(8, 4)
            .cutBlind(-5)
            )
    return body

# ═══════════════════════════════════════════════════════════════
# PART 9: BUMPERS — 280×30×20mm, rounded, hollow, microswitch holes
# ═══════════════════════════════════════════════════════════════

def make_bumper():
    # Rounded rectangle 280x30x20
    body = (cq.Workplane("XY")
            .rect(280, 30)
            .extrude(20)
            .edges(">Z").fillet(10.0)  # 10mm corner fillet
            )
    # Shell 2mm wall (hollow)
    inner = (cq.Workplane("XY")
             .transformed(offset=(0, 0, 2))
             .rect(276, 26)
             .extrude(18)
             )
    body = body.cut(inner)
    # 2× microswitch holes at ±100mm from center
    for hx in [-100, 100]:
        body = (body.faces(">Y").workplane()
                .pushPoints([(hx, 0)])
                .circle(1.5)
                .cutThruAll()
                )
    return body

# ═══════════════════════════════════════════════════════════════
# PART 10: ESP32 ENCLOSURE — 55×30×15mm, hollow, USB-C cutout
# ═══════════════════════════════════════════════════════════════

def make_esp32_enclosure():
    outer = (cq.Workplane("XY")
             .rect(55, 30)
             .extrude(15)
             )
    inner = (cq.Workplane("XY")
             .transformed(offset=(0, 0, 1.5))
             .rect(52, 27)
             .extrude(13.5)
             )
    body = outer.cut(inner)
    # USB-C cutout on front (10x5mm)
    body = (body.faces(">X").workplane(offset=-2)
            .pushPoints([(0, 0)])
            .rect(10, 5)
            .cutBlind(-5)
            )
    # Ventilation slots on top
    for vx in [-15, -5, 5, 15]:
        body = (body.faces(">Z").workplane()
                .pushPoints([(vx, 0)])
                .rect(5, 1)
                .cutBlind(-5)
                )
    return body

# ═══════════════════════════════════════════════════════════════
# PART 11: ESP32 LID
# ═══════════════════════════════════════════════════════════════

def make_esp32_lid():
    return (cq.Workplane("XY")
            .rect(55, 30)
            .extrude(2)
            .edges(">Z").fillet(0.5)
            )

# ═══════════════════════════════════════════════════════════════
# PART 12: LiDAR DISK (mounting adapter)
# ═══════════════════════════════════════════════════════════════

def make_lidar_disk():
    return (cq.Workplane("XY")
            .circle(35)   # 70mm diameter
            .extrude(4)   # 4mm thick
            .faces(">Z").workplane()
            .pushPoints([(0,0)])
            .circle(12)   # center hole for LiDAR shaft
            .cutThruAll()
            )

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

PARTS = [
    ("advika_chassis.stl",          make_chassis_base,      "Chassis 300x240x5mm + 4 holes"),
    ("advika_battery_tray.stl",     make_battery_tray,      "Battery Tray 80x70x25 hollow"),
    ("advika_bumper_front.stl",     make_bumper,           "Front Bumper 280x30x20 hollow"),
    ("advika_bumper_rear.stl",       make_bumper,           "Rear Bumper 280x30x20 hollow"),
    ("advika_camera_floor.stl",     make_camera_mount,     "Floor Camera Mount 25x24x8mm"),
    ("advika_camera_horizon.stl",   make_camera_mount,     "Horizon Camera Mount 25x24x8mm"),
    ("advika_esp32_enclosure.stl",  make_esp32_enclosure,  "ESP32 Enclosure 55x30x15mm hollow"),
    ("advika_esp32_lid.stl",        make_esp32_lid,         "ESP32 Lid 55x30x2mm"),
    ("advika_imu_mount.stl",        make_imu_mount,         "IMU Mount 20x20x5mm"),
    ("advika_lidar_tower.stl",      make_lidar_tower,       "LiDAR Tower 70mm base 150mm tall hollow"),
    ("advika_motor_mount_L.stl",    make_motor_mount,       "Motor Mount L 6mm shaft 4x M3"),
    ("advika_motor_mount_R.stl",    make_motor_mount,       "Motor Mount R 6mm shaft 4x M3"),
    ("advika_lidar_disk.stl",       make_lidar_disk,        "LiDAR Disk adapter 70mm"),
]

print("=" * 60)
print("ADVIKA 3.0 — CADQuery STL Generator")
print("  Dimensions from: advika_3_0_generator.py (Fusion 360)")
print(f"  Output: {OUT_DIR}")
print("=" * 60)

for filename, maker_fn, description in PARTS:
    stl_path = os.path.join(OUT_DIR, filename)
    print(f"\n  Building: {description}...")
    try:
        shape = maker_fn()
        save(stl_path, shape, filename)
    except Exception as e:
        print(f"  [FAIL] {filename}: {e}")
        import traceback
        traceback.print_exc()

print()
print("=" * 60)
print("DONE!")
print(f"  STL files saved to: {OUT_DIR}")
print("=" * 60)