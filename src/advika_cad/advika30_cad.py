"""
════════════════════════════════════════════════════════════════════════════
ADVIKA 3.0 — AUTONOMOUS MOBILE ROBOT (Differential Drive AMR)
Parametric CAD Model — CadQuery 2.x
════════════════════════════════════════════════════════════════════════════

Run with:  python advika30_cad.py
Requires:  pip install cadquery

────────────────────────────────────────────────────────────────────────────
BILL OF MATERIALS (BOM)
────────────────────────────────────────────────────────────────────────────
PRINTED PARTS (PETG unless noted)
  1  Base Plate                       x1   300x240x5mm, 50% infill
  2  Mid Frame                        x1   150mm tall walls, 30% infill
  3  Top Cover (w/ LiDAR dome)        x1   300x240x2.5mm, 30% infill
  4  Motor Mount Bracket (L/R)        x2   30% infill
  5  Wheel Hub                        x2   50% infill
  6  Caster Housing                   x2   30% infill
  7  Camera Mount - Front (Horizon)   x1   30% infill
  8  Camera Mount - Floor             x1   30% infill
  9  Battery Retainer (sliding lock)  x1   30% infill
 10  Bumper Front/Rear (TPU 95A)      x2   40% infill, flexible
 11  Gasket - Top Perimeter (TPU95A)  x1
 12  Gasket - Pi Vibration Pad (TPU)  x1
 13  Gasket - Motor Isolation (TPU)   x2

PURCHASED / ELECTRONIC COMPONENTS
  JGA25-370 DC Encoder Motor          x2
  15mm Ball Caster                    x2
  Raspberry Pi 5 (8GB)                x1
  ESP32-S3 DevKitC-1                  x1
  DRV8833 Dual H-Bridge Driver        x1
  YDLIDAR X4                          x1
  VL53L5CX ToF Sensor                 x2
  Pi Camera Module 3 Wide             x2
  3S2P 18650 Li-Ion Pack (11.1V 5200mAh, integrated BMS) x1
  Power Distribution Board (custom)   x1
  BNO055 9-DOF IMU                    x1
  WS2812B 24-LED Ring (80mm)          x2
  4Ω 3W Mini Speaker (28mm)           x1
  16mm Latching E-Stop (NC)           x1
  M3 Brass Heat-Set Threaded Insert   x~40
  M3 x various SHCS                   x~40
  M4 Shoulder Bolt + Spring           x8  (bumper floating mount)
  10mm Aluminum Standoff (ESP32/Pi)   x8
  XT60 Connector Pair                 x1
  JST-XH Balance Connector            x1

────────────────────────────────────────────────────────────────────────────
PRINT SETTINGS (per-part recommendation)
────────────────────────────────────────────────────────────────────────────
  Structural PETG parts (base, frame, brackets, hubs):
    0.2mm layer height, 3-4 perimeters, 4 top/bottom layers,
    50% infill (base/hub) or 30% infill (covers/brackets),
    0.4mm nozzle, 240C/80C, supports on overhangs > 45 deg.
  Clear PETG LiDAR dome: printed separately, 2 perimeters, 0% infill
    (vase-mode optional), slow speed for optical clarity.
  TPU 95A parts (bumpers, gaskets): 0.2mm layer, 2 perimeters,
    15-20% infill, slow print speed (20-30mm/s), direct drive
    extruder strongly recommended.

────────────────────────────────────────────────────────────────────────────
ASSEMBLY INSTRUCTIONS
────────────────────────────────────────────────────────────────────────────
 1. Press M3 brass heat-set inserts into all bosses on base_plate,
    mid_frame, and top_cover using a soldering iron at ~250C.
 2. Slide battery pack into base_plate tray from the rear; secure
    with battery_retainer thumb screw (tool-required access).
 3. Bolt motor_mount_bracket L/R to base_plate motor pockets;
    insert JGA25-370 motors, close split-collar clamp, tighten
    M3 pinch bolt. Press wheel_hub onto D-shaft, lock set screw.
 4. Snap caster_housing F/R into base_plate recesses; press-fit
    15mm ball casters, confirm retention clip engages.
 5. Stack mid_frame onto base_plate, securing with M3 SHCS into
    heat-set inserts (frame walls align with base plate bosses).
 6. Mount ESP32-S3 on front standoffs; mount DRV8833 near ESP32
    on 15mm standoffs (thermal pad to chassis floor beneath);
    mount Raspberry Pi 5 on center platform standoffs (25mm up,
    10mm clearance maintained below for airflow); mount power
    distribution board on rear standoffs above battery.
 7. Adhesive-mount BNO055 IMU on base_plate locating pins,
    centered, vibration isolated.
 8. Install camera_mount_front (15 deg up-tilt) at front, and
    camera_mount_floor (45 deg down-tilt) on the underside front;
    snap-fit Pi Camera Module 3 Wide units with TPU gasket.
 9. Install YDLIDAR X4 on mid_frame top ring (3x M3, 60mm PCD);
    route 6-pin JST cable through center shaft.
10. Route all internal cabling through base_plate and mid_frame
    channels (min. bend radius 10mm, 20mm service loops at
    connectors); snap channel cover strips over open runs.
11. Install bumper_front / bumper_rear on M4 shoulder bolts with
    springs (10mm floating travel); confirm microswitch triggers
    at 5mm compression; press WS2812B LED rings into bumper
    channel, light-pipe diffuser faces outward.
12. Press gasket_pi under Raspberry Pi platform, gasket_motor
    onto each motor mounting face, gasket_top onto top_cover
    perimeter lip.
13. Panel-mount 16mm E-Stop button through top_cover rear hole,
    wire NC contact in series with motor power.
14. Lower top_cover onto mid_frame; engage 4x corner snap
    latches; confirm SD-card slot aligns with Pi 5 SD reader and
    dome sits centered over LiDAR ring.
    ORDER: Battery -> Motors -> Electronics -> Cables -> Top Cover
"""

