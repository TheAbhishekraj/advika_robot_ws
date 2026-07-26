# ADVIKA 3.0 — Complete Setup & Usage Guide

## Table of Contents
1. [File Overview](#1-file-overview)
2. [Installation](#2-installation)
3. [How to Run the Script](#3-how-to-run-the-script)
4. [Verification After Each Step](#4-verification-after-each-step)
5. [How to Export STL Files](#5-how-to-export-stl-files)
6. [Troubleshooting](#6-troubleshooting)
7. [Component Specifications](#7-component-specifications)

---

## 1. File Overview

| File | Location | Purpose |
|------|----------|---------|
| `advika_3_0_generator.py` | `C:\Users\HP\` | Main Fusion 360 API script |
| `Advika_3_0_PDCA.md` | `C:\Users\HP\` | PDCA plan document |
| **NEW**: `ADVIKA_3_0_README.md` | `C:\Users\HP\` | This file |

### What the Script Creates (12 Components)

| # | Component | Dimensions |
|---|-----------|------------|
| 1 | Chassis Base | 300 × 240 × 5 mm |
| 2 | Motor Mount Left | 6mm shaft, 4× M3 holes |
| 3 | Motor Mount Right | Mirror of Left |
| 4 | Wheel Hub Left | 65mm diameter, 20mm thick |
| 5 | Wheel Hub Right | Mirror of Left |
| 6 | LiDAR Tower | 70mm base, 150mm height |
| 7 | Top Dome | 115mm radius, 80mm height |
| 8 | Horizon Camera Mount | 25 × 24 × 8 mm, 15° tilt |
| 9 | Floor Camera Mount | 25 × 24 × 8 mm, 45° tilt |
| 10 | IMU Mount | 20 × 20 × 5 mm |
| 11 | Battery Tray | 80 × 70 × 25 mm |
| 12 | Front Bumper | 280 × 30 × 20 mm |
| 13 | Rear Bumper | Mirror of Front |
| 14 | ESP32 Enclosure | 55 × 30 × 15 mm |

---

## 2. Installation

### Step 2.1: Copy Script to Fusion 360 Scripts Folder

**Windows:**
```
%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\
```
Full path: `C:\Users\HP\AppData\Roaming\Autodesk\Autodesk Fusion 360\API\Scripts\`

**Create folder structure:**
```
%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\Advika3_0\
                                                        └── advika_3_0_generator.py
```

### Step 2.2: Verify File Location

1. Open File Explorer
2. Navigate to: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\`
3. Create folder `Advika3_0` if not exists
4. Copy `advika_3_0_generator.py` into that folder
5. Verify file is there

---

## 3. How to Run the Script

### Step 3.1: Open Fusion 360

1. Launch Fusion 360
2. Create a **NEW DESIGN** (File → New Design)
3. Name it: `Advika 3.0 Robot`
4. Set units to **mm** (Solid → Units → mm)

### Step 3.2: Open Scripts Panel

**Method A: Keyboard Shortcut**
- Press `Shift + S`

**Method B: Menu**
- Click `Solid` workspace
- Go to `CREATE` tab
- Click `Scripts` dropdown → `Scripts`

### Step 3.3: Run the Script

1. In Scripts panel, find `Advika3_0` folder
2. Click to expand
3. Select `advika_3_0_generator`
4. Click **"Run"** button

### Step 3.4: Watch Progress

The Output window will show:
```
============================================================
Starting Advika 3.0 Robot Model Generation
============================================================

--- Creating Chassis Base ---
Chassis Base created: 300x240x5 mm with 4 mounting holes

--- Creating Motor Mounts ---
Motor Mount Left created at (-90, 70)
Motor Mount Right created at (90, -70)

--- Creating Wheel Hubs ---
Wheel Hub Left created: 65mm diameter, 20mm thick
Wheel Hub Right created: 65mm diameter, 20mm thick

--- Creating LiDAR Tower ---
LiDAR Tower created: 70mm base, 150mm height, hollow

--- Creating Top Dome ---
Top Dome created: 115mm radius, 80mm height

--- Creating Camera Mounts ---
Horizon Camera Mount created: 25x24mm, 15deg tilt
Floor Camera Mount created: 25x24mm, -45deg tilt

--- Creating IMU Mount ---
IMU Mount created: 20x20x5mm with 3mm center hole

--- Creating Battery Tray ---
Battery Tray created: 80x70x25mm, hollow with cutouts

--- Creating Bumpers ---
Front Bumper created: 280x30x20mm, rounded, hollow
Rear Bumper created: 280x30x20mm, rounded, hollow

--- Creating ESP32 Enclosure ---
ESP32 Enclosure created: 55x30x15mm, hollow with cutouts

============================================================
Advika 3.0 Robot Model Generation Complete!
============================================================

VERIFICATION STEPS:
1. Check Browser tree for all component names
2. Verify dimensions in Properties panel (right-click → Properties)
3. Export STL: File → Export → select STL → High quality
4. See README for detailed verification checklist
```

---

## 4. Verification After Each Step

### Verification 4.1: Check Browser Tree (Left Sidebar)

Press `F` to toggle Browser visibility if not visible.

**Expected Components:**
```
□ Advika 3.0 Robot
├── ◢ Chassis Base
├── ◢ Motor Mount Left
├── ◢ Motor Mount Right
├── ◢ Wheel Hub Left
├── ◢ Wheel Hub Right
├── ◢ LiDAR Tower
├── ◢ Top Dome
├── ◢ Horizon Camera Mount
├── ◢ Floor Camera Mount
├── ◢ IMU Mount
├── ◢ Battery Tray
├── ◢ Front Bumper
├── ◢ Rear Bumper
└── ◢ ESP32 Enclosure
```

**How to Check:**
1. Look at Browser tree on left side
2. Count components
3. All 14 should be present

### Verification 4.2: Check Individual Dimensions

**For each component:**

1. **Right-click** component in Browser
2. Select **"Properties"**
3. Check dimensions in dialog

**Dimension Reference Table:**

| Component | Expected Dimensions | What to Check |
|-----------|-------------------|---------------|
| Chassis Base | 300 × 240 × 5 mm | Length, Width, Height |
| Motor Mounts | 6mm shaft hole | Diameter of center hole |
| Wheel Hubs | Ø65 × 20 mm | Diameter, Extrusion depth |
| LiDAR Tower | Ø70 base, 150mm height | Base diameter, Height |
| Top Dome | Ø230 × 80mm (revolved) | Radius, Height |
| Camera Mounts | 25 × 24 × 8 mm | Box dimensions |
| IMU Mount | 20 × 20 × 5 mm | Square, Height |
| Battery Tray | 80 × 70 × 25 mm | Box dimensions |
| Bumpers | 280 × 30 × 20 mm | Box dimensions |
| ESP32 Enclosure | 55 × 30 × 15 mm | Box dimensions |

### Verification 4.3: Check in 3D Viewport

**Rotate view:** Click and drag with mouse
**Pan view:** Shift + Click and drag
**Zoom:** Scroll wheel

**Visual Checks:**
- [ ] Chassis is a flat rectangle at bottom
- [ ] Motor mounts are at corners
- [ ] Wheel hubs are circular
- [ ] LiDAR Tower is a tapered cylinder
- [ ] Top Dome is a half-sphere
- [ ] Camera mounts are tilted rectangles
- [ ] Bumpers are rounded rectangles at front/back
- [ ] No overlapping geometry

### Verification 4.4: Check Timeline (Bottom)

The Timeline shows all operations performed.

**Expected Timeline Operations:**
- Sketch (multiple)
- Extrude (multiple)
- Fillet (on Chassis Base)
- Shell (on hollow components)

---

## 5. How to Export STL Files

### Step 5.1: Export Each Component

Fusion 360 exports one STL at a time.

**For EACH component (1-14):**

1. **In Browser**, click to select component
2. **Right-click** → **Export**
3. Or: **File → Export**
4. In Export dialog:
   - **Format:** STL (Binary or ASCII)
   - **Quality:** High (default is fine)
   - **Resolution:** 0.001 mm (fine)
5. **Save** with correct filename

### Step 5.2: STL Filenames Reference

Use these exact filenames:

| # | Component | STL Filename |
|---|-----------|--------------|
| 1 | Chassis Base | `advika_chassis.stl` |
| 2 | Motor Mount Left | `advika_motor_mount_L.stl` |
| 3 | Motor Mount Right | `advika_motor_mount_R.stl` |
| 4 | Wheel Hub Left | `advika_wheel_hub_L.stl` |
| 5 | Wheel Hub Right | `advika_wheel_hub_R.stl` |
| 6 | LiDAR Tower | `advika_lidar_tower.stl` |
| 7 | Top Dome | `advika_top_dome.stl` |
| 8 | Horizon Camera Mount | `advika_camera_horizon.stl` |
| 9 | Floor Camera Mount | `advika_camera_floor.stl` |
| 10 | IMU Mount | `advika_imu_mount.stl` |
| 11 | Battery Tray | `advika_battery_tray.stl` |
| 12 | Front Bumper | `advika_bumper_front.stl` |
| 13 | Rear Bumper | `advika_bumper_rear.stl` |
| 14 | ESP32 Enclosure | `advika_esp32_enclosure.stl` |

### Step 5.3: Verify STL Export

**In your slicer software (Cura, PrusaSlicer, etc.):**
1. Open each STL file
2. Check for errors:
   - **Red warning** = non-watertight mesh (needs fix)
   - **Orange warning** = inverted normals
   - **Green** = ready to print

**Mesh Repair if needed:**
- Use Meshmixer
- Use Netfabb
- Or Fusion 360's built-in repair

---

## 6. Troubleshooting

### Problem: Script not visible in Scripts panel

**Solution:**
1. Close Fusion 360 completely
2. Check file location:
   ```
   %APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\Advika3_0\advika_3_0_generator.py
   ```
3. Restart Fusion 360

### Problem: "No active design" error

**Solution:**
1. Create new design first: File → New Design
2. Then run script

### Problem: Script runs but no geometry created

**Solution:**
1. Check Output window for errors
2. Press `Shift + Alt + O` to show Output
3. Report errors

### Problem: Geometry looks wrong

**Solution:**
1. Undo: `Ctrl + Z`
2. Modify script values
3. Run again

### Problem: Shell feature fails

**Solution:**
Shell requires a thick enough wall. The script uses:
- LiDAR Tower: 2mm shell
- Battery Tray: 2mm shell
- Bumpers: 2mm shell
- ESP32: 1.5mm shell

If shell fails, the wall is too thin for the geometry.

---

## 7. Component Specifications

### 7.1 Chassis Base
```
Dimensions: 300 × 240 × 5 mm
Material: Dark Blue (RGB: 43, 91, 132)
Features:
  - 5mm corner fillets
  - 4× mounting holes (Ø3mm) at 15mm from corners
  - Position: Origin (0, 0, 0)
```

### 7.2 Motor Mounts
```
Dimensions: Through chassis
Shaft Hole: Ø6mm
Mounting Holes: 4× Ø3mm at 15mm radius
Left Position: (-90, 70, -10)
Right Position: (90, -70, -10)
Material: Silver (RGB: 192, 192, 192)
```

### 7.3 Wheel Hubs
```
Dimensions: Ø65mm × 20mm thick
Shaft Hole: Ø6mm with 5.5mm flat (D-shaft)
Mounting: 4× Ø3mm at 25mm radius (45° intervals)
Left Position: (-90, 70, -15)
Right Position: (90, -70, -15)
Material: Black (RGB: 26, 26, 26)
```

### 7.4 LiDAR Tower
```
Base Diameter: Ø70mm
Height: 150mm
Draft: 2° taper
Wall Thickness: 2mm (hollow)
Top Platform: Ø80mm × 5mm thick
Mounting Holes: 4× Ø3mm at 25mm radius
Position: (0, 0, 75)
Material: White (RGB: 240, 240, 240)
```

### 7.5 Top Dome
```
Radius: 115mm
Height: 80mm
Type: Revolved half-sphere
Position: (0, 0, 155)
Material: Translucent White (60% opacity)
```

### 7.6 Camera Mounts
```
Dimensions: 25 × 24 × 8 mm
Screw Holes: 2× Ø2.5mm
Horizon Camera:
  - Position: (140, 0, 75)
  - Tilt: 15° upward
Floor Camera:
  - Position: (120, 0, 25)
  - Tilt: 45° downward
Material: Silver (RGB: 192, 192, 192)
```

### 7.7 IMU Mount
```
Dimensions: 20 × 20 × 5 mm
Locating Hole: Ø3mm center
Position: (0, 0, 5)
Material: Gold (RGB: 255, 215, 0)
```

### 7.8 Battery Tray
```
Dimensions: 80 × 70 × 25 mm
Wall Thickness: 2mm (hollow)
XT60 Cutout: 15 × 10 mm (front)
JST-XH Cutout: 8 × 4 mm (side)
Position: (0, -20, -5)
Material: Orange (RGB: 255, 140, 0)
```

### 7.9 Bumpers
```
Dimensions: 280 × 30 × 20 mm
Corner Radius: 10mm
Wall Thickness: 2mm (hollow)
Microswitch Holes: 2× Ø3mm at ±100mm
Front Position: (150, 0, 5)
Rear Position: (-150, 0, 5)
Material: Red (RGB: 230, 57, 70)
```

### 7.10 ESP32 Enclosure
```
Dimensions: 55 × 30 × 15 mm
Wall Thickness: 1.5mm (hollow)
USB-C Cutout: 10 × 5 mm (front)
Ventilation: 4× slots on top
Position: (0, 20, 5)
Material: Blue (RGB: 0, 0, 128)
```

---

## Assembly Positions Summary

| Component | X | Y | Z |
|-----------|---|---|---|
| Chassis Base | 0 | 0 | 0 |
| Motor Mount Left | -90 | 70 | -10 |
| Motor Mount Right | 90 | -70 | -10 |
| Wheel Hub Left | -90 | 70 | -15 |
| Wheel Hub Right | 90 | -70 | -15 |
| LiDAR Tower | 0 | 0 | 75 |
| Top Dome | 0 | 0 | 155 |
| Horizon Camera | 140 | 0 | 75 |
| Floor Camera | 120 | 0 | 25 |
| IMU Mount | 0 | 0 | 5 |
| Battery Tray | 0 | -20 | -5 |
| Front Bumper | 150 | 0 | 5 |
| Rear Bumper | -150 | 0 | 5 |
| ESP32 Enclosure | 0 | 20 | 5 |

---

## Next Steps After Generation

1. **3D Print** each component
2. **Post-process** prints (remove supports, sand, etc.)
3. **Assemble** hardware:
   - Motors to mounts
   - Wheels to hubs
   - LiDAR to tower
   - Cameras to mounts
   - ESP32 to enclosure
   - Battery to tray
   - All to chassis

4. **Wire** electronics
5. **Flash** firmware
6. **Test** movement

---

**Document Version:** 1.0
**Last Updated:** 2026-07-26
**Author:** Claude (for Advika 3.0 Project)