# Fusion 360 STL Files — PRIMARY DESIGN
**Advika 3.0 — Frozen: 2026-07-26**

This folder contains your **Fusion 360 design STLs** — these are the real robot parts.
All other CAD paths (CadQuery, FreeCAD) are auto-generated reference copies.

---

## Files in this folder

| STL File | Robot Part | Material | Notes |
|----------|-----------|----------|-------|
| `advika_chassis.stl` | Base plate + mid frame combined | PETG (blue) | Main structural body |
| `advika_top_dome.stl` | Top cover + LiDAR dome | PETG (white/translucent) | Combined part |
| `advika_wheel_hub_L.stl` | Left wheel hub | PETG (black) | 6mm D-shaft bore |
| `advika_wheel_hub_R.stl` | Right wheel hub | PETG (black) | Mirrored |
| `advika_bumper_front.stl` | Front bumper | TPU 95A (red) | With LED channel |
| `advika_bumper_rear.stl` | Rear bumper | TPU 95A (red) | Mirrored |
| `advika_camera_horizon.stl` | Front camera mount | PETG (black) | 15° upward tilt |
| `advika_camera_floor.stl` | Floor camera mount | PETG (black) | 45° downward tilt |
| `advika_motor_mount_L.stl` | Left motor mount bracket | PETG (blue) | Split collar clamp |
| `advika_motor_mount_R.stl` | Right motor mount bracket | PETG (blue) | Mirrored |
| `advika_imu_mount.stl` | BNO055 IMU mount | PETG (grey) | Vibration-isolated |
| `advika_lidar_tower.stl` | LiDAR tower | PETG (white) | For YDLIDAR X4 |
| `advika_top_dome.stl` | Top dome / LiDAR cover | PETG (clear) | Translucent |
| `advika_battery_tray.stl` | Battery retainer | PETG (orange) | 3S2P 18650 pack |
| `advika_esp32_enclosure.stl` | ESP32-S3 enclosure | PETG (grey) | USB-C access |
| `advika_axle_shaft.stl` | Axle shaft | PETG (black) | D-profile |

---

## How these are used

1. **Simulation**: URDF references these STLs via `package://advika_description/stl/`
2. **3D Printing**: Export directly to your slicer (Cura, PrusaSlicer)
3. **Real Robot**: Print with PETG 240°C / TPU 220°C settings

## URDF Reference

```xml
<!-- Example from advika.urdf -->
<mesh filename="package://advika_description/stl/advika_chassis.stl"/>
```

## Print Settings

See: `../../docs/PRINT_SETTINGS.md`

| Part | Material | Nozzle | Bed | Speed | Infill |
|------|----------|--------|-----|-------|--------|
| Chassis | PETG | 240°C | 80°C | 50mm/s | 50% |
| Top dome | Clear PETG | 240°C | 75°C | 30mm/s | 0% (vase) |
| Motor mounts | PETG | 240°C | 80°C | 50mm/s | 30% |
| Bumpers | TPU 95A | 220°C | 50°C | 20mm/s | 40% |
| Camera mounts | PETG | 240°C | 80°C | 50mm/s | 30% |
| Battery tray | PETG | 240°C | 80°C | 50mm/s | 30% |

---

## Other CAD Locations

```
advika_description/stl/     ← YOUR FUSION 360 FILES (HERE — primary)
advika_cad/meshes/          ← CadQuery auto-generated (21 parts, reference)
advika_cad/meshes_freecad/ ← FreeCAD auto-generated (23 parts, reference)
advika_cad/step/            ← CadQuery STEP exports
advika_cad/step_freecad/    ← FreeCAD STEP exports
```

---

## Electronics Schematic

For the electronic circuit diagram, use **KiCad** (free, cross-platform) or **EasyEDA** (browser-based):

- **KiCad**: Best for professional schematics + PCB design
- **EasyEDA**: Best for quick online PCB prototyping with Chinese manufacturers

See: `../../docs/Wiring_README.md` (complete pinout + power distribution)
See: `../../docs/wiring_diagram.svg` (full-color schematic diagram)

Fusion 360 has a "Circuit" workspace but it's limited — KiCad is better for the full schematic + PCB layout.