import cadquery as cq
from cadquery import exporters
import math

# ════════════════════════════════════════════════════════════════════════
# GLOBAL PARAMETERS
# ════════════════════════════════════════════════════════════════════════

CHASSIS_L = 300.0
CHASSIS_W = 240.0
CHASSIS_H_NO_LIDAR = 150.0
GROUND_CLEARANCE = 15.0
WHEELBASE = 200.0          # center-to-center track width

BASE_T = 5.0                # base plate thickness
WALL_T = 3.0                 # mid frame wall thickness
TOP_T = 2.5                  # top cover thickness
RIB_T = 5.0

FILLET_EDGE = 3.0             # child-safety min edge radius
FILLET_INTERNAL = 2.0         # min internal corner fillet for FDM

# --- M3 heat-set insert boss standard ---
INSERT_PILOT_D = 4.2
INSERT_PILOT_DEPTH = 3.5
INSERT_BOSS_OD = 10.0
INSERT_BOSS_H = 5.0

# --- Motors ---
MOTOR_OFFSET_Y = WHEELBASE / 2.0     # 100mm from centerline (±)
MOTOR_BODY_D = 25.0
MOTOR_BODY_L = 37.0
MOTOR_SHAFT_H = 32.5                  # from ground
MOTOR_FACE_W = 25.0
MOTOR_FACE_H = 16.0
MOTOR_HOLE_PITCH = 18.0

# --- Wheels ---
WHEEL_D = 65.0
WHEEL_W = 30.0

# --- Casters ---
CASTER_BALL_D = 15.0
CASTER_FRONT_X = 120.0
CASTER_REAR_X = -120.0

# --- Raspberry Pi 5 ---
PI_L, PI_W = 85.0, 56.0
PI_HOLE_X, PI_HOLE_Y = 58.0, 49.0
PI_ELEV = 25.0

# --- ESP32-S3 ---
ESP_L, ESP_W = 55.0, 28.0
ESP_HOLE_X, ESP_HOLE_Y = 48.0, 21.0
ESP_STANDOFF_H = 10.0

# --- DRV8833 ---
DRV_L, DRV_W = 20.0, 20.0
DRV_STANDOFF_H = 15.0

# --- LiDAR ---
LIDAR_D = 70.0
LIDAR_H = 40.0
LIDAR_PCD = 60.0
DOME_OD = 80.0
DOME_H = 60.0
DOME_WALL = 2.0

# --- Battery ---
BATT_L, BATT_W, BATT_H = 110.0, 75.0, 25.0

# --- Power distribution board ---
PDB_L, PDB_W = 50.0, 30.0
PDB_STANDOFF_H = 15.0

# --- LED ring / bumper ---
LED_RING_OD = 80.0

CABLE_CHANNEL_W = 8.0
CABLE_CHANNEL_H = 5.0


def insert_boss(wp, x, y, top_face_z, boss_od=INSERT_BOSS_OD,
                 boss_h=INSERT_BOSS_H, pilot_d=INSERT_PILOT_D,
                 pilot_depth=INSERT_PILOT_DEPTH):
    """Add a cylindrical M3 heat-set insert boss with pilot hole at (x,y)."""
    boss = (cq.Workplane("XY", origin=(x, y, top_face_z))
            .circle(boss_od / 2.0).extrude(boss_h))
    pilot = (cq.Workplane("XY", origin=(x, y, top_face_z + boss_h))
             .circle(pilot_d / 2.0).extrude(-pilot_depth))
    return wp.union(boss).cut(pilot)


def insert_boss_array(wp, points, z):
    for (x, y) in points:
        wp = insert_boss(wp, x, y, z)
    return wp


