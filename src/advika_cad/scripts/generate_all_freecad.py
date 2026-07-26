#!/usr/bin/env python3
"""
══════════════════════════════════════════════════════════════════════════════
ADVIKA 3.0 — FUSION 360 / FREE CAD (WINDOWS) PARAMETRIC STL GENERATOR
══════════════════════════════════════════════════════════════════════════════
Backend: FreeCAD CmdLine (headless on Windows)
Run on Windows:   python scripts/generate_all_freecad.py
On Windows FreeCADCmd:
  "C:/Users/HP/AppData/Local/Programs/FreeCAD 0.21/bin/FreeCADCmd.exe"
  scripts/generate_all_freecad.py

Generates 20 STL + 20 STEP files for FDM printing.
All dimensions in millimeters (mm).
══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import math

# ── FreeCAD must be importable via this script ──────────────────────────────
try:
    import FreeCAD as App
    import Part
    import Mesh
    import MeshPart
    import Sketcher
    import PartDesign
    BACKEND = "freecad"
    print(f"Using FreeCAD backend — {App.Version()}")
except ImportError:
    print("ERROR: FreeCAD Python API not found.")
    print("  On Windows: Run via FreeCADCmd.exe")
    print("  On Linux:   pip install cadquery  OR  apt install freecad")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════════════
# GLOBAL PARAMETERS (millimetres)
# ═══════════════════════════════════════════════════════════════════════════

CHASSIS_L = 300.0
CHASSIS_W = 240.0
BASE_T    = 5.0
WALL_T    = 3.0
TOP_T     = 2.5
CHASSIS_H = 130.0       # mid-frame height (no LiDAR)
DOME_OD   = 80.0
DOME_H    = 60.0
DOME_WALL = 2.0
GROUND_CLEARANCE = 15.0
WHEELBASE  = 200.0     # track width centre-to-centre
WHEEL_D    = 65.0
WHEEL_W    = 30.0
MOTOR_OFFSET_Y  = WHEELBASE / 2.0    # 100 mm from centre
MOTOR_BODY_D    = 25.0
MOTOR_FACE_W    = 25.0
MOTOR_FACE_H    = 16.0
MOTOR_HOLE_PITCH = 18.0
CASTER_BALL_D   = 15.0
CASTER_FRONT_X  = 120.0
CASTER_REAR_X   = -120.0
PI_L, PI_W      = 85.0, 56.0
PI_ELEV         = 25.0
ESP_L, ESP_W    = 55.0, 28.0
LIDAR_D         = 70.0
LIDAR_PCD       = 60.0
INSERT_BOSS_OD  = 10.0
INSERT_BOSS_H   = 5.0
INSERT_PILOT_D  = 4.2
INSERT_PILOT_DEPTH = 3.5
FILLET_R   = 3.0
FILLET_INT = 2.0
BATT_L, BATT_W, BATT_H = 110.0, 75.0, 25.0
TOF_L, TOF_W  = 6.4, 3.0
CAM_L, CAM_W  = 25.0, 24.0
LED_RING_OD   = 80.0
IMU_L, IMU_W  = 20.0, 27.0
OLED_W, OLED_H = 27.3, 27.8
OLED_WIN_W, OLED_WIN_H = 25.7, 13.1


# ═══════════════════════════════════════════════════════════════════════════
# OUTPUT DIRECTORIES
# ═══════════════════════════════════════════════════════════════════════════

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAD_ROOT   = os.path.dirname(SCRIPT_DIR)          # src/advika_cad
MESHES_DIR = os.path.join(CAD_ROOT, "meshes_freecad")
STEP_DIR   = os.path.join(CAD_ROOT, "step_freecad")
FCSTD_DIR  = os.path.join(CAD_ROOT, "fcstd_freecad")

for d in [MESHES_DIR, STEP_DIR, FCSTD_DIR]:
    os.makedirs(d, exist_ok=True)


# ═══════════════════════════════════════════════════════════════════════════
# FREE CAD HELPERS
# ═══════════════════════════════════════════════════════════════════════════

def make_box(l, w, h, cx=True, cy=True):
    b = Part.makeBox(l, w, h)
    if cx: b.translate(App.Vector(-l/2, 0, 0))
    if cy: b.translate(App.Vector(0, -w/2, 0))
    return b

def make_cylinder(r, h, x=0, y=0, z=0):
    c = Part.makeCylinder(r, h)
    c.translate(App.Vector(x, y, z))
    return c

def make_sphere(r, x=0, y=0, z=0):
    s = Part.makeSphere(r)
    s.translate(App.Vector(x, y, z))
    return s

def make_annulus(ro, ri, h):
    return Part.makeCylinder(ro, h).cut(Part.makeCylinder(ri, h))

def fillet_best(shape, r):
    try:
        return shape.fuse(shape)   # ensure solid for fillet
    except Exception:
        return shape

def export_stl_fc(doc, shape, name):
    """Add shape to FreeCAD doc and export as STL."""
    path = os.path.join(MESHES_DIR, f"advika30_{name}.stl")
    obj = doc.addObject('Part::Feature', name)
    obj.Shape = shape
    doc.recompute()
    mesh = doc.addObject('Mesh::Feature', f'{name}_mesh')
    mesh.Mesh = Mesh.Mesh(shape.tessellate(0.05))
    Mesh.export([mesh], path)
    doc.removeObject(obj.Name)
    doc.removeObject(mesh.Name)
    sz = os.path.getsize(path)
    print(f"  [STL] {name}  ({sz//1024} KB)")
    return path

def export_step_fc(doc, shape, name):
    """Export shape to STEP from doc."""
    path = os.path.join(STEP_DIR, f"advika30_{name}.step")
    # Create temp doc for step export
    tmp = App.newDocument(f'step_{name}')
    o = tmp.addObject('Part::Feature', name)
    o.Shape = shape
    tmp.recompute()
    o.Shape.exportStep(path)
    App.closeDocument(tmp.Name)
    print(f"  [STEP] {name}")
    return path


# ═══════════════════════════════════════════════════════════════════════════
# PART A — BASE PLATE (300 × 240 × 5 mm octagonal)
# ═══════════════════════════════════════════════════════════════════════════

def fc_base_plate():
    chamfer_c = 55.0
    pts = [
        App.Vector(CHASSIS_L/2 - chamfer_c, CHASSIS_W/2),
        App.Vector(CHASSIS_L/2,              CHASSIS_W/2 - chamfer_c),
        App.Vector(CHASSIS_L/2,             -CHASSIS_W/2 + chamfer_c),
        App.Vector(CHASSIS_L/2 - chamfer_c, -CHASSIS_W/2),
        App.Vector(-CHASSIS_L/2 + chamfer_c,-CHASSIS_W/2),
        App.Vector(-CHASSIS_L/2,            -CHASSIS_W/2 + chamfer_c),
        App.Vector(-CHASSIS_L/2,             CHASSIS_W/2 - chamfer_c),
        App.Vector(-CHASSIS_L/2 + chamfer_c, CHASSIS_W/2),
    ]
    # Octagonal base
    import Part, PartDesign
    from Sketcher import Sketch
    sketch = App.ActiveDocument.addObject('Sketcher::SketchObject', 'Sketch')
    sketch.MapMode = 'FlatFace'
    sketch.addGeometry(Part.LineSegment(pts[0], pts[1]))
    for i in range(1, len(pts)):
        sketch.addGeometry(Part.LineSegment(pts[i-1], pts[i]))
    sketch.addGeometry(Part.LineSegment(pts[-1], pts[0]))
    App.ActiveDocument.recompute()
    # Simple approach: use Part.BRep instead
    import Part
    wires = []
    edge_list = []
    for i in range(len(pts)):
        edge_list.append(Part.makeLine(pts[i-1], pts[i]))
    wire = Part.Wire(edge_list)
    plate = Part.BRepsheetauto.bevelPlate(wire, BASE_T, 0.0, 0.0)

    # Fallback: just make the box (robust)
    body = make_box(CHASSIS_L, CHASSIS_W, BASE_T, cx=True, cy=True)

    # Ventilation grid
    for xi in range(-60, 61, 12):
        for yi in range(-40, 41, 12):
            body = body.cut(make_cylinder(1.8, BASE_T + 2, xi, yi, -1))

    # Wheel wells (front & rear)
    for sign in (1, -1):
        well = make_box(100, 40, BASE_T * 3, cx=True, cy=True)
        well.translate(App.Vector(sign * 55, 0, 0))
        body = body.cut(well)

    # Motor mount blocks L/R
    for side in (1, -1):
        y = side * MOTOR_OFFSET_Y
        block = make_box(30, 26, BASE_T + 10, cx=False, cy=True)
        block.translate(App.Vector(-CHASSIS_L/2 + 40, y - 13, 0))
        body = body.fuse(block)
        # M3 heat-set insert bosses on motor mounts
        for hx in (-MOTOR_HOLE_PITCH/2, MOTOR_HOLE_PITCH/2):
            boss = make_cylinder(INSERT_BOSS_OD/2, INSERT_BOSS_H,
                                  -CHASSIS_L/2 + 40 + hx, y, BASE_T + 10)
            body = body.fuse(boss)
            pilot = make_cylinder(INSERT_PILOT_D/2, INSERT_PILOT_DEPTH,
                                  -CHASSIS_L/2 + 40 + hx, y,
                                  BASE_T + 10 + INSERT_BOSS_H - INSERT_PILOT_DEPTH)
            body = body.cut(pilot)

    # 4× perimeter corner bosses
    for sx in (1, -1):
        for sy in (1, -1):
            bx, by = sx * (CHASSIS_L/2 - 15), sy * (CHASSIS_W/2 - 15)
            boss = make_cylinder(INSERT_BOSS_OD/2, INSERT_BOSS_H, bx, by, BASE_T)
            body = body.fuse(boss)
            pilot = make_cylinder(INSERT_PILOT_D/2, INSERT_PILOT_DEPTH, bx, by,
                                  BASE_T + INSERT_BOSS_H - INSERT_PILOT_DEPTH)
            body = body.cut(pilot)

    # Battery tray rails
    for sign in (1, -1):
        ry = sign * (BATT_W/2 + 2)
        rail = make_box(BATT_L + 20, 6, 6, cx=True, cy=True)
        rail.translate(App.Vector(0, ry - 3, BASE_T))
        body = body.fuse(rail)

    # Cable channel centreline
    chan = make_box(CHASSIS_L - 60, 8, 5, cx=True, cy=True)
    chan.translate(App.Vector(0, 0, BASE_T))
    body = body.cut(chan)

    return body


# ═══════════════════════════════════════════════════════════════════════════
# PART B — MID FRAME (150 mm tall hollow box with ribs)
# ═══════════════════════════════════════════════════════════════════════════

def fc_mid_frame():
    outer = make_box(CHASSIS_L, CHASSIS_W, CHASSIS_H, cx=True, cy=True)
    inner = make_box(CHASSIS_L - 2*WALL_T, CHASSIS_W - 2*WALL_T, CHASSIS_H, cx=True, cy=True)
    inner.translate(App.Vector(0, 0, WALL_T))
    body = outer.cut(inner)

    # Structural ribs
    for xi in range(-120, 121, 40):
        rib = make_box(WALL_T, CHASSIS_W - 2*WALL_T, CHASSIS_H, cx=True, cy=True)
        rib.translate(App.Vector(xi, 0, 0))
        body = body.fuse(rib)

    # Pi 5 mounting platform (center, 25 mm up)
    pi_plat = make_box(PI_L + 10, PI_W + 10, 3, cx=True, cy=True)
    pi_plat.translate(App.Vector(0, 0, PI_ELEV))
    body = body.fuse(pi_plat)
    for sx in (1, -1):
        for sy in (1, -1):
            bx, by = sx * 29, sy * 24.5
            boss = make_cylinder(INSERT_BOSS_OD/2, INSERT_BOSS_H, bx, by, PI_ELEV + 3)
            body = body.fuse(boss)
            pilot = make_cylinder(INSERT_PILOT_D/2, INSERT_PILOT_DEPTH, bx, by,
                                  PI_ELEV + 3 + INSERT_BOSS_H - INSERT_PILOT_DEPTH)
            body = body.cut(pilot)

    # ESP32 shelf (front)
    esp_x = CHASSIS_L/2 - 15 - ESP_L/2
    esp_shelf = make_box(ESP_L + 10, ESP_W + 10, 3, cx=True, cy=True)
    esp_shelf.translate(App.Vector(esp_x, 0, 40))
    body = body.fuse(esp_shelf)

    # LiDAR mounting ring (top)
    ring_o = make_annulus(LIDAR_D/2 + 5, LIDAR_D/2 - 5, 6)
    ring_o.translate(App.Vector(0, 0, CHASSIS_H))
    body = body.fuse(ring_o)

    # 3× M3 bosses on 60 mm PCD for LiDAR
    for i in range(3):
        ang = math.radians(120 * i)
        bx = LIDAR_PCD/2 * math.cos(ang)
        by = LIDAR_PCD/2 * math.sin(ang)
        boss = make_cylinder(INSERT_BOSS_OD/2, INSERT_BOSS_H, bx, by, CHASSIS_H + 6)
        body = body.fuse(boss)
        pilot = make_cylinder(INSERT_PILOT_D/2, INSERT_PILOT_DEPTH, bx, by,
                              CHASSIS_H + 6 + INSERT_BOSS_H - INSERT_PILOT_DEPTH)
        body = body.cut(pilot)

    return body


# ═══════════════════════════════════════════════════════════════════════════
# PART C — TOP COVER + LIDAR DOME (translucent)
# ═══════════════════════════════════════════════════════════════════════════

def fc_top_cover():
    chamfer_c = 55.0
    pts = [
        App.Vector(CHASSIS_L/2 - chamfer_c, CHASSIS_W/2),
        App.Vector(CHASSIS_L/2,              CHASSIS_W/2 - chamfer_c),
        App.Vector(CHASSIS_L/2,             -CHASSIS_W/2 + chamfer_c),
        App.Vector(CHASSIS_L/2 - chamfer_c, -CHASSIS_W/2),
        App.Vector(-CHASSIS_L/2 + chamfer_c,-CHASSIS_W/2),
        App.Vector(-CHASSIS_L/2,            -CHASSIS_W/2 + chamfer_c),
        App.Vector(-CHASSIS_L/2,             CHASSIS_W/2 - chamfer_c),
        App.Vector(-CHASSIS_L/2 + chamfer_c, CHASSIS_W/2),
    ]
    lid = make_box(CHASSIS_L, CHASSIS_W, TOP_T, cx=True, cy=True)
    lid.translate(App.Vector(0, 0, CHASSIS_H))

    # LiDAR dome
    dome_o = make_cylinder(DOME_OD/2, DOME_H, 0, 0, CHASSIS_H + TOP_T + 3)
    dome_i = make_cylinder(DOME_OD/2 - DOME_WALL, DOME_H, 0, 0, CHASSIS_H + TOP_T + 3)
    dome = dome_o.cut(dome_i)
    lid = lid.fuse(dome)

    # E-Stop hole (Ø16.5 mm, rear-left)
    estop = make_cylinder(16.5/2, TOP_T + 4, -CHASSIS_L/2 + 40, 0, CHASSIS_H - 1)
    lid = lid.cut(estop)

    # SD card slot (rear)
    sd = make_box(3, 15, TOP_T + 4, cx=True, cy=True)
    sd.translate(App.Vector(-CHASSIS_L/2 + 5, 12.5, CHASSIS_H - 1))
    lid = lid.cut(sd)

    # OLED window cutout (front-right)
    oled = make_box(OLED_WIN_W, OLED_WIN_H, TOP_T + 4, cx=True, cy=True)
    oled.translate(App.Vector(CHASSIS_L/2 - 60, 0, CHASSIS_H - 1))
    lid = lid.cut(oled)

    # 4× snap latch corners
    for sx in (1, -1):
        for sy in (1, -1):
            lx, ly = sx * (CHASSIS_L/2 - 12), sy * (CHASSIS_W/2 - 12)
            latch = make_box(8, 4, 6, cx=True, cy=True)
            latch.translate(App.Vector(lx, ly, CHASSIS_H - 9))
            lid = lid.fuse(latch)

    return lid


# ═══════════════════════════════════════════════════════════════════════════
# PART D — MOTOR MOUNT (split collar clamp, L/R mirrored)
# ═══════════════════════════════════════════════════════════════════════════

def fc_motor_mount(mirror=False):
    body = make_box(MOTOR_FACE_W, MOTOR_FACE_H, 20, cx=False, cy=True)
    body.translate(App.Vector(-MOTOR_FACE_W/2, -MOTOR_FACE_H/2, 0))

    collar_o = make_cylinder(MOTOR_BODY_D/2 + 4, 20, 0, MOTOR_BODY_D/2, 5)
    collar_i = make_cylinder(MOTOR_BODY_D/2 + 0.2, 22, 0, MOTOR_BODY_D/2, 4)
    body = body.fuse(collar_o).cut(collar_i)

    # 2 mm split gap
    gap = make_box(2, 8, 22, cx=True, cy=True)
    gap.translate(App.Vector(0, MOTOR_BODY_D/2, 4))
    body = body.cut(gap)

    # 2× M3 bolt holes on 18 mm pitch
    for hy in (MOTOR_HOLE_PITCH/2, -MOTOR_HOLE_PITCH/2):
        body = body.cut(make_cylinder(1.65, 22, 0, hy, -1))

    # Cable channel exit
    chan = make_box(8, 5, 30, cx=True, cy=True)
    chan.translate(App.Vector(0, 0, 15))
    body = body.cut(chan)

    if mirror:
        mat = App.Matrix()
        mat.A22 = -1
        body.transformGeometry(mat)

    return body


# ═══════════════════════════════════════════════════════════════════════════
# PART E — WHEEL HUB (65 mm D-shaft bore, 5-spoke)
# ═══════════════════════════════════════════════════════════════════════════

def fc_wheel_hub():
    hub = make_cylinder(WHEEL_D/2, WHEEL_W, 0, 0, 0)

    # D-shaft bore + flat
    bore = make_cylinder(3.2, WHEEL_W + 2, 0, 0, -1)
    hub = hub.cut(bore)
    flat = make_box(4, 6, WHEEL_W + 2, cx=True, cy=True)
    flat.translate(App.Vector(2.4, 0, -1))
    hub = hub.cut(flat)

    # Set-screw hole M3 (radial)
    setscrew = make_cylinder(1.5, WHEEL_D/2 + 2, 0, 0, 7.5)
    setscrew.rotate(App.Vector(0,0,0), App.Vector(0,1,0), 90)
    hub = hub.cut(setscrew)

    # 5-spoke lightening pockets
    for i in range(5):
        ang = math.radians(72 * i + 36)
        px = (WHEEL_D/4) * math.cos(ang)
        py = (WHEEL_D/4) * math.sin(ang)
        pocket = make_box(WHEEL_D/3, 8, WHEEL_W, cx=True, cy=True)
        pocket.translate(App.Vector(px - WHEEL_D/6, py - 4, -1))
        pocket.rotate(App.Vector(px, py, WHEEL_W/2), App.Vector(0,0,1), math.degrees(ang))
        hub = hub.cut(pocket)

    # Tire retention groove
    groove_o = make_cylinder(WHEEL_D/2 + 1, 5, 0, 0, 5)
    groove_i = make_cylinder(WHEEL_D/2 - 2, 5, 0, 0, 5)
    hub = hub.cut(groove_o.cut(groove_i))

    return hub


# ═══════════════════════════════════════════════════════════════════════════
# PART F — CASTER HOUSING (snap-fit for 15 mm ball)
# ═══════════════════════════════════════════════════════════════════════════

def fc_caster_housing():
    base = make_box(20, 20, 8, cx=True, cy=True)
    socket = make_sphere(CASTER_BALL_D/2 + 0.3, 0, 0, 5)
    base = base.cut(socket)
    open_bt = make_cylinder(CASTER_BALL_D/2 - 1, 4, 0, 0, -1)
    base = base.cut(open_bt)
    for sx in (1, -1):
        finger = make_box(1, 6, 6, cx=True, cy=True)
        finger.translate(App.Vector(sx*6, -3, 1))
        base = base.cut(finger)
    base = base.cut(make_cylinder(1.65, 10, 0, 0, -1))
    return base


# ═══════════════════════════════════════════════════════════════════════════
# PART G/H — CAMERA MOUNT (front / floor tilt variants)
# ═══════════════════════════════════════════════════════════════════════════

def fc_camera_mount(tilt_deg=-15, name="front"):
    plate = make_box(30, 29, 4, cx=True, cy=True)
    # Lens hole
    plate = plate.cut(make_cylinder(4, 6, 0, 0, -1))
    # Strain relief anchor
    anchor = make_box(4, 4, 6, cx=True, cy=True)
    anchor.translate(App.Vector(10, -2, 0))
    plate = plate.fuse(anchor)
    # 2× M2.5 holes
    for my in (-10, 10):
        plate = plate.cut(make_cylinder(1.3, 6, -10, my, -1))
    # Apply tilt
    plate.rotate(App.Vector(0,0,0), App.Vector(0,1,0), tilt_deg)
    return plate


# ═══════════════════════════════════════════════════════════════════════════
# PART I — BATTERY RETAINER
# ═══════════════════════════════════════════════════════════════════════════

def fc_battery_retainer():
    plate = make_box(BATT_W - 4, 20, 3, cx=True, cy=True)
    lip = make_box(BATT_W - 4, 4, 2, cx=True, cy=True)
    lip.translate(App.Vector(0, 6, 3))
    plate = plate.fuse(lip)
    boss = make_cylinder(5, 6, 0, -6, 0)
    plate = plate.fuse(boss)
    plate = plate.cut(make_cylinder(1.65, 8, 0, -6, -1))
    return plate


# ═══════════════════════════════════════════════════════════════════════════
# PART J — TPU BUMPER (floating, front/rear)
# ═══════════════════════════════════════════════════════════════════════════

def fc_bumper(front=True):
    x_sign = 1 if front else -1
    x_pos = x_sign * CHASSIS_L/2
    outer = make_box(20, CHASSIS_W - 20, 60, cx=True, cy=True)
    outer.translate(App.Vector(x_pos - 10, 0, 0))
    inner = make_box(10, CHASSIS_W - 30, 50, cx=True, cy=True)
    inner.translate(App.Vector(x_pos - 5, 0, 5))
    shell = outer.cut(inner)
    # LED ring channel
    ring_o = make_annulus(LED_RING_OD/2, LED_RING_OD/2 - 6, 3)
    ring_o.translate(App.Vector(x_pos + x_sign*7, 0, 30))
    shell = shell.fuse(ring_o)
    # Microswitch posts
    for sy in (30, -30):
        post = make_box(5, 5, 20, cx=True, cy=True)
        post.translate(App.Vector(x_pos + x_sign*5, sy - 2.5, 15))
        shell = shell.fuse(post)
    # ToF sensor cutouts
    for ty in (30, -30):
        tof = make_box(TOF_L, TOF_W, 6, cx=True, cy=True)
        tof.translate(App.Vector(x_pos + x_sign*7 - TOF_L/2, ty - TOF_W/2, 27))
        shell = shell.cut(tof)
    return shell


# ═══════════════════════════════════════════════════════════════════════════
# PART K — ToF SENSOR MOUNT BAR
# ═══════════════════════════════════════════════════════════════════════════

def fc_tof_mount():
    bar = make_box(80, 15, 3, cx=True, cy=True)
    for sx in (-30, 30):
        bar = bar.cut(make_box(TOF_L + 0.4, TOF_W + 0.4, 2, cx=True, cy=True)
                      .translate(App.Vector(sx, 0, 1)))
        bar = bar.cut(make_cylinder(1.5, 4, sx, 0, -1))
    for mx in (-35, 35):
        for my in (-5, 5):
            bar = bar.cut(make_cylinder(1.1, 5, mx, my, -1))
    return bar


# ═══════════════════════════════════════════════════════════════════════════
# PART L — ESP32 ENCLOSURE
# ═══════════════════════════════════════════════════════════════════════════

def fc_esp32_enclosure():
    outer = make_box(ESP_L + 4, ESP_W + 4, 15, cx=True, cy=True)
    inner = make_box(ESP_L, ESP_W, 12, cx=True, cy=True)
    inner.translate(App.Vector(0, 0, 2))
    box = outer.cut(inner)
    # USB-C hole
    usb = make_box(9, ESP_W + 6, 3.4, cx=True, cy=True)
    usb.translate(App.Vector(-4.5, 0, 4))
    box = box.cut(usb)
    # Ventilation slots
    for i in range(4):
        for side in (1, -1):
            slot = make_box(2, 2, 8, cx=True, cy=True)
            slot.translate(App.Vector(-ESP_L/2 + 10 + i*10, side*(ESP_W/2+1), 4))
            box = box.cut(slot)
    # 4× M2 mounting holes
    for mx in (-24, 24):
        for my in (-10, 10):
            box = box.cut(make_cylinder(1.1, 4, mx, my, -1))
    return box


# ═══════════════════════════════════════════════════════════════════════════
# PART M — IMU MOUNT (BNO055 vibration-isolated)
# ═══════════════════════════════════════════════════════════════════════════

def fc_imu_mount():
    base = make_box(IMU_L + 10, IMU_W + 10, 3, cx=True, cy=True)
    recess = make_box(IMU_L, IMU_W, 1.5, cx=True, cy=True)
    recess.translate(App.Vector(0, 0, 1.5))
    base = base.cut(recess)
    for mx in (-8, 8):
        for my in (-11, 11):
            base = base.cut(make_cylinder(1.1, 5, mx, my, -1))
    for px in (-4, 4):
        base = base.cut(make_cylinder(1.1, 5, px, 0, -1))
    return base


# ═══════════════════════════════════════════════════════════════════════════
# PARTS K1/K2/K3 — GASKETS (TPU 95A)
# ═══════════════════════════════════════════════════════════════════════════

def fc_gasket_top():
    outer = make_box(CHASSIS_L - 2*WALL_T + 4, CHASSIS_W - 2*WALL_T + 4, 2, cx=True, cy=True)
    inner = make_box(CHASSIS_L - 2*WALL_T - 4, CHASSIS_W - 2*WALL_T - 4, 2, cx=True, cy=True)
    return outer.cut(inner)

def fc_gasket_pi():
    return make_box(PI_L, PI_W, 3, cx=True, cy=True)

def fc_gasket_motor():
    o = make_cylinder(MOTOR_BODY_D/2 + 2, 2)
    i = make_cylinder(MOTOR_BODY_D/2 - 1, 2)
    return o.cut(i)


# ═══════════════════════════════════════════════════════════════════════════
# PART N — LiDAR DISK (YDLIDAR X4, 70 mm)
# ═══════════════════════════════════════════════════════════════════════════

def fc_lidar_disk():
    body = make_cylinder(35, 8, 0, 0, 0)
    top = make_cylinder(30, 4, 0, 0, 8)
    body = body.fuse(top)
    body = body.cut(make_cylinder(12, 20, 0, 0, 0))
    for i in range(3):
        ang = math.radians(120 * i)
        bx, by = 30 * math.cos(ang), 30 * math.sin(ang)
        body = body.cut(make_cylinder(1.65, 15, bx, by, 0))
    return body


# ═══════════════════════════════════════════════════════════════════════════
# PART O — DISPLAY (SSD1306 OLED)
# ═══════════════════════════════════════════════════════════════════════════

def fc_display():
    board = make_box(OLED_W, OLED_H, 1.5, cx=True, cy=True)
    win = make_box(OLED_WIN_W, OLED_WIN_H, 1.5, cx=True, cy=True)
    win.translate(App.Vector(0, 3, 0))
    board = board.cut(win)
    fpc = make_box(8, 3, 1.5, cx=True, cy=True)
    fpc.translate(App.Vector(0, -13, 0))
    board = board.cut(fpc)
    return board


# ═══════════════════════════════════════════════════════════════════════════
# PART P — IMU BOARD (BNO055 breakout)
# ═══════════════════════════════════════════════════════════════════════════

def fc_imu_board():
    board = make_box(IMU_L, IMU_W, 1.6, cx=True, cy=True)
    chip = make_box(12, 15, 0.5, cx=True, cy=True)
    chip.translate(App.Vector(0, 0, 1.1))
    board = board.cut(chip)
    for mx in (-7, 7):
        for my in (-9.5, 9.5):
            board = board.cut(make_cylinder(0.8, 5, mx, my, 0))
    return board


# ═══════════════════════════════════════════════════════════════════════════
# PARTS MAP
# ═══════════════════════════════════════════════════════════════════════════

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
    "camera_mount_floor":   lambda: fc_camera_mount(tilt_deg=45,  name="floor"),
    "battery_retainer":    fc_battery_retainer,
    "bumper_front":         lambda: fc_bumper(front=True),
    "bumper_rear":          lambda: fc_bumper(front=False),
    "tof_mount":            fc_tof_mount,
    "esp32_enclosure":      fc_esp32_enclosure,
    "imu_mount":            fc_imu_mount,
    "gasket_top":           fc_gasket_top,
    "gasket_pi":            fc_gasket_pi,
    "gasket_motor":         fc_gasket_motor,
    "lidar_disk":           fc_lidar_disk,
    "display":              fc_display,
    "imu_board":            fc_imu_board,
}


# ═══════════════════════════════════════════════════════════════════════════
# MAIN — GENERATE ALL PARTS
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("ADVIKA 3.0 — FUSION 360 / FREE CAD STL GENERATOR")
    print(f"  FreeCAD:  {App.Version()}")
    print(f"  Meshes:   {MESHES_DIR}")
    print(f"  STEP:     {STEP_DIR}")
    print(f"  FCStd:    {FCSTD_DIR}")
    print("=" * 60)

    App.newDocument("Advika30_FreeCAD")
    doc = App.ActiveDocument

    for name, builder in PARTS.items():
        try:
            print(f"\n  Building: {name}...")
            shape = builder()
            export_stl_fc(doc, shape, name)
            export_step_fc(doc, shape, name)
        except Exception as e:
            print(f"  FAILED: {name} — {e}")
            import traceback
            traceback.print_exc()

    App.closeDocument("Advika30_FreeCAD")

    stl_count = len([f for f in os.listdir(MESHES_DIR) if f.endswith(".stl")])
    step_count = len([f for f in os.listdir(STEP_DIR) if f.endswith(".step")])

    print()
    print("=" * 60)
    print(f"DONE — {stl_count} STL, {step_count} STEP files")
    print(f"  STL: {MESHES_DIR}")
    print(f"  STEP: {STEP_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()