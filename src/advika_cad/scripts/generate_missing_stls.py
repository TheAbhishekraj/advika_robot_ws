#!/usr/bin/env python3
"""
ADVIKA 3.0 — Generate missing STLs (lidar disk, tof bar, imu board, display)
Uses CadQuery 2.x only. Run from repo root:
  python src/advika_cad/scripts/generate_missing_stls.py
"""

import math
import os
import sys
import cadquery as cq
from cadquery import exporters

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAD_ROOT = os.path.dirname(SCRIPT_DIR)   # src/advika_cad
MESHES_DIR = os.path.join(CAD_ROOT, "meshes")
os.makedirs(MESHES_DIR, exist_ok=True)


def make_lidar_disk():
    """LiDAR YDLIDAR X4 — 70mm disk with center bore and 3 mounting holes on 60mm PCD."""
    body = (cq.Workplane("XY")
            .circle(35).extrude(8)
            .faces(">Z").workplane().circle(30).extrude(4))
    # Center bore
    body = body.cut(cq.Workplane("XY").circle(12).extrude(20))
    # 3x M3 bolt holes on 60mm PCD
    for i in range(3):
        ang = 120 * i
        hx = 30 * (1 if i == 0 else -0.5)
        hy = 30 * (0.866 if i == 1 else -0.866)
        body = body.cut(cq.Workplane("XY", origin=(hx, hy, 0)).circle(1.65).extrude(15))
    return body


def make_tof_bar():
    """ToF sensor bar — 80×15×3mm with 2 sensor cutouts at 30mm spacing."""
    bar = cq.Workplane("XY").box(80, 15, 3, centered=True)
    for sx in (-30, 30):
        # Sensor pocket 6.4×3mm
        bar = bar.cut(cq.Workplane("XY", origin=(sx, 0, 0)).box(6.4, 3.0, 2).faces(">Z").workplane().circle(2).cutThruAll())
        # Wire channel
        bar = bar.cut(cq.Workplane("XY", origin=(sx, 0, -1)).box(2, 2, 4))
    # 4x M2 mounting holes at corners
    for mx in (-35, 35):
        for my in (-5, 5):
            bar = bar.cut(cq.Workplane("XY", origin=(mx, my, 0)).circle(1.1).extrude(5))
    return bar


def make_imu_board():
    """BNO055 IMU breakout — 20×27×1.6mm board with corner holes."""
    board = cq.Workplane("XY").box(20, 27, 1.6, centered=True)
    # Chip recess
    board = board.cut(cq.Workplane("XY").box(12, 15, 0.5).translate((0, 0, 1.1)))
    # 4x M2 mounting holes at corners (5mm from edges)
    for mx in (-7, 7):
        for my in (-9.5, 9.5):
            board = board.cut(cq.Workplane("XY", origin=(mx, my, 0)).circle(0.8).extrude(5))
    return board


def make_display():
    """SSD1306 OLED 128×64 display — 27.3×27.8mm board with 25.7×13.1mm window cutout."""
    board = cq.Workplane("XY").box(27.3, 27.8, 1.5, centered=True)
    # Display window
    board = board.cut(cq.Workplane("XY").box(25.7, 13.1, 1.5).translate((0, 3, 0)))
    # FPC connector at bottom
    board = board.cut(cq.Workplane("XY").box(8, 3, 1.5).translate((0, -13, 0)))
    # 2x header pins
    for px in (-5, 5):
        board = board.cut(cq.Workplane("XY", origin=(px, -13.9, 0)).box(1.2, 1.2, 3).faces(">Z").workplane().circle(0.6).cutThruAll())
    return board


PARTS = [
    ("advika30_lidar_disk.stl",       make_lidar_disk),
    ("advika30_tof_bar.stl",           make_tof_bar),
    ("advika30_imu_board.stl",         make_imu_board),
    ("advika30_display.stl",           make_display),
]


def main():
    print("Generating missing STLs (CadQuery)...")
    for name, fn in PARTS:
        path = os.path.join(MESHES_DIR, name)
        try:
            part = fn()
            exporters.export(part, path)
            print(f"  OK {name}")
        except Exception as e:
            print(f"  FAIL {name}: {e}")
    count = len([f for f in os.listdir(MESHES_DIR) if f.endswith(".stl")])
    print(f"\nTotal STL files: {count}")
    print(f"Location: {MESHES_DIR}")


if __name__ == "__main__":
    main()