# ════════════════════════════════════════════════════════════════════════
# PART A — BASE PLATE
# ════════════════════════════════════════════════════════════════════════

def make_base_plate():
    plate = (cq.Workplane("XY")
             .box(CHASSIS_L, CHASSIS_W, BASE_T, centered=(True, True, False)))

    # Ventilation grid (center region, avoid motor/battery zones)
    vent_pts = []
    for xi in range(-60, 61, 10):
        for yi in range(-30, 31, 10):
            vent_pts.append((xi, yi))
    vent_holes = (cq.Workplane("XY", origin=(0, 0, 0))
                  .pushPoints(vent_pts)
                  .circle(1.5)
                  .extrude(BASE_T + 2))
    plate = plate.cut(vent_holes)

    # Motor mount blocks (integral, 5mm walls) — pockets for split-collar
    # bracket footprint (25x16mm face, 2x M3 on 18mm centers) each side
    for side in (1, -1):
        y = side * MOTOR_OFFSET_Y
        block = (cq.Workplane("XY", origin=(-CHASSIS_L / 2 + 40, y, 0))
                 .box(30, 26, BASE_T + 10, centered=(True, True, False)))
        plate = plate.union(block)
        mount_pts = [(-CHASSIS_L / 2 + 40 - MOTOR_HOLE_PITCH / 2, y),
                     (-CHASSIS_L / 2 + 40 + MOTOR_HOLE_PITCH / 2, y)]
        plate = insert_boss_array(plate, mount_pts, BASE_T + 10)

    # Caster snap-fit recesses (front & rear, on centerline)
    for cx in (CASTER_FRONT_X, CASTER_REAR_X):
        recess = (cq.Workplane("XY", origin=(cx, 0, 0))
                  .box(22, 22, 8, centered=(True, True, False)))
        plate = plate.cut(recess)

    # Battery tray rails (C-channel, 3mm lip), centered, slides from rear
    rail_y_offsets = [BATT_W / 2 + 2, -(BATT_W / 2 + 2)]
    for ry in rail_y_offsets:
        rail = (cq.Workplane("XY", origin=(0, ry, BASE_T))
                .box(BATT_L + 20, 6, 6, centered=(True, True, False)))
        lip = (cq.Workplane("XY", origin=(0, ry - 3 * (1 if ry > 0 else -1), BASE_T + 6))
               .box(BATT_L + 20, 3, 3, centered=(True, True, False)))
        plate = plate.union(rail).union(lip)

    # Cable channel down the centerline (radiused corners) from motors to center
    channel = (cq.Workplane("XY", origin=(0, 0, BASE_T))
               .box(CHASSIS_L - 60, CABLE_CHANNEL_W, CABLE_CHANNEL_H,
                    centered=(True, True, False)))
    plate = plate.cut(channel)

    # IMU locating pins (2x Ø2mm, 8mm apart, centered)
    for px in (-4, 4):
        pin = (cq.Workplane("XY", origin=(px, 0, BASE_T))
               .circle(1.0).extrude(2.0))
        plate = plate.union(pin)

    # 4x heat-set boss around perimeter for mid-frame attachment
    perim_pts = [
        (CHASSIS_L / 2 - 15, CHASSIS_W / 2 - 15),
        (CHASSIS_L / 2 - 15, -(CHASSIS_W / 2 - 15)),
        (-(CHASSIS_L / 2 - 15), CHASSIS_W / 2 - 15),
        (-(CHASSIS_L / 2 - 15), -(CHASSIS_W / 2 - 15)),
    ]
    plate = insert_boss_array(plate, perim_pts, BASE_T)

    plate = plate.edges("|Z").fillet(FILLET_EDGE)
    return plate


# ════════════════════════════════════════════════════════════════════════
# PART B — MID FRAME
# ════════════════════════════════════════════════════════════════════════

