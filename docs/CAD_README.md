# CAD Chassis v3

## Advika 3.0 Chassis Design

This directory contains the 3D printable chassis files for Advika 3.0.

### Files
- `CAD_Chassis_v3.step` -- Full 3D assembly in STEP format (import into Fusion 360, SolidWorks, FreeCAD)
- `chassis_base.stl` -- Main chassis base plate (print in PETG, 3 perimeters, 30% infill)
- `chassis_lid.stl` -- Top cover/lid (print in PETG, 2 perimeters, 20% infill)
- `motor_mounts.stl` -- JGA25-370 motor mounts (print in PETG, 4 perimeters, 50% infill)
- `camera_bracket.stl` -- Dual camera mounting bracket
- `lidar_tower.stl` -- LD06 LiDAR mounting tower
- `tof_holder.stl` -- VL53L5CX ToF array holder
- `battery_tray.stl` -- 3S LiPo battery tray with strap slots

### Print Settings
- Material: PETG (recommended) or ABS
- Nozzle: 0.4mm
- Layer height: 0.2mm
- Infill: 30-50% for structural parts, 20% for covers
- Supports: Required for motor mounts and camera bracket

### Assembly Notes
1. Print all parts before assembly
2. Press-fit M3 brass threaded inserts into mounting holes
3. Mount motors first, then electronics tray
4. Route all cables through the internal cable channels
5. Install the E-Stop button on the rear panel before closing the lid
