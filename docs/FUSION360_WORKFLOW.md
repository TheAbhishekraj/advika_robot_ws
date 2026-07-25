# FUSION 360 WORKFLOW GUIDE FOR ADVIKA 3.0

**Platform:** Windows (Fusion 360 Web Version / Desktop)
**Date:** 2026-07-25
**Purpose:** Design and export 3D-printable components for Advika AMR

---

## 1. GETTING STARTED

### 1.1 Fusion 360 Installation

1. Download Fusion 360 from [autodesk.com/fusion-360](https://www.autodesk.com/products/fusion-360/)
2. Install on Windows 10/11 (64-bit)
3. Create Autodesk account (free for personal/hobby use)
4. Activate 3-year personal license (free for makers)

### 1.2 Workspace Setup

```
Fusion 360 → Preferences → General
├── Units: mm (millimeters)
├── Snap: Enable for accurate modeling
└── Graphics: Set to "Performance" mode
```

### 1.3 New Project Structure

```
Fusion 360 → Data Panel → Create Project
└── Name: "Advika_3.0_CAD"

Project Structure:
├── Robot Chassis/
│   ├── Chassis_Base
│   ├── Chassis_Lid
│   ├── Motor_Mounts
│   └── Cable_Channels
├── Sensor_Mounts/
│   ├── LiDAR_Tower
│   ├── Camera_Bracket
│   └── ToF_Holder
├── Enclosures/
│   ├── Top_Dome
│   ├── ESP32_Enclosure
│   └── Battery_Tray
├── Wheels/
│   ├── Wheel_Hub_Left
│   └── Wheel_Hub_Right
└── Bumpers/
    ├── Front_Bumper
    └── Rear_Bumper
```

---

## 2. COMPONENT DESIGN ORDER

Design components in this order (dependencies noted):

### 2.1 Phase 1: Foundation (Do First)

#### Chassis Base (PETG)
```
Dimensions: 300mm × 240mm × 5mm
Features:
  - Motor mount holes (4× M3 press-fit)
  - Raspberry Pi 5 mounting holes (4× M2.5)
  - ESP32 mounting holes (4× M2)
  - Cable routing channels (6mm wide)
  - Battery tray slot (140mm × 80mm)
  - Wall thickness: 5mm
```

**Design Steps:**
1. Create new sketch on XY plane
2. Draw 300×240mm rectangle
3. Add all mounting hole positions
4. Add cable channel cutouts
5. Extrude 5mm
6. Add chamfer to edges (0.5mm)

#### Wheel Hubs (PETG) ×2
```
Dimensions:
  - Outer diameter: 65mm (for wheel)
  - Bore diameter: 6mm (D-shaft)
  - Hub height: 12mm
  - 4× M3 screw holes (for wheel attachment)
```

**Design Steps:**
1. Create new sketch on XZ plane
2. Draw 65mm circle
3. Draw 6mm center bore
4. Add 4× M3 holes on 50mm PCD
5. Extrude 12mm
6. Add decorative grooves

### 2.2 Phase 2: Sensor Infrastructure

#### LiDAR Tower (PETG)
```
Dimensions:
  - Height: 150mm from ground
  - Base diameter: 70mm
  - Top diameter: 60mm (taper)
  - Cable channel: 4mm × 4mm internal
  - Wall thickness: 3mm
```

**Design Steps:**
1. Create new sketch
2. Draw 70mm circle (base)
3. Draw 60mm circle (top, offset 150mm)
4. Use LOFT command to create taper
5. Cut cable channel through center
6. Add base flange for mounting

#### Camera Bracket (PETG)
```
Dimensions:
  - Main plate: 80mm × 40mm × 3mm
  - Horizon camera mount: 20mm × 20mm × 15mm
  - Floor camera mount: 20mm × 20mm × 10mm (angled)
  - Camera tilt: 30° for floor view
```

### 2.3 Phase 3: Top-Level Components

#### Top Dome (PETG, translucent)
```
Dimensions:
  - Diameter: 230mm
  - Height: 80mm
  - Wall thickness: 2mm
  - Dome profile: Hemisphere

Features:
  - SSD1306 display cutout (60mm × 30mm)
  - Cable passthrough (2× 10mm holes)
  - Camera cable routing channels
```

**Design Steps:**
1. Create new sketch
2. Draw 230mm circle
3. Use REVOVE command to create dome profile
4. Import SSD1306 bezel outline as sketch
5. Cut display window
6. Add mounting tabs (6× evenly spaced)

#### Battery Tray (PETG)
```
Dimensions:
  - Length: 140mm
  - Width: 80mm
  - Depth: 25mm
  - Wall thickness: 3mm

Features:
  - 3S2P 18650 battery holder (8 cells)
  - XT60 connector access slot
  - JST-XH balance connector slot
  - Strap retention slots
```

### 2.4 Phase 4: Wheels & Bumpers

#### Wheel Design (TPU 95A - not printed, purchased)
```
Note: Wheels typically purchased pre-made. Design hubs only.
JGA25-370 wheel compatibility:
  - Wheel bore: 6mm
  - Hub interface: 4× M3 on 50mm PCD
```

#### Bumpers (TPU 95A)
```
Dimensions:
  - Width: 280mm
  - Height: 40mm
  - Depth: 20mm
  - Microswitch recess: 10mm × 6mm × 5mm

Features:
  - Floating mount design (3mm gap)
  - 2× Microswitch mounts per bumper
  - Flexible TPU 95A for collision absorption
```

---

## 3. EXPORT SETTINGS

### 3.1 STL Export (for 3D Printing)

```
File → Export
├── Format: STL
├── Units: Millimeters
├── Resolution: High (0.01mm mesh deviation)
└── Output: Binary STL (smaller file size)

Recommended Mesh Settings:
├── Surface Deviation: 0.01 mm
├── Normal Deviation: 0.05 deg
└── Maximum Aspect Ratio: 100:1
```

### 3.2 STEP Export (for Mechanical Integration)

```
File → Export
├── Format: STEP
├── Units: Millimeters
├── Scheme: AP214
└── Include: All components

Assembly STEP:
├── File → Export
├── Format: STEP
├── Include: As single compound
└── For: Mechanical drawings, vendor quotes
```

### 3.3 Fusion 360 Print Settings

```
For PETG (recommended):
├── Layer Height: 0.2mm
├── Infill: 30-50% (structural), 20% (covers)
├── Perimeters: 3-4
├── Supports: Required for overhangs >60°
├── Nozzle Temp: 250°C
├── Bed Temp: 80°C
└── Cooling: 50%

For TPU 95A (bumpers):
├── Layer Height: 0.24mm
├── Infill: 20%
├── Perimeters: 3
├── Supports: Tree supports
├── Nozzle Temp: 235°C
├── Bed Temp: 60°C
└── Cooling: 30%
```

---

## 4. ASSEMBLY WORKFLOW

### 4.1 Sub-Assembly Groups

```
1. Drivetrain Sub-Assembly
   ├── Chassis Base
   ├── Left Wheel Hub
   ├── Right Wheel Hub
   ├── Motor Mounts
   └── Caster Wheels

2. Sensor Sub-Assembly
   ├── LiDAR Tower
   ├── LiDAR mount
   ├── Camera Bracket
   ├── ToF Holder
   └── IMU Mount

3. Electronics Sub-Assembly
   ├── Top Dome
   ├── ESP32 Enclosure
   ├── Battery Tray
   ├── Display Bezel
   └── Cable Management
```

### 4.2 Full Assembly Order

```
Step 1: Print all parts
Step 2: Press-fit M3 brass threaded inserts (all holes)
Step 3: Mount motors to chassis (M3 × 8mm screws)
Step 4: Attach caster wheels (M3 × 12mm screws)
Step 5: Install Raspberry Pi 5 (M2.5 standoffs)
Step 6: Mount ESP32 board (M2 screws)
Step 7: Route cables through channels
Step 8: Install LiDAR tower (M3 × 10mm screws)
Step 9: Attach camera bracket (M3 × 8mm screws)
Step 10: Install battery tray (clip-in design)
Step 11: Attach bumpers (M3 × 16mm screws, floating)
Step 12: Install top dome (M3 × 8mm screws)
Step 13: Connect all cables
Step 14: Perform smoke test
```

---

## 5. QUALITY CHECKLIST

### 5.1 Design Verification

- [ ] All dimensions match URDF (check scale)
- [ ] Motor mount holes align with JGA25-370
- [ ] Raspberry Pi 5 mounting holes correct
- [ ] LiDAR tower fits LD06/X4 sensor
- [ ] Camera bracket clearances adequate
- [ ] Battery tray fits 3S2P configuration
- [ ] Display cutout matches SSD1306

### 5.2 Print Verification

- [ ] Test print smallest part first
- [ ] Verify hole diameters (M3 = 3mm, M2.5 = 2.5mm)
- [ ] Check for warping on large flat parts
- [ ] Verify supports remove cleanly
- [ ] Test press-fit insert installation

### 5.3 Assembly Verification

- [ ] All screws thread smoothly
- [ ] Cables route without pinching
- [ ] LiDAR has clear 360° view
- [ ] Cameras have correct field of view
- [ ] Battery removable without tools
- [ ] E-Stop accessible from exterior

---

## 6. FILE NAMING CONVENTION

```
Format: {Component}_{Version}_{Date}.{ext}

Examples:
├── Chassis_Base_v3_20260725.stl
├── Wheel_Hub_Left_v1_20260725.stl
├── LiDAR_Tower_v2_20260725.step
├── Top_Dome_v1_20260725.stl
└── Assembly_Advika_3D_v1_20260725.step
```

---

## 7. INTEGRATION WITH SIMULATION

### 7.1 Update URDF with Mesh References

After exporting STL files, update the URDF:

```xml
<link name="base_link">
  <visual>
    <origin xyz="0 0 0.075" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://advika_cad/meshes/Chassis_Base_v3.stl"/>
    </geometry>
    <material name="blue"/>
  </visual>
</link>
```

### 7.2 Mesh Directory Structure

```
src/advika_cad/
├── meshes/
│   ├── Chassis_Base_v3.stl
│   ├── Wheel_Hub_Left_v1.stl
│   ├── Wheel_Hub_Right_v1.stl
│   ├── LiDAR_Tower_v2.stl
│   ├── Top_Dome_v1.stl
│   ├── Motor_Mount_v1.stl
│   ├── Battery_Tray_v1.stl
│   ├── Camera_Bracket_v1.stl
│   ├── ToF_Holder_v1.stl
│   ├── Front_Bumper_v1.stl
│   └── Rear_Bumper_v1.stl
└── step/
    ├── Chassis_Assembly_v3.step
    ├── Sensor_Module_v2.step
    └── Full_Robot_Assembly_v1.step
```

---

## 8. QUICK REFERENCE

| Component | Material | Priority | Print Time (est.) |
|-----------|----------|----------|-------------------|
| Chassis Base | PETG | HIGH | 2.5 hours |
| Wheel Hubs | PETG | HIGH | 45 min each |
| LiDAR Tower | PETG | HIGH | 1.5 hours |
| Top Dome | PETG | HIGH | 2 hours |
| Motor Mounts | PETG | MEDIUM | 30 min each |
| Battery Tray | PETG | MEDIUM | 1 hour |
| Camera Bracket | PETG | MEDIUM | 45 min |
| ToF Holder | PETG | MEDIUM | 20 min |
| Bumpers | TPU 95A | MEDIUM | 1 hour each |
| ESP32 Enclosure | PETG | LOW | 30 min |

---

*End of Fusion 360 Workflow Guide*