def make_mid_frame():
    outer = (cq.Workplane("XY")
             .box(CHASSIS_L, CHASSIS_W, CHASSIS_H_NO_LIDAR,
                  centered=(True, True, False)))
    inner = (cq.Workplane("XY", origin=(0, 0, WALL_T))
             .box(CHASSIS_L - 2 * WALL_T, CHASSIS_W - 2 * WALL_T,
                  CHASSIS_H_NO_LIDAR, centered=(True, True, False)))
    frame = outer.cut(inner)

    # Structural ribs every 40mm along length
    for xi in range(int(-CHASSIS_L / 2) + 40, int(CHASSIS_L / 2), 40):
        rib = (cq.Workplane("XY", origin=(xi, 0, 0))
               .box(RIB_T, CHASSIS_W, CHASSIS_H_NO_LIDAR,
                    centered=(True, True, False)))
        rib = rib.cut(cq.Workplane("XY", origin=(xi, 0, WALL_T))
                      .box(RIB_T, CHASSIS_W - 2 * WALL_T, CHASSIS_H_NO_LIDAR,
                           centered=(True, True, False)))
        frame = frame.union(rib)

    # Pi mounting platform (center, 25mm up, ventilated below)
    pi_plat = (cq.Workplane("XY", origin=(0, 0, PI_ELEV))
               .box(PI_L + 10, PI_W + 10, 3, centered=(True, True, False)))
    frame = frame.union(pi_plat)
    pi_pts = [(PI_HOLE_X / 2, PI_HOLE_Y / 2), (PI_HOLE_X / 2, -PI_HOLE_Y / 2),
              (-PI_HOLE_X / 2, PI_HOLE_Y / 2), (-PI_HOLE_X / 2, -PI_HOLE_Y / 2)]
    frame = insert_boss_array(frame, pi_pts, PI_ELEV + 3)

    # ESP32 mounting shelf (front, 15mm from front edge)
    esp_x = CHASSIS_L / 2 - 15 - ESP_L / 2
    esp_shelf = (cq.Workplane("XY", origin=(esp_x, 0, 40))
                 .box(ESP_L + 10, ESP_W + 10, 3, centered=(True, True, False)))
    frame = frame.union(esp_shelf)
    esp_pts = [(esp_x + ESP_HOLE_X / 2, ESP_HOLE_Y / 2),
               (esp_x + ESP_HOLE_X / 2, -ESP_HOLE_Y / 2),
               (esp_x - ESP_HOLE_X / 2, ESP_HOLE_Y / 2),
               (esp_x - ESP_HOLE_X / 2, -ESP_HOLE_Y / 2)]
    frame = insert_boss_array(frame, esp_pts, 43)

    # Power distribution board mounting bosses (rear of center, above battery)
    pdb_x = -30
    pdb_pts = [(pdb_x + PDB_L / 2, PDB_W / 2), (pdb_x + PDB_L / 2, -PDB_W / 2),
               (pdb_x - PDB_L / 2, PDB_W / 2), (pdb_x - PDB_L / 2, -PDB_W / 2)]
    frame = insert_boss_array(frame, pdb_pts, BATT_H + 10)

    # Vertical cable raceway (10x10mm) along rear wall interior
    raceway = (cq.Workplane("XY", origin=(-CHASSIS_L / 2 + WALL_T + 5, 0, 0))
               .box(10, 10, CHASSIS_H_NO_LIDAR, centered=(True, True, False)))
    frame = frame.cut(raceway)

    # LiDAR mounting ring (top, 3x M3 bosses on 60mm PCD)
    ring = (cq.Workplane("XY", origin=(0, 0, CHASSIS_H_NO_LIDAR))
            .circle(LIDAR_D / 2 + 5).circle(LIDAR_D / 2 - 5)
            .extrude(6))
    frame = frame.union(ring)
    lidar_pts = []
    for i in range(3):
        ang = math.radians(120 * i)
        lidar_pts.append((LIDAR_PCD / 2 * math.cos(ang),
                           LIDAR_PCD / 2 * math.sin(ang)))
    frame = insert_boss_array(frame, lidar_pts, CHASSIS_H_NO_LIDAR + 6)

    frame = frame.edges("|Z").fillet(FILLET_EDGE)
    return frame


# ════════════════════════════════════════════════════════════════════════
# PART C — TOP COVER (with LiDAR dome)
# ════════════════════════════════════════════════════════════════════════

