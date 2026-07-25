#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════
ADVIKA 3.0 — COMPLETE PARAMETRIC CAD MODEL GENERATOR (FreeCAD)
═══════════════════════════════════════════════════════════════════════════

Run with:  freecadcmd generate_all.py
    or:    python3 generate_all.py  (uses FreeCAD library if installed)

Generates 17 STL files for FDM printing + STEP assembly export.
All dimensions in millimeters.
"""

import sys
import os
import math

# ─── Try FreeCAD, fallback to cadquery ───
BACKEND = None
try:
    import FreeCAD as App
    import Part
    import Mesh
    BACKEND = "freecad"
    print("Using FreeCAD backend")
except ImportError:
    try:
        import cadquery as cq
        from cadquery import exporters
        BACKEND = "cadquery"
        print("Using CadQuery backend")
    except ImportError:
        print("ERROR: Neither FreeCAD nor CadQuery found.")
        print("Install one of:")
        print("  sudo apt install freecad")
        print("  pip install cadquery")
        sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════
# OUTPUT DIRECTORIES
# ═══════════════════════════════════════════════════════════════════════

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAD_ROOT = os.path.dirname(SCRIPT_DIR)  # src/advika_cad
MESHES_DIR = os.path.join(CAD_ROOT, "meshes")
STEP_DIR = os.path.join(CAD_ROOT, "step")
FCSTD_DIR = os.path.join(CAD_ROOT, "fcstd")

for d in [MESHES_DIR, STEP_DIR, FCSTD_DIR]:
    os.makedirs(d, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════
# GLOBAL PARAMETERS (exact match with advika30_cad.py)
# ═══════════════════════════════════════════════════════════════════════

CHASSIS_L = 300.0       # mm
CHASSIS_W = 240.0
CHASSIS_H = 150.0       # without LiDAR dome
GROUND_CLEARANCE = 15.0
WHEELBASE = 200.0       # track width center-to-center

BASE_T = 5.0            # base plate thickness
WALL_T = 3.0            # mid frame wall thickness
TOP_T = 2.5             # top cover thickness
RIB_T = 5.0             # structural rib thickness

FILLET_R = 3.0          # child-safety edge radius
FILLET_INT = 2.0        # FDM internal corner

# M3 heat-set insert boss
INSERT_PILOT_D = 4.2
INSERT_PILOT_DEPTH = 3.5
INSERT_BOSS_OD = 10.0
INSERT_BOSS_H = 5.0

# Motors (JGA25-370)
MOTOR_OFFSET_Y = WHEELBASE / 2.0  # 100mm from centerline
MOTOR_BODY_D = 25.0
MOTOR_BODY_L = 37.0
MOTOR_SHAFT_H = 32.5
MOTOR_FACE_W = 25.0
MOTOR_FACE_H = 16.0
MOTOR_HOLE_PITCH = 18.0

# Wheels
WHEEL_D = 65.0
WHEEL_W = 30.0

# Casters
CASTER_BALL_D = 15.0
CASTER_FRONT_X = 120.0
CASTER_REAR_X = -120.0

# Raspberry Pi 5
PI_L, PI_W = 85.0, 56.0
PI_HOLE_X, PI_HOLE_Y = 58.0, 49.0
PI_ELEV = 25.0

# ESP32-S3
ESP_L, ESP_W = 55.0, 28.0
ESP_HOLE_X, ESP_HOLE_Y = 48.0, 21.0
ESP_STANDOFF_H = 10.0

# DRV8833
DRV_L, DRV_W = 20.0, 20.0
DRV_STANDOFF_H = 15.0

# LiDAR (LD06 / YDLIDAR X4)
LIDAR_D = 70.0
LIDAR_H = 40.0
LIDAR_PCD = 60.0
DOME_OD = 80.0
DOME_H = 60.0
DOME_WALL = 2.0

# Battery (3S2P 18650)
BATT_L, BATT_W, BATT_H = 110.0, 75.0, 25.0

# Power distribution board
PDB_L, PDB_W = 50.0, 30.0
PDB_STANDOFF_H = 15.0

# LED ring / bumper
LED_RING_OD = 80.0
CABLE_CHANNEL_W = 8.0
CABLE_CHANNEL_H = 5.0

# Camera (Pi Camera Module 3 Wide: 25×24mm board)
CAM_L, CAM_W = 25.0, 24.0

# ToF sensor (VL53L5CX: 6.4×3.0mm)
TOF_L, TOF_W = 6.4, 3.0

# IMU (BNO055: 20×27mm)
IMU_L, IMU_W = 20.0, 27.0

# SSD1306 OLED (27.3×27.8mm board, 25.7×13.1mm display window)
OLED_W, OLED_H = 27.3, 27.8
OLED_WINDOW_W, OLED_WINDOW_H = 25.7, 13.1


# ═══════════════════════════════════════════════════════════════════════
# FREECAD HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

if BACKEND == "freecad":

    def make_box(l, w, h, centered=True):
        """Create a box, optionally centered on XY."""
        shape = Part.makeBox(l, w, h)
        if centered:
            shape.translate(App.Vector(-l/2, -w/2, 0))
        return shape

    def make_cylinder(r, h, x=0, y=0, z=0):
        """Create a cylinder at position."""
        shape = Part.makeCylinder(r, h)
        shape.translate(App.Vector(x, y, z))
        return shape

    def make_sphere(r, x=0, y=0, z=0):
        """Create a sphere at position."""
        shape = Part.makeSphere(r)
        shape.translate(App.Vector(x, y, z))
        return shape

    def fillet_edges(shape, r):
        """Fillet all edges with given radius (best effort)."""
        try:
            return shape.makeFillet(r, shape.Edges)
        except Exception:
            return shape

    def export_stl(shape, name):
        """Export shape to STL file."""
        path = os.path.join(MESHES_DIR, f"advika30_{name}.stl")
        doc = App.newDocument(name)
        obj = doc.addObject("Part::Feature", name)
        obj.Shape = shape
        doc.recompute()
        mesh = doc.addObject("Mesh::Feature", f"{name}_mesh")
        mesh.Mesh = Mesh.Mesh(shape.tessellate(0.1))
        Mesh.export([mesh], path)
        # Also save FCStd
        fcstd_path = os.path.join(FCSTD_DIR, f"advika30_{name}.FCStd")
        doc.saveAs(fcstd_path)
        App.closeDocument(doc.Name)
        print(f"  ✅ {path}")
        return path

    def export_step(shape, name):
        """Export shape to STEP file."""
        path = os.path.join(STEP_DIR, f"advika30_{name}.step")
        shape.exportStep(path)
        print(f"  ✅ {path}")
        return path


# ═══════════════════════════════════════════════════════════════════════
# CADQUERY HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

if BACKEND == "cadquery":

    def export_stl_cq(part, name):
        """Export CadQuery part to STL file."""
        path = os.path.join(MESHES_DIR, f"advika30_{name}.stl")
        exporters.export(part, path)
        print(f"  ✅ {path}")
        return path

    def export_step_cq(part, name):
        """Export CadQuery part to STEP file."""
        path = os.path.join(STEP_DIR, f"advika30_{name}.step")
        exporters.export(part, path, exportType="STEP")
        print(f"  ✅ {path}")
        return path


# ═══════════════════════════════════════════════════════════════════════
# PART GENERATORS — FREECAD BACKEND
# ═══════════════════════════════════════════════════════════════════════

def fc_base_plate():
    """PART A: Base Plate 300×240×5mm with motor mounts, battery rails, vents."""
    plate = make_box(CHASSIS_L, CHASSIS_W, BASE_T)

    # Ventilation grid (center, avoid motor/battery zones)
    for xi in range(-60, 61, 10):
        for yi in range(-30, 31, 10):
            hole = make_cylinder(1.5, BASE_T + 2, xi, yi, -1)
            plate = plate.cut(hole)

    # Motor mount blocks (left & right)
    for side in (1, -1):
        y = side * MOTOR_OFFSET_Y
        block = Part.makeBox(30, 26, BASE_T + 10)
        block.translate(App.Vector(-CHASSIS_L/2 + 40 - 15, y - 13, 0))
        plate = plate.fuse(block)
        # M3 insert bosses
        for hx in (-MOTOR_HOLE_PITCH/2, MOTOR_HOLE_PITCH/2):
            boss = make_cylinder(INSERT_BOSS_OD/2, INSERT_BOSS_H,
                                 -CHASSIS_L/2 + 40 + hx, y, BASE_T + 10)
            pilot = make_cylinder(INSERT_PILOT_D/2, INSERT_PILOT_DEPTH,
                                  -CHASSIS_L/2 + 40 + hx, y, BASE_T + 10 + INSERT_BOSS_H - INSERT_PILOT_DEPTH)
            plate = plate.fuse(boss).cut(pilot)

    # Caster snap-fit recesses (front & rear)
    for cx in (CASTER_FRONT_X, CASTER_REAR_X):
        recess = Part.makeBox(22, 22, 8)
        recess.translate(App.Vector(cx - 11, -11, 0))
        plate = plate.cut(recess)

    # Battery tray rails (C-channel)
    for sign in (1, -1):
        ry = sign * (BATT_W/2 + 2)
        rail = Part.makeBox(BATT_L + 20, 6, 6)
        rail.translate(App.Vector(-(BATT_L + 20)/2, ry - 3, BASE_T))
        lip = Part.makeBox(BATT_L + 20, 3, 3)
        offset = -3 if sign > 0 else 0
        lip.translate(App.Vector(-(BATT_L + 20)/2, ry + offset, BASE_T + 6))
        plate = plate.fuse(rail).fuse(lip)

    # Cable channel (centerline)
    channel = Part.makeBox(CHASSIS_L - 60, CABLE_CHANNEL_W, CABLE_CHANNEL_H)
    channel.translate(App.Vector(-(CHASSIS_L - 60)/2, -CABLE_CHANNEL_W/2, BASE_T))
    plate = plate.cut(channel)

    # IMU locating pins (2× Ø2mm)
    for px in (-4, 4):
        pin = make_cylinder(1.0, 2.0, px, 0, BASE_T)
        plate = plate.fuse(pin)

    # 4× perimeter insert bosses for mid-frame
    for sx in (1, -1):
        for sy in (1, -1):
            bx = sx * (CHASSIS_L/2 - 15)
            by = sy * (CHASSIS_W/2 - 15)
            boss = make_cylinder(INSERT_BOSS_OD/2, INSERT_BOSS_H, bx, by, BASE_T)
            pilot = make_cylinder(INSERT_PILOT_D/2, INSERT_PILOT_DEPTH,
                                  bx, by, BASE_T + INSERT_BOSS_H - INSERT_PILOT_DEPTH)
            plate = plate.fuse(boss).cut(pilot)

    return fillet_edges(plate, FILLET_R)


def fc_mid_frame():
    """PART B: Mid Frame — 150mm tall hollow frame with ribs, Pi/ESP shelves."""
    outer = make_box(CHASSIS_L, CHASSIS_W, CHASSIS_H)
    inner = Part.makeBox(CHASSIS_L - 2*WALL_T, CHASSIS_W - 2*WALL_T, CHASSIS_H)
    inner.translate(App.Vector(-(CHASSIS_L - 2*WALL_T)/2, -(CHASSIS_W - 2*WALL_T)/2, WALL_T))
    frame = outer.cut(inner)

    # Structural ribs every 40mm
    for xi in range(int(-CHASSIS_L/2) + 40, int(CHASSIS_L/2), 40):
        rib = Part.makeBox(RIB_T, CHASSIS_W, CHASSIS_H)
        rib.translate(App.Vector(xi - RIB_T/2, -CHASSIS_W/2, 0))
        rib_cut = Part.makeBox(RIB_T, CHASSIS_W - 2*WALL_T, CHASSIS_H)
        rib_cut.translate(App.Vector(xi - RIB_T/2, -(CHASSIS_W - 2*WALL_T)/2, WALL_T))
        frame = frame.fuse(rib.cut(rib_cut))

    # Pi 5 mounting platform (center, 25mm up)
    pi_plat = Part.makeBox(PI_L + 10, PI_W + 10, 3)
    pi_plat.translate(App.Vector(-(PI_L + 10)/2, -(PI_W + 10)/2, PI_ELEV))
    frame = frame.fuse(pi_plat)
    for sx in (1, -1):
        for sy in (1, -1):
            bx, by = sx * PI_HOLE_X/2, sy * PI_HOLE_Y/2
            boss = make_cylinder(INSERT_BOSS_OD/2, INSERT_BOSS_H, bx, by, PI_ELEV + 3)
            pilot = make_cylinder(INSERT_PILOT_D/2, INSERT_PILOT_DEPTH,
                                  bx, by, PI_ELEV + 3 + INSERT_BOSS_H - INSERT_PILOT_DEPTH)
            frame = frame.fuse(boss).cut(pilot)

    # ESP32 mounting shelf (front)
    esp_x = CHASSIS_L/2 - 15 - ESP_L/2
    esp_shelf = Part.makeBox(ESP_L + 10, ESP_W + 10, 3)
    esp_shelf.translate(App.Vector(esp_x - (ESP_L + 10)/2, -(ESP_W + 10)/2, 40))
    frame = frame.fuse(esp_shelf)

    # LiDAR mounting ring (top)
    ring_outer = make_cylinder(LIDAR_D/2 + 5, 6, 0, 0, CHASSIS_H)
    ring_inner = make_cylinder(LIDAR_D/2 - 5, 6, 0, 0, CHASSIS_H)
    frame = frame.fuse(ring_outer.cut(ring_inner))

    # 3× M3 bosses on 60mm PCD for LiDAR
    for i in range(3):
        ang = math.radians(120 * i)
        bx = LIDAR_PCD/2 * math.cos(ang)
        by = LIDAR_PCD/2 * math.sin(ang)
        boss = make_cylinder(INSERT_BOSS_OD/2, INSERT_BOSS_H, bx, by, CHASSIS_H + 6)
        pilot = make_cylinder(INSERT_PILOT_D/2, INSERT_PILOT_DEPTH,
                              bx, by, CHASSIS_H + 6 + INSERT_BOSS_H - INSERT_PILOT_DEPTH)
        frame = frame.fuse(boss).cut(pilot)

    return fillet_edges(frame, FILLET_R)


def fc_top_cover():
    """PART C: Top Cover with LiDAR dome, E-stop hole, snap latches."""
    lid = make_box(CHASSIS_L, CHASSIS_W, TOP_T)

    # Perimeter lip (5mm drop-down to engage mid_frame)
    lip_outer = Part.makeBox(CHASSIS_L - 2*WALL_T - 0.4, CHASSIS_W - 2*WALL_T - 0.4, 5)
    lip_outer.translate(App.Vector(-(CHASSIS_L - 2*WALL_T - 0.4)/2,
                                    -(CHASSIS_W - 2*WALL_T - 0.4)/2, -5))
    lip_inner = Part.makeBox(CHASSIS_L - 4*WALL_T - 0.4, CHASSIS_W - 4*WALL_T - 0.4, 5)
    lip_inner.translate(App.Vector(-(CHASSIS_L - 4*WALL_T - 0.4)/2,
                                    -(CHASSIS_W - 4*WALL_T - 0.4)/2, -5))
    lid = lid.fuse(lip_outer.cut(lip_inner))

    # LiDAR dome (translucent cylinder)
    dome_outer = make_cylinder(DOME_OD/2, DOME_H, 0, 0, TOP_T + 3)
    dome_inner = make_cylinder(DOME_OD/2 - DOME_WALL, DOME_H, 0, 0, TOP_T + 3)
    dome_flange = make_cylinder(DOME_OD/2 + 5, 3, 0, 0, TOP_T)
    lid = lid.fuse(dome_flange).fuse(dome_outer.cut(dome_inner))

    # E-Stop hole (Ø16.5mm, rear)
    estop = make_cylinder(16.5/2, TOP_T + 2, -CHASSIS_L/2 + 40, 0, -1)
    lid = lid.cut(estop)

    # LED status window (front)
    led_win = Part.makeBox(20, 6, TOP_T + 2)
    led_win.translate(App.Vector(CHASSIS_L/2 - 30, -3, -1))
    lid = lid.cut(led_win)

    # SD card slot (rear)
    sd_slot = Part.makeBox(3, 15, TOP_T + 2)
    sd_slot.translate(App.Vector(-CHASSIS_L/2 + 5, 12.5, -1))
    lid = lid.cut(sd_slot)

    # SSD1306 OLED display cutout (front-right area)
    oled_cut = Part.makeBox(OLED_WINDOW_W, OLED_WINDOW_H, TOP_T + 2)
    oled_cut.translate(App.Vector(CHASSIS_L/2 - 60, -OLED_WINDOW_H/2, -1))
    lid = lid.cut(oled_cut)

    # 4× corner snap latches
    for sx in (1, -1):
        for sy in (1, -1):
            lx = sx * (CHASSIS_L/2 - 12)
            ly = sy * (CHASSIS_W/2 - 12)
            latch = Part.makeBox(8, 4, 6)
            latch.translate(App.Vector(lx - 4, ly - 2, -9))
            hook = Part.makeBox(10, 4, 2)
            hook.translate(App.Vector(lx - 5, ly - 2, -3))
            lid = lid.fuse(latch).fuse(hook)

    return fillet_edges(lid, FILLET_R)


def fc_motor_mount(mirror=False):
    """PART D: Motor Mount Bracket — split collar clamp for JGA25-370."""
    body = Part.makeBox(MOTOR_FACE_W, MOTOR_FACE_H, 20)
    body.translate(App.Vector(-MOTOR_FACE_W/2, -MOTOR_FACE_H/2, 0))

    # Clamp collar
    collar = make_cylinder(MOTOR_BODY_D/2 + 4, 20, 0, 0, 5)
    bore = make_cylinder(MOTOR_BODY_D/2 + 0.2, 22, 0, 0, 4)
    body = body.fuse(collar).cut(bore)

    # Split gap (2mm)
    gap = Part.makeBox(2, 8, 22)
    gap.translate(App.Vector(-1, MOTOR_BODY_D/2, 4))
    body = body.cut(gap)

    # Pinch bolt hole M3
    pinch = make_cylinder(1.6, 20, 0, MOTOR_BODY_D/2 + 6, 15)
    pinch.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 90)
    body = body.cut(pinch)

    # 2× M3 mounting holes on 18mm centers
    for hy in (MOTOR_HOLE_PITCH/2, -MOTOR_HOLE_PITCH/2):
        hole = make_cylinder(1.65, 22, 0, hy, -1)
        body = body.cut(hole)

    # Cable channel exit
    chan = Part.makeBox(CABLE_CHANNEL_W, CABLE_CHANNEL_H, 30)
    chan.translate(App.Vector(-CABLE_CHANNEL_W/2, -CABLE_CHANNEL_H/2, 15))
    body = body.cut(chan)

    if mirror:
        mat = App.Matrix()
        mat.A22 = -1  # mirror Y
        body = body.transformGeometry(mat)

    return fillet_edges(body, FILLET_INT)


def fc_wheel_hub():
    """PART E: Wheel Hub — 65mm, 6mm D-shaft bore, 5-spoke pattern."""
    hub = make_cylinder(WHEEL_D/2, 15)

    # D-shaft bore (6mm with flat)
    bore = make_cylinder(3.2, 17, 0, 0, -1)
    hub = hub.cut(bore)
    flat = Part.makeBox(4, 6, 17)
    flat.translate(App.Vector(2.4, -3, -1))
    hub = hub.cut(flat)

    # Set screw hole M3 (radial)
    setscrew = make_cylinder(1.5, WHEEL_D/2 + 2, 0, 0, 7.5)
    setscrew.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), 90)
    hub = hub.cut(setscrew)

    # Tire retention groove (2mm deep, 30mm wide band)
    groove_outer = make_cylinder(WHEEL_D/2, 30, 0, 0, -7.5)
    groove_inner = make_cylinder(WHEEL_D/2 - 2, 30, 0, 0, -7.5)
    groove_outer.translate(App.Vector(0, 0, 7.5))
    groove_inner.translate(App.Vector(0, 0, 7.5))
    # Only cut the band
    groove_band = groove_outer.cut(groove_inner)
    # Intersect with outer rim to get the groove
    # (simplified: just cut a ring-shaped channel)
    groove_cut = make_cylinder(WHEEL_D/2 + 1, 5, 0, 0, 5)
    groove_fill = make_cylinder(WHEEL_D/2 - 2, 5, 0, 0, 5)
    hub = hub.cut(groove_cut.cut(groove_fill))

    # 5-spoke pattern (cut pockets between spokes)
    for i in range(5):
        ang = math.radians(72 * i + 36)
        px = (WHEEL_D/4) * math.cos(ang)
        py = (WHEEL_D/4) * math.sin(ang)
        pocket = Part.makeBox(WHEEL_D/3, 8, 17)
        pocket.translate(App.Vector(px - WHEEL_D/6, py - 4, -1))
        pocket.rotate(App.Vector(px, py, 0), App.Vector(0, 0, 1), math.degrees(ang))
        hub = hub.cut(pocket)

    return fillet_edges(hub, 1.5)


def fc_caster_housing():
    """PART F: Caster Housing — snap-fit for 15mm ball caster."""
    base = make_box(20, 20, 8)

    # Ball socket (sphere cut)
    socket = make_sphere(CASTER_BALL_D/2 + 0.3, 0, 0, 5)
    base = base.cut(socket)

    # Open bottom for ball protrusion
    open_bt = make_cylinder(CASTER_BALL_D/2 - 1, 4, 0, 0, -1)
    base = base.cut(open_bt)

    # Retention clip flex fingers
    for sx in (1, -1):
        finger = Part.makeBox(1, 6, 6)
        finger.translate(App.Vector(sx*6 - 0.5, -3, 1))
        base = base.cut(finger)

    # Central M3 mounting hole
    mhole = make_cylinder(1.65, 10, 0, 0, -1)
    base = base.cut(mhole)

    return fillet_edges(base, 2.0)


def fc_camera_mount(tilt_deg=-15, name="front"):
    """PART G/H: Camera Mount — tilted bracket for Pi Camera Module 3."""
    plate = make_box(30, 29, 4)

    # Gasket pocket (top face)
    gasket = Part.makeBox(25, 24, 3)
    gasket.translate(App.Vector(-12.5, -12, 4))
    plate = plate.cut(gasket)

    # Lens hole
    lens = make_cylinder(4, 6, 0, 0, -1)
    plate = plate.cut(lens)

    # Strain relief anchor
    anchor = Part.makeBox(4, 4, 6)
    anchor.translate(App.Vector(10, -2, 0))
    tie_hole = make_cylinder(1, 4, 12, 0, 3)
    tie_hole.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 90)
    plate = plate.fuse(anchor).cut(tie_hole)

    # 2× M2.5 mounting holes
    for my in (-10, 10):
        mh = make_cylinder(1.3, 6, -10, my, -1)
        plate = plate.cut(mh)

    # Apply tilt
    plate.rotate(App.Vector(0, 0, 0), App.Vector(0, 1, 0), tilt_deg)

    return fillet_edges(plate, 1.5)


def fc_battery_retainer():
    """PART I: Battery Retainer — sliding lock with thumb screw."""
    plate = make_box(BATT_W - 4, 20, 3)

    # Retention lip
    lip = Part.makeBox(BATT_W - 4, 4, 2)
    lip.translate(App.Vector(-(BATT_W - 4)/2, 6, 3))
    plate = plate.fuse(lip)

    # Thumb screw boss M3
    boss = make_cylinder(5, 6, 0, -6, 0)
    screw_hole = make_cylinder(1.65, 8, 0, -6, -1)
    plate = plate.fuse(boss).cut(screw_hole)

    return fillet_edges(plate, 1.5)


def fc_bumper(front=True):
    """PART J: TPU Bumper — floating bumper with LED ring channel."""
    x_sign = 1 if front else -1
    x_pos = x_sign * CHASSIS_L/2

    outer = Part.makeBox(20, CHASSIS_W - 20, 60)
    outer.translate(App.Vector(x_pos - 10, -(CHASSIS_W - 20)/2, 0))

    # Hollow shell (5mm wall)
    inner = Part.makeBox(10, CHASSIS_W - 30, 50)
    inner.translate(App.Vector(x_pos - 5, -(CHASSIS_W - 30)/2, 5))
    shell = outer.cut(inner)

    # LED ring channel (80mm annular recess on outward face)
    ring_cx = x_pos + x_sign * 7
    ring_outer = make_cylinder(LED_RING_OD/2, 3, 0, 0, 30)
    ring_inner = make_cylinder(LED_RING_OD/2 - 6, 3, 0, 0, 30)
    ring_chan = ring_outer.cut(ring_inner)
    ring_chan.translate(App.Vector(ring_cx, 0, 0))
    shell = shell.fuse(ring_chan)

    # Microswitch mounting posts (2×)
    for sy in (30, -30):
        post = Part.makeBox(5, 5, 20)
        post.translate(App.Vector(x_pos + x_sign*5 - 2.5, sy - 2.5, 15))
        shell = shell.fuse(post)

    # ToF sensor cutouts (2× on face, 60mm apart)
    for ty in (30, -30):
        tof = Part.makeBox(TOF_L, TOF_W, 6)
        tof.translate(App.Vector(ring_cx - TOF_L/2, ty - TOF_W/2, 27))
        shell = shell.cut(tof)

    return fillet_edges(shell, FILLET_R)


def fc_tof_mount():
    """PART: ToF Sensor Mount — VL53L5CX bracket (60mm spacing)."""
    base = make_box(70, 15, 3)

    # 2× sensor pockets (6.4×3.0mm, 60mm apart)
    for sx in (-30, 30):
        pocket = Part.makeBox(TOF_L + 0.4, TOF_W + 0.4, 2)
        pocket.translate(App.Vector(sx - (TOF_L + 0.4)/2, -(TOF_W + 0.4)/2, 1))
        base = base.cut(pocket)
        # Lens window hole
        lens = make_cylinder(1.5, 4, sx, 0, -1)
        base = base.cut(lens)

    # M2 mounting holes (4×)
    for mx in (-30, 30):
        for my in (-5, 5):
            mh = make_cylinder(1.1, 5, mx, my, -1)
            base = base.cut(mh)

    return fillet_edges(base, 1.0)


def fc_esp32_enclosure():
    """PART: ESP32-S3 Enclosure — 55×30×15mm ventilated box."""
    outer = make_box(ESP_L + 4, ESP_W + 4, 15)
    inner = Part.makeBox(ESP_L, ESP_W, 12)
    inner.translate(App.Vector(-ESP_L/2, -ESP_W/2, 2))
    box = outer.cut(inner)

    # USB-C access hole (9×3.4mm, front face)
    usb = Part.makeBox(9, ESP_W + 6, 3.4)
    usb.translate(App.Vector(-4.5, -(ESP_W + 6)/2, 4))
    box = box.cut(usb)

    # UART header slot (rear face, 15×5mm)
    uart = Part.makeBox(15, ESP_W + 6, 5)
    uart.translate(App.Vector(-7.5, -(ESP_W + 6)/2, 5))
    uart.rotate(App.Vector(0, 0, 0), App.Vector(0, 0, 1), 180)
    box = box.cut(uart)

    # Ventilation slots (4× per side, 2mm wide × 8mm long)
    for i in range(4):
        for side in (1, -1):
            slot = Part.makeBox(2, 2, 8)
            sx = -ESP_L/2 + 10 + i * 10
            slot.translate(App.Vector(sx, side * (ESP_W/2 + 1), 4))
            box = box.cut(slot)

    # 4× M2 mounting holes (bottom)
    for mx in (ESP_HOLE_X/2, -ESP_HOLE_X/2):
        for my in (ESP_HOLE_Y/2, -ESP_HOLE_Y/2):
            mh = make_cylinder(1.1, 4, mx, my, -1)
            box = box.cut(mh)

    return fillet_edges(box, 1.5)


def fc_imu_mount():
    """PART: IMU Mount — BNO055 vibration-isolated center plate."""
    base = make_box(IMU_L + 10, IMU_W + 10, 3)

    # Sensor recess (20×27mm)
    recess = Part.makeBox(IMU_L, IMU_W, 1.5)
    recess.translate(App.Vector(-IMU_L/2, -IMU_W/2, 1.5))
    base = base.cut(recess)

    # TPU isolator pads — 4× M2 mounting holes
    for mx in (-IMU_L/2 + 2, IMU_L/2 - 2):
        for my in (-IMU_W/2 + 2, IMU_W/2 - 2):
            mh = make_cylinder(1.1, 5, mx, my, -1)
            base = base.cut(mh)

    # 2× locating pins (Ø2mm) to match base plate
    for px in (-4, 4):
        pin_hole = make_cylinder(1.1, 5, px, 0, -1)
        base = base.cut(pin_hole)

    return fillet_edges(base, 1.0)


def fc_gasket_top():
    """PART K1: Top Perimeter Gasket — TPU 95A."""
    outer = make_box(CHASSIS_L - 2*WALL_T + 4, CHASSIS_W - 2*WALL_T + 4, 2)
    inner = Part.makeBox(CHASSIS_L - 2*WALL_T - 4, CHASSIS_W - 2*WALL_T - 4, 2)
    inner.translate(App.Vector(-(CHASSIS_L - 2*WALL_T - 4)/2, -(CHASSIS_W - 2*WALL_T - 4)/2, 0))
    return outer.cut(inner)


def fc_gasket_pi():
    """PART K2: Pi Vibration Pad — TPU 95A."""
    return make_box(PI_L, PI_W, 3)


def fc_gasket_motor():
    """PART K3: Motor Isolation Ring — TPU 95A."""
    outer = make_cylinder(MOTOR_BODY_D/2 + 2, 2)
    inner = make_cylinder(MOTOR_BODY_D/2 - 1, 2)
    return outer.cut(inner)


# ═══════════════════════════════════════════════════════════════════════
# MAIN — BUILD ALL PARTS, EXPORT STL + STEP
# ═══════════════════════════════════════════════════════════════════════

PARTS = {
    "base_plate":           fc_base_plate,
    "mid_frame":            fc_mid_frame,
    "top_cover":            fc_top_cover,
    "motor_mount_L":        lambda: fc_motor_mount(mirror=False),
    "motor_mount_R":        lambda: fc_motor_mount(mirror=True),
    "wheel_hub_L":          fc_wheel_hub,
    "wheel_hub_R":          fc_wheel_hub,
    "caster_housing_F":     fc_caster_housing,
    "caster_housing_R":     fc_caster_housing,
    "camera_mount_front":   lambda: fc_camera_mount(tilt_deg=-15, name="front"),
    "camera_mount_floor":   lambda: fc_camera_mount(tilt_deg=45, name="floor"),
    "battery_retainer":     fc_battery_retainer,
    "bumper_front":         lambda: fc_bumper(front=True),
    "bumper_rear":          lambda: fc_bumper(front=False),
    "tof_mount":            fc_tof_mount,
    "esp32_enclosure":      fc_esp32_enclosure,
    "imu_mount":            fc_imu_mount,
    "gasket_top":           fc_gasket_top,
    "gasket_pi":            fc_gasket_pi,
    "gasket_motor":         fc_gasket_motor,
}


def main():
    print("=" * 60)
    print("ADVIKA 3.0 — PARAMETRIC CAD MODEL GENERATOR")
    print("=" * 60)
    print(f"Backend:    {BACKEND}")
    print(f"Meshes:     {MESHES_DIR}")
    print(f"STEP:       {STEP_DIR}")
    if BACKEND == "freecad":
        print(f"FCStd:      {FCSTD_DIR}")
    print()

    if BACKEND == "freecad":
        print("Generating parts (FreeCAD)...")
        for name, builder in PARTS.items():
            try:
                print(f"\n  📐 Building: {name}")
                shape = builder()
                export_stl(shape, name)
                export_step(shape, name)
            except Exception as e:
                print(f"  ❌ FAILED: {name} — {e}")

    elif BACKEND == "cadquery":
        # Import and run the existing CadQuery-based script
        print("Generating parts (CadQuery — using advika30_cad.py)...")
        cad_script = os.path.join(CAD_ROOT, "advika30_cad.py")
        if os.path.exists(cad_script):
            # Redirect CadQuery output to meshes dir
            sys.path.insert(0, CAD_ROOT)
            import advika30_cad as cad
            cad.export_all_stl(out_dir=MESHES_DIR)
            try:
                asm = cad.build_assembly()
                step_path = os.path.join(STEP_DIR, "advika30_assembly.step")
                asm.save(step_path)
                print(f"  ✅ Assembly STEP: {step_path}")
            except Exception as e:
                print(f"  ⚠️  Assembly STEP export skipped: {e}")
        else:
            print(f"  ❌ CadQuery script not found: {cad_script}")

    print()
    print("=" * 60)
    stl_count = len([f for f in os.listdir(MESHES_DIR) if f.endswith(".stl")])
    print(f"✅ DONE — {stl_count} STL files in {MESHES_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
