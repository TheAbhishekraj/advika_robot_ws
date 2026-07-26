# Fusion 360 STL Files — PRIMARY DESIGN
**Advika 3.0 — Frozen: 2026-07-26**

This folder contains your **Fusion 360 design STLs** — these are the real robot parts.
All other CAD paths (CadQuery, FreeCAD) are auto-generated reference copies.

---

## Files in this folder (17 STLs)

| STL File | Robot Part | Material | Print Settings |
|----------|-----------|----------|----------------|
| `advika_chassis.stl` | Base plate + mid frame | PETG (blue) | 240°C, 50mm/s, 50% infill |
| `advika_top_dome.stl` | Top cover + LiDAR dome | PETG (white/translucent) | 240°C, 30mm/s, vase |
| `advika_wheel_hub_L.stl` | Left wheel hub | PETG (black) | 240°C, 50mm/s, 50% infill |
| `advika_wheel_hub_R.stl` | Right wheel hub | PETG (black) | 240°C, 50mm/s, 50% infill |
| `advika_bumper_front.stl` | Front bumper | TPU 95A (red) | 220°C, 20mm/s, 40% infill |
| `advika_bumper_rear.stl` | Rear bumper | TPU 95A (red) | 220°C, 20mm/s, 40% infill |
| `advika_camera_horizon.stl` | Front camera mount | PETG (black) | 240°C, 50mm/s, 30% infill |
| `advika_camera_floor.stl` | Floor camera mount | PETG (black) | 240°C, 50mm/s, 30% infill |
| `advika_motor_mount_L.stl` | Left motor mount | PETG (blue) | 240°C, 50mm/s, 30% infill |
| `advika_motor_mount_R.stl` | Right motor mount | PETG (blue) | 240°C, 50mm/s, 30% infill |
| `advika_imu_mount.stl` | BNO055 IMU mount | PETG (grey) | 240°C, 50mm/s, 30% infill |
| `advika_lidar_tower.stl` | LiDAR tower | PETG (white) | 240°C, 50mm/s, 30% infill |
| `advika_battery_tray.stl` | Battery retainer | PETG (orange) | 240°C, 50mm/s, 30% infill |
| `advika_esp32_enclosure.stl` | ESP32-S3 enclosure box | PETG (grey) | 240°C, 50mm/s, 30% infill |
| `advika_esp32_lid.stl` | ESP32 enclosure lid | PETG (grey) | 240°C, 50mm/s, 20% infill |
| `advika_axle_shaft.stl` | Axle shaft | PETG (black) | 240°C, 50mm/s, 50% infill |
| `advika_esp32_enclosure.stl` | ESP32-S3 box | PETG (grey) | 240°C, 50mm/s, 30% infill |

---

## URDF Reference

```xml
<mesh filename="package://advika_description/stl/advika_chassis.stl"/>
```

---

## Other CAD Locations

```
advika_description/stl/     ← YOUR FUSION 360 FILES (HERE — primary)
advika_cad/meshes/          ← CadQuery auto-generated (reference only)
advika_cad/meshes_freecad/  ← FreeCAD auto-generated (reference only)
```

---

## Electronics

See: `../../docs/wiring_diagram.svg` (full schematic)
See: `../../docs/Wiring_README.md` (pinout + power distribution)

For PCB design: use **KiCad** (free) or **EasyEDA** (browser, free)