def make_top_cover():
    lid = (cq.Workplane("XY")
           .box(CHASSIS_L, CHASSIS_W, TOP_T, centered=(True, True, False)))

    # Perimeter lip (5mm, drops down to engage mid_frame)
    lip_outer = (cq.Workplane("XY", origin=(0, 0, -5))
                 .box(CHASSIS_L - 2 * WALL_T - 0.4, CHASSIS_W - 2 * WALL_T - 0.4, 5,
                      centered=(True, True, False)))
    lip_inner = (cq.Workplane("XY", origin=(0, 0, -5))
                 .box(CHASSIS_L - 2 * WALL_T - 0.4 - 2 * WALL_T,
                      CHASSIS_W - 2 * WALL_T - 0.4 - 2 * WALL_T, 5,
                      centered=(True, True, False)))
    lip = lip_outer.cut(lip_inner)
    lid = lid.union(lip)

    # LiDAR dome base flange + clear dome
    flange = (cq.Workplane("XY", origin=(0, 0, TOP_T))
              .circle(DOME_OD / 2 + 5).extrude(3))
    lid = lid.union(flange)
    dome_pts = []
    for i in range(3):
        ang = math.radians(120 * i)
        dome_pts.append((LIDAR_PCD / 2 * math.cos(ang),
                          LIDAR_PCD / 2 * math.sin(ang)))
    dome_clr = (cq.Workplane("XY", origin=(0, 0, 0))
                .pushPoints(dome_pts).circle(1.6).extrude(TOP_T + 3 + 1))
    lid = lid.cut(dome_clr)

    dome_outer = (cq.Workplane("XY", origin=(0, 0, TOP_T + 3))
                  .circle(DOME_OD / 2).extrude(DOME_H))
    dome_inner = (cq.Workplane("XY", origin=(0, 0, TOP_T + 3))
                  .circle(DOME_OD / 2 - DOME_WALL).extrude(DOME_H + 1))
    dome = dome_outer.cut(dome_inner)
    dome = dome.faces(">Z").shell(-DOME_WALL)
    lid = lid.union(dome)

    # Ventilation slots (2x30mm, rear)
    for i in (-1, 1):
        slot = (cq.Workplane("XY",
                              origin=(-CHASSIS_L / 2 + 20, i * 10, 0))
                .box(2, 30, TOP_T + 2, centered=(True, True, False)))
        lid = lid.cut(slot)

    # E-Stop button hole (Ø16.5mm), top-rear
    estop_pos = (-CHASSIS_L / 2 + 40, 0)
    estop_hole = (cq.Workplane("XY", origin=(*estop_pos, 0))
                  .circle(16.5 / 2).extrude(TOP_T + 2))
    lid = lid.cut(estop_hole)

    # Status LED light-pipe window (frosted), front edge
    led_window = (cq.Workplane("XY", origin=(CHASSIS_L / 2 - 20, 0, 0))
                  .box(20, 6, TOP_T + 2, centered=(True, True, False)))
    lid = lid.cut(led_window)

    # SD card access slot (rear, 15x3mm)
    sd_slot = (cq.Workplane("XY", origin=(-CHASSIS_L / 2 + 5, 20, 0))
               .box(3, 15, TOP_T + 2, centered=(True, True, False)))
    lid = lid.cut(sd_slot)

    # 4x corner snap latches (2mm undercut cantilever)
    for sx in (1, -1):
        for sy in (1, -1):
            lx = sx * (CHASSIS_L / 2 - 12)
            ly = sy * (CHASSIS_W / 2 - 12)
            latch = (cq.Workplane("XY", origin=(lx, ly, -9))
                     .box(8, 4, 6, centered=(True, True, False)))
            hook = (cq.Workplane("XY", origin=(lx, ly, -3))
                    .box(10, 4, 2, centered=(True, True, False)))
            lid = lid.union(latch).union(hook)

    lid = lid.edges("|Z").fillet(FILLET_EDGE)
    return lid


# ════════════════════════════════════════════════════════════════════════
# PART D — MOTOR MOUNT BRACKET (split collar clamp)
# ════════════════════════════════════════════════════════════════════════

def make_motor_mount_bracket(mirror=False):
    body = (cq.Workplane("XY")
            .box(MOTOR_FACE_W, MOTOR_FACE_H, 20, centered=(True, True, False)))
    clamp_bore = (cq.Workplane("XY", origin=(0, 0, 5))
                  .circle(MOTOR_BODY_D / 2 + 0.2).extrude(20))
    body = body.union(
        cq.Workplane("XY", origin=(0, 0, 5)).circle(MOTOR_BODY_D / 2 + 4).extrude(20)
    ).cut(clamp_bore)

    # split gap 2mm with M3 pinch bolt clearance
    gap = (cq.Workplane("XY", origin=(0, MOTOR_BODY_D / 2 + 2, 5))
           .box(2, 8, 22, centered=(True, True, False)))
    body = body.cut(gap)
    pinch_hole = (cq.Workplane("YZ", origin=(0, MOTOR_BODY_D / 2 + 6, 15))
                  .circle(1.6).extrude(20))
    body = body.cut(pinch_hole)

    # mounting face 2x M3 clearance on 18mm centers
    for hy in (MOTOR_HOLE_PITCH / 2, -MOTOR_HOLE_PITCH / 2):
        hole = (cq.Workplane("XY", origin=(0, hy, -1))
                .circle(1.65).extrude(22))
        body = body.cut(hole)

    # integral cable channel exit
    chan = (cq.Workplane("XY", origin=(0, 0, 15))
            .box(CABLE_CHANNEL_W, CABLE_CHANNEL_H, 30, centered=(True, True, False)))
    body = body.cut(chan)

    if mirror:
        body = body.mirror("YZ")

    body = body.edges("|Z").fillet(FILLET_INTERNAL)
    return body


# ════════════════════════════════════════════════════════════════════════
# PART E — WHEEL HUB
# ════════════════════════════════════════════════════════════════════════

def make_wheel_hub():
    hub = (cq.Workplane("XY").circle(WHEEL_D / 2).extrude(15))

    # D-bore for motor shaft (approx 6mm dia with flat)
    dbore = (cq.Workplane("XY").circle(3.0).extrude(15))
    flat = (cq.Workplane("XY", origin=(1.2, 0, 0))
            .box(6, 6, 15, centered=(True, True, False)))
    hub = hub.cut(dbore).union(
        cq.Workplane("XY").circle(3.0).extrude(15).intersect(
            cq.Workplane("XY", origin=(0, 0, 0)).box(6, 6, 15, centered=(True, True, False))
        )
    )
    hub = (cq.Workplane("XY").circle(WHEEL_D / 2).extrude(15)
           .cut(cq.Workplane("XY").circle(3.2).extrude(15))
           .cut(cq.Workplane("XY", origin=(4.4, 0, 0)).box(4, 6, 15, centered=(True, True, False))))

    # set screw hole M3 x 3mm deep, radial
    setscrew = (cq.Workplane("YZ", origin=(0, 0, 7.5))
                .circle(1.5).extrude(WHEEL_D / 2 + 1))
    hub = hub.cut(setscrew)

    # tire retention groove: 2mm deep, 30mm wide (centered)
    groove_outer = cq.Workplane("XY", origin=(0, 0, 6.5)).circle(WHEEL_D / 2).extrude(30)
    groove_inner = cq.Workplane("XY", origin=(0, 0, 6.5)).circle(WHEEL_D / 2 - 2).extrude(30)
    hub = hub.cut(groove_outer.cut(groove_inner))

    # 5-spoke pattern (lightening, 3mm thick spokes) — cut pockets between spokes
    for i in range(5):
        ang = 72 * i
        pocket = (cq.Workplane("XY").transformed(rotate=(0, 0, ang))
                  .center(WHEEL_D / 4, 0)
                  .box(WHEEL_D / 3, 8, 15, centered=(True, True, False)))
        hub = hub.cut(pocket)

    hub = hub.edges("|Z").fillet(1.5)
    return hub


# ════════════════════════════════════════════════════════════════════════
# PART F — CASTER HOUSING (snap-fit for 15mm ball)
# ════════════════════════════════════════════════════════════════════════

def make_caster_housing():
    base = (cq.Workplane("XY").box(20, 20, 8, centered=(True, True, False)))
    socket = (cq.Workplane("XY", origin=(0, 0, 2))
              .sphere(CASTER_BALL_D / 2 + 0.3))
    base = base.cut(socket)
    # open bottom for ball protrusion
    open_bottom = (cq.Workplane("XY", origin=(0, 0, -1))
                   .circle(CASTER_BALL_D / 2 - 1).extrude(4))
    base = base.cut(open_bottom)
    # retention clip flex fingers (1mm)
    for sx in (1, -1):
        finger = (cq.Workplane("XY", origin=(sx * 6, 0, 1))
                  .box(1, 6, 6, centered=(True, True, False)))
        base = base.cut(finger)
    # central M3 mounting hole
    mhole = cq.Workplane("XY", origin=(0, 0, -1)).circle(1.65).extrude(10)
    base = base.cut(mhole)
    base = base.edges("|Z").fillet(2.0)
    return base


# ════════════════════════════════════════════════════════════════════════
# PART G — CAMERA MOUNT (Front / Horizon, 15deg up-tilt)
# ════════════════════════════════════════════════════════════════════════

def make_camera_mount_front():
    plate = cq.Workplane("XY").box(30, 29, 4, centered=(True, True, False))
    gasket_pocket = (cq.Workplane("XY", origin=(0, 0, 4))
                      .box(25, 24, 3, centered=(True, True, False)))
    plate = plate.cut(gasket_pocket)
    lens_hole = cq.Workplane("XY", origin=(0, 0, -1)).circle(4).extrude(6)
    plate = plate.cut(lens_hole)
    # strain relief anchor
    anchor = (cq.Workplane("XY", origin=(12, 0, 0)).box(4, 4, 6, centered=(True, True, False)))
    tie_hole = cq.Workplane("YZ", origin=(12, 0, 3)).circle(1).extrude(4)
    plate = plate.union(anchor).cut(tie_hole)
    mount = plate.rotate((0, 0, 0), (0, 1, 0), -15)
    mount = mount.edges("|Z").fillet(1.5)
    return mount


# ════════════════════════════════════════════════════════════════════════
# PART H — CAMERA MOUNT (Floor, 45deg down-tilt)
# ════════════════════════════════════════════════════════════════════════

def make_camera_mount_floor():
    plate = cq.Workplane("XY").box(30, 29, 4, centered=(True, True, False))
    gasket_pocket = (cq.Workplane("XY", origin=(0, 0, 4))
                      .box(25, 24, 3, centered=(True, True, False)))
    plate = plate.cut(gasket_pocket)
    lens_hole = cq.Workplane("XY", origin=(0, 0, -1)).circle(4).extrude(6)
    plate = plate.cut(lens_hole)
    window_recess = (cq.Workplane("XY", origin=(0, 0, -1)).box(20, 20, 1, centered=(True, True, False)))
    plate = plate.cut(window_recess)
    mount = plate.rotate((0, 0, 0), (0, 1, 0), 45)
    mount = mount.edges("|Z").fillet(1.5)
    return mount


# ════════════════════════════════════════════════════════════════════════
# PART I — BATTERY RETAINER (sliding lock, thumb screw)
# ════════════════════════════════════════════════════════════════════════

def make_battery_retainer():
    plate = cq.Workplane("XY").box(BATT_W - 4, 20, 3, centered=(True, True, False))
    lip = (cq.Workplane("XY", origin=(0, 8, 3))
           .box(BATT_W - 4, 4, 2, centered=(True, True, False)))
    plate = plate.union(lip)
    # thumb screw boss M3x20 knurled
    screw_boss = cq.Workplane("XY", origin=(0, -6, 0)).circle(5).extrude(6)
    screw_hole = cq.Workplane("XY", origin=(0, -6, -1)).circle(1.65).extrude(8)
    plate = plate.union(screw_boss).cut(screw_hole)
    plate = plate.edges("|Z").fillet(1.5)
    return plate


# ════════════════════════════════════════════════════════════════════════
# PART J — BUMPER (Front / Rear) — TPU
# ════════════════════════════════════════════════════════════════════════

def make_bumper(front=True):
    x_sign = 1 if front else -1
    outer = (cq.Workplane("XY", origin=(x_sign * CHASSIS_L / 2, 0, 0))
             .box(20, CHASSIS_W - 20, 60, centered=(True, True, False)))
    shell = outer.shell(-5)  # 5mm wall, hollow interior

    # LED ring channel (80mm dia recess) on outward face
    ring_face_x = x_sign * (CHASSIS_L / 2 + 9)
    ring_cut_outer = (cq.Workplane("YZ", origin=(ring_face_x, 0, 30))
                       .circle(LED_RING_OD / 2).extrude(3 * x_sign))
    ring_cut_inner = (cq.Workplane("YZ", origin=(ring_face_x, 0, 30))
                       .circle(LED_RING_OD / 2 - 6).extrude(3 * x_sign))
    ring_channel = ring_cut_outer.cut(ring_cut_inner)
    shell = shell.union(ring_channel)

    # microswitch mounting posts (x2) inside
    for sy in (30, -30):
        post = (cq.Workplane("XY", origin=(x_sign * (CHASSIS_L / 2 + 5), sy, 15))
                .box(5, 5, 20, centered=(True, True, False)))
        shell = shell.union(post)

    # ToF sensor flush-mount cutouts (2x, 60mm apart)
    for ty in (30, -30):
        tof_hole = (cq.Workplane("YZ", origin=(ring_face_x, ty, 30))
                    .box(6.4, 3.0, 6, centered=(True, True, False)))
        shell = shell.cut(tof_hole)

    shell = shell.edges("|X").fillet(FILLET_EDGE)
    return shell


# ════════════════════════════════════════════════════════════════════════
# PART K — GASKETS (TPU seals)
# ════════════════════════════════════════════════════════════════════════

def make_gasket_top():
    outer = cq.Workplane("XY").box(CHASSIS_L - 2 * WALL_T + 4,
                                    CHASSIS_W - 2 * WALL_T + 4, 2,
                                    centered=(True, True, False))
    inner = cq.Workplane("XY").box(CHASSIS_L - 2 * WALL_T - 4,
                                    CHASSIS_W - 2 * WALL_T - 4, 2,
                                    centered=(True, True, False))
    return outer.cut(inner)


def make_gasket_pi():
    return cq.Workplane("XY").box(PI_L, PI_W, 3, centered=(True, True, False))


def make_gasket_motor():
    outer = cq.Workplane("XY").circle(MOTOR_BODY_D / 2 + 2).extrude(2)
    inner = cq.Workplane("XY").circle(MOTOR_BODY_D / 2 - 1).extrude(2)
    return outer.cut(inner)


# ════════════════════════════════════════════════════════════════════════
# MAIN — BUILD, ASSEMBLE, EXPORT
# ════════════════════════════════════════════════════════════════════════

def build_assembly():
    """Assemble all parts into one cq.Assembly for visualization/inspection."""
    asm = cq.Assembly(name="Advika_3_0")
    asm.add(make_base_plate(), name="base_plate", loc=cq.Location(cq.Vector(0, 0, 0)))
    asm.add(make_mid_frame(), name="mid_frame", loc=cq.Location(cq.Vector(0, 0, BASE_T)))
    asm.add(make_top_cover(), name="top_cover",
            loc=cq.Location(cq.Vector(0, 0, BASE_T + CHASSIS_H_NO_LIDAR)))

    asm.add(make_motor_mount_bracket(mirror=False), name="motor_mount_L",
            loc=cq.Location(cq.Vector(-CHASSIS_L / 2 + 40, MOTOR_OFFSET_Y, MOTOR_SHAFT_H)))
    asm.add(make_motor_mount_bracket(mirror=True), name="motor_mount_R",
            loc=cq.Location(cq.Vector(-CHASSIS_L / 2 + 40, -MOTOR_OFFSET_Y, MOTOR_SHAFT_H)))

    asm.add(make_wheel_hub(), name="wheel_hub_L",
            loc=cq.Location(cq.Vector(-CHASSIS_L / 2 + 40, MOTOR_OFFSET_Y + 20, MOTOR_SHAFT_H)))
    asm.add(make_wheel_hub(), name="wheel_hub_R",
            loc=cq.Location(cq.Vector(-CHASSIS_L / 2 + 40, -MOTOR_OFFSET_Y - 20, MOTOR_SHAFT_H)))

    asm.add(make_caster_housing(), name="caster_housing_F",
            loc=cq.Location(cq.Vector(CASTER_FRONT_X, 0, 0)))
    asm.add(make_caster_housing(), name="caster_housing_R",
            loc=cq.Location(cq.Vector(CASTER_REAR_X, 0, 0)))

    asm.add(make_camera_mount_front(), name="camera_mount_front",
            loc=cq.Location(cq.Vector(CHASSIS_L / 2 - 10, 0, 100)))
    asm.add(make_camera_mount_floor(), name="camera_mount_floor",
            loc=cq.Location(cq.Vector(CHASSIS_L / 2 - 30, 0, 25)))

    asm.add(make_battery_retainer(), name="battery_retainer",
            loc=cq.Location(cq.Vector(0, 0, BASE_T)))

    asm.add(make_bumper(front=True), name="bumper_front",
            loc=cq.Location(cq.Vector(0, 0, BASE_T)))
    asm.add(make_bumper(front=False), name="bumper_rear",
            loc=cq.Location(cq.Vector(0, 0, BASE_T)))

    asm.add(make_gasket_top(), name="gasket_top",
            loc=cq.Location(cq.Vector(0, 0, BASE_T + CHASSIS_H_NO_LIDAR)))
    asm.add(make_gasket_pi(), name="gasket_pi",
            loc=cq.Location(cq.Vector(0, 0, BASE_T + PI_ELEV)))
    asm.add(make_gasket_motor(), name="gasket_motor_L",
            loc=cq.Location(cq.Vector(-CHASSIS_L / 2 + 40, MOTOR_OFFSET_Y, MOTOR_SHAFT_H)))
    asm.add(make_gasket_motor(), name="gasket_motor_R",
            loc=cq.Location(cq.Vector(-CHASSIS_L / 2 + 40, -MOTOR_OFFSET_Y, MOTOR_SHAFT_H)))

    return asm


def export_all_stl(out_dir="."):
    parts = {
        "advika30_base_plate.stl": make_base_plate(),
        "advika30_mid_frame.stl": make_mid_frame(),
        "advika30_top_cover.stl": make_top_cover(),
        "advika30_motor_mount_L.stl": make_motor_mount_bracket(mirror=False),
        "advika30_motor_mount_R.stl": make_motor_mount_bracket(mirror=True),
        "advika30_wheel_hub_L.stl": make_wheel_hub(),
        "advika30_wheel_hub_R.stl": make_wheel_hub(),
        "advika30_caster_housing_F.stl": make_caster_housing(),
        "advika30_caster_housing_R.stl": make_caster_housing(),
        "advika30_camera_mount_front.stl": make_camera_mount_front(),
        "advika30_camera_mount_floor.stl": make_camera_mount_floor(),
        "advika30_battery_retainer.stl": make_battery_retainer(),
        "advika30_bumper_front.stl": make_bumper(front=True),
        "advika30_bumper_rear.stl": make_bumper(front=False),
        "advika30_gasket_top.stl": make_gasket_top(),
        "advika30_gasket_pi.stl": make_gasket_pi(),
        "advika30_gasket_motor.stl": make_gasket_motor(),
    }

    for fname, part in parts.items():
        path = f"{out_dir}/{fname}"
        exporters.export(part, path)
        print(f"Exported: {path}")

    return parts


if __name__ == "__main__":
    print("Building Advika 3.0 part set...")
    export_all_stl(out_dir=".")

    print("\nBuilding full assembly for visualization...")
    assembly = build_assembly()
    try:
        assembly.save("advika30_assembly.step")
        print("Exported: advika30_assembly.step")
    except Exception as e:
        print(f"Assembly STEP export skipped: {e}")

    print("\nDone. 17 STL files exported for FDM printing.")
