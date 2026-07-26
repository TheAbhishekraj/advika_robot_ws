# ADVIKA 3.0 CAD DESIGN GUIDE

**Purpose:** Central hub for all 3D design, printing, and mesh integration
**Platform:** Fusion 360 (Windows/Mac), Blender for mesh processing
**Last Updated:** 2026-07-25

---

## 📁 REPOSITORY CAD STRUCTURE

```
advika_robot_ws/
├── src/advika_cad/           # ROS2 CAD package
│   ├── meshes/               # STL files for 3D printing
│   │   ├── Chassis_Base_v3.stl
│   │   └── ...
│   ├── step/                # STEP files for mechanical
│   │   └── Chassis_Assembly_v3.step
│   ├── fusion360/           # Fusion 360 project files
│   │   └── Advika_3.0.f3d
│   └── advika_cad/          # Python package (if any)
│
├── simulation/urdf/
│   ├── advika.urdf          # Robot URDF (uses meshes)
│   └── meshes/
│       └── base_link.stl    # Single legacy mesh
│
├── docs/
│   ├── FUSION360_WORKFLOW.md      # Complete design workflow
│   ├── MESH_EXPORT_GUIDE.md       # STL→DAE→URDF pipeline
│   ├── 3BHK_FURNITURE_SPEC.md     # Furniture design specs
│   ├── BOM.md                     # Bill of Materials + costs
│   ├── CAD_README.md              # Original chassis notes
│   ├── MENTORSHIP_GUIDE.md        # 9-week learning path
│   └── SIMULATION_FIRST_CHECKLIST.md  # Phase 1 checklist
```

---

## 🎯 DESIGN PRIORITIES

### High Priority (Do First)

| # | Component | Why | STL Required |
|---|-----------|-----|--------------|
| 1 | Chassis Base | Foundation of entire robot | Yes |
| 2 | Wheel Hubs (×2) | Drive system interface | Yes |
| 3 | LiDAR Tower | Sensor mounting, height | Yes |
| 4 | Top Dome | Protection + aesthetics | Yes |
| 5 | Motor Mounts | Motor attachment | Yes |

### Medium Priority

| # | Component | Why | STL Required |
|---|-----------|-----|--------------|
| 6 | Battery Tray | Power system | Yes |
| 7 | Camera Bracket | Dual camera mount | Yes |
| 8 | ToF Holder | Depth sensor mount | Yes |
| 9 | Bumpers (×2) | Collision protection (TPU) | Yes |
| 10 | ESP32 Enclosure | Electronics protection | Yes |

### Lower Priority

| # | Component | Why | STL Required |
|---|-----------|-----|--------------|
| 11 | IMU Mount | Small, simple | Yes |
| 12 | Display Bezel | Aesthetic + protection | Yes |
| 13 | Cable Clips | Cable management | Optional |

---

## 📐 COMPONENT SPECIFICATIONS

### Chassis Base v3
```
Dimensions: 300mm × 240mm × 5mm
Features:
  - Motor mount holes (4× M3 per side)
  - Raspberry Pi 5 mounting (4× M2.5)
  - ESP32 mounting (4× M2)
  - Cable routing channels (6mm wide)
  - Battery tray slot (140mm × 80mm)
Material: PETG
Print Time: ~2.5 hours
Infill: 40%
Perimeters: 4
```

### Wheel Hub
```
Dimensions:
  - Outer diameter: 65mm
  - Bore: 6mm (D-shaft)
  - Height: 12mm
  - 4× M3 holes on 50mm PCD
Material: PETG
Print Time: ~45 minutes each
Infill: 50%
Perimeters: 4
```

### LiDAR Tower
```
Dimensions:
  - Base diameter: 70mm
  - Top diameter: 60mm (tapered)
  - Height: 150mm
  - Internal cable channel: 4mm × 4mm
Material: PETG
Print Time: ~1.5 hours
Infill: 30%
Perimeters: 3
```

### Top Dome
```
Dimensions:
  - Diameter: 230mm
  - Height: 80mm
  - Wall thickness: 2mm
  - SSD1306 cutout: 60mm × 30mm
Material: PETG (translucent)
Print Time: ~2 hours
Infill: 20%
Perimeters: 2
Note: Print with 50% fan, slow cooling
```

---

## 🔄 DESIGN → PRINT → INTEGRATION WORKFLOW

```
┌──────────────────────────────────────────────────────────────────┐
│  1. DESIGN IN FUSION 360                                          │
│     └─ Create component sketch and 3D model                       │
│     └─ Export as STL (millimeters, high quality)                  │
│     ↓                                                              │
│  2. VERIFY IN SLICER                                              │
│     └─ Import into Cura/PrusaSlicer                               │
│     └─ Check dimensions with caliper measurement                  │
│     └─ Add supports if needed                                     │
│     ↓                                                              │
│  3. PRINT IN PETG                                                 │
│     └─ Nozzle: 250°C, Bed: 80°C                                   │
│     └─ Layer: 0.2mm, Infill: 30-50%                               │
│     ↓                                                              │
│  4. TEST FIT                                                      │
│     └─ Verify hole diameters (tap threads)                        │
│     └─ Check alignment with other parts                           │
│     ↓                                                              │
│  5. UPDATE URDF                                                   │
│     └─ Replace primitive with mesh reference                      │
│     └─ Rebuild: colcon build --packages-select advika_cad        │
│     ↓                                                              │
│  6. VALIDATE IN GAZEBO                                            │
│     └─ Launch simulation                                          │
│     └─ Verify mesh renders correctly                               │
│     └─ Check collision geometry                                    │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📋 COMPONENT DESIGN CHECKLIST

For each component, verify:

- [ ] Dimensions match specification (check twice!)
- [ ] Mounting holes correct diameter (M3 = 3mm, tap to 2.5mm)
- [ ] Fits with adjacent components
- [ ] Cable routing paths clear
- [ ] STL exported at correct scale (mm)
- [ ] STEP exported for mechanical review
- [ ] Print settings optimized (PETG/TPU)
- [ ] First print is draft quality to verify
- [ ] Final print dimensions verified with calipers
- [ ] URDF updated with mesh reference
- [ ] Gazebo renders mesh correctly

---

## 🔧 PRINT SETTINGS REFERENCE

### PETG (All structural parts)
```yaml
Nozzle Temperature: 250°C
Bed Temperature: 80°C
Layer Height: 0.2mm
Perimeters: 3-4
Infill: 30-50% (structural), 20% (covers)
Supports: Tree supports for >60° overhangs
Cooling: 50% fan
Travel Speed: 150mm/s
```

### TPU 95A (Bumpers only)
```yaml
Nozzle Temperature: 235°C
Bed Temperature: 60°C
Layer Height: 0.24mm
Perimeters: 3
Infill: 20%
Supports: Tree supports
Cooling: 30% fan
Print Speed: Slow (30-40mm/s)
```

### Draft Mode (First Prints)
```yaml
Layer Height: 0.3mm
Infill: 10%
Perimeters: 2
Supports: None (if possible)
Speed: Fast
Purpose: Verify dimensions only
```

---

## 📦 STL FILE NAMING

```
Format: {Component}_{Version}_{Date}.stl

Examples:
├── Chassis_Base_v3_20260725.stl
├── Wheel_Hub_Left_v1_20260801.stl
├── Wheel_Hub_Right_v1_20260801.stl
├── LiDAR_Tower_v2_20260805.stl
├── Top_Dome_v1_20260810.stl
├── Motor_Mount_Left_v1_20260803.stl
├── Motor_Mount_Right_v1_20260803.stl
├── Battery_Tray_v1_20260807.stl
├── Camera_Bracket_v1_20260808.stl
├── ToF_Holder_v1_20260809.stl
├── Front_Bumper_v1_20260812.stl
└── Rear_Bumper_v1_20260812.stl
```

---

## 🔗 URDF INTEGRATION TEMPLATE

```xml
<!-- Replace this (primitive): -->
<link name="component_link">
  <visual>
    <geometry>
      <box size="0.30 0.24 0.15"/>
    </geometry>
  </visual>
</link>

<!-- With this (mesh): -->
<link name="component_link">
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://advika_cad/meshes/Component_Name.stl"/>
    </geometry>
    <material name="blue"/>
  </visual>
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://advika_cad/meshes/Component_Name.stl"/>
    </geometry>
  </collision>
</link>
```

After editing URDF:
```bash
colcon build --packages-select advika_cad
source install/setup.bash
ros2 launch advika_sim sim_bringup.launch.py
```

---

## 📁 FILE STORAGE STRATEGY

### Git Repository (Small files)
- URDF files (.urdf, .xacro)
- World files (.world)
- Launch files (.launch.py)
- Documentation (.md)

### GitHub Releases (Large files)
- STL meshes (>100KB each)
- STEP assemblies
- Fusion 360 project files (.f3d)

### Local Storage (Working files)
- Fusion 360 active projects
- Slicer profiles
- Print logs

---

## 📚 REFERENCE DOCUMENTS

| Document | What It Contains |
|----------|------------------|
| [FUSION360_WORKFLOW.md](FUSION360_WORKFLOW.md) | Complete Fusion 360 tutorial |
| [MESH_EXPORT_GUIDE.md](MESH_EXPORT_GUIDE.md) | STL→DAE→URDF pipeline |
| [3BHK_FURNITURE_SPEC.md](3BHK_FURNITURE_SPEC.md) | Furniture dimensions for Gazebo |
| [BOM.md](BOM.md) | Hardware costs and supplier links |
| [MENTORSHIP_GUIDE.md](MENTORSHIP_GUIDE.md) | 9-week learning path |
| [SIMULATION_FIRST_CHECKLIST.md](SIMULATION_FIRST_CHECKLIST.md) | Phase 1 validation checklist |

---

## ⚠️ COMMON MISTAKES TO AVOID

1. **Wrong units** - Always export in millimeters, not inches
2. **Forgetting collision** - Update BOTH visual AND collision in URDF
3. **Skip draft mode** - Always print draft quality first
4. **No caliper check** - Measure printed parts, don't trust slicer estimates
5. **Hot bed too cold** - PETG needs 80°C bed, not 60°C
6. **Fast TPU** - TPU 95A needs slow print speed (30mm/s)
7. **Missing supports** - Check slicer preview for overhangs

---

## 🆘 TROUBLESHOOTING

| Problem | Cause | Solution |
|---------|-------|----------|
| Mesh not in Gazebo | Wrong path | Use `package://advika_cad/meshes/` |
| Warped prints | Bed too cold | Increase to 80°C, use glue stick |
| Holes too small | Slicer compensation | Design 0.2mm larger for M3 tap |
| Stringing | Retraction settings | Increase retraction, reduce temp |
| Layer separation | Under-extrusion | Check e-steps calibration |

---

## ✅ CAD COMPLETION CHECKLIST

Before moving to hardware phase:

- [ ] All 9 high/medium priority components designed
- [ ] All STLs printed and dimension-verified
- [ ] All STEP files exported for mechanical review
- [ ] URDF updated with all mesh references
- [ ] Gazebo renders all meshes correctly
- [ ] Collision geometry matches visual
- [ ] BOM completed with final costs
- [ ] Hardware ordered (or budget confirmed)

---

*Design first. Print second. Build third.*
---

## 🎓 LEARNING: FUSION 360 SIMULATION (THERMAL & STRESS)

This section provides a complete step-by-step guide to run Thermal and Static Stress simulations on Advika 3.0 in Fusion 360.

### ⚠️ MANDATORY FIRST — Open Simulation Workspace

1. Click the workspace switcher (top-left corner of Fusion, it currently shows "Design")
2. Click: **Simulate**
3. A "New Study" panel opens on the left side

---

### 🌡️ THERMAL SIMULATION — Steps

**Step 1 — Create Thermal Study**
- In "New Study" panel: Click **Thermal**
- Name it: Advika30_Thermal
- Click: **OK**

**Step 2 — Assign PCB Material**
- In Study panel (left side): Click **Materials**
- Select body: Advika30_PCB_Board (the green flat board in the model)
- Search for: Glass Fiber
- Select: Glass Fiber Epoxy (closest to FR-4)
- Click: **OK**

**Step 3 — Add Heat Loads**
- Click: **Loads → Internal Heat Load**
- **Load 1 — ESP32-S3:** Select body dvika_esp32_enclosure, Value  .5 W, Click OK
- **Load 2 — DRV8833 Motor Driver:** Select body Advika30_PCB_Board (top face, right area), Value 1.0 W, Click OK
- **Load 3 — Ambient Temperature:** Click **Loads → Temperature**, Select ALL outer faces of Advika30_PCB_Board, Value 25°C, Click OK

**Step 4 — Add Convection**
- Click: **Loads → Convection**
- Select: all exposed top faces of Advika30_PCB_Board
- Set: Convection coefficient = 10 W/m²K, Ambient temperature = 25°C
- Click: **OK**

**Step 5 — Pre-check & Solve**
- Click: **Manage → Pre-Check** (Must show: ✅ No errors)
- Then Click: **Solve → Solve Current** (Wait: 5–15 minutes for cloud solve)

**Step 6 — Read Results**
- Results panel → **Temperature**
- Target: Max temp < 70°C everywhere (DRV8833 area < 85°C, ESP32 area < 80°C)

---

### ⚙️ STATIC STRESS SIMULATION — Steps

**Step 1 — Create New Study**
- Click: **Simulate → New Study**
- Click: **Static Stress**
- Name it: Advika30_Chassis_Stress
- Click: **OK**

**Step 2 — Assign PLA Material**
- Click: **Materials**
- Select body: dvika_chassis
- Search: PLA or Acrylonitrile Butadiene Styrene (ABS is closest to PLA in Fusion library)
- If not found, Create Custom: Young's Modulus 3500 MPa, Yield Strength 50 MPa, Density 1240 kg/m³, Poisson's Ratio  .36
- Apply same material to: dvika_motor_mount_L, dvika_motor_mount_R, dvika_wheel_hub_L, dvika_wheel_hub_R
- Click: **OK**

**Step 3 — Apply Fixed Constraints**
- Click: **Constraints → Fixed**
- **Selection 1:** Select the BOTTOM FLAT FACE of dvika_motor_mount_L (the face that bolts to the chassis floor), Click OK
- **Selection 2:** Select the BOTTOM FLAT FACE of dvika_motor_mount_R, Click OK

**Step 4 — Apply Robot Weight Load**
- Click: **Loads → Force**
- **Load 1 — Total robot weight:** Select TOP FLAT FACE of dvika_chassis (200×150mm top surface), Direction -Z (downward), Magnitude 24.5 N (= 2.5 kg × 9.81), Click OK
- **Load 2 — Battery weight:** Select TOP FACE of dvika_battery_tray, Direction -Z, Magnitude 5.9 N (= 0.6 kg × 9.81), Click OK

**Step 5 — Pre-check & Solve**
- Click: **Manage → Pre-Check** (Must show: ✅ No errors)
- Then Click: **Solve → Solve Current** (Wait: 5–20 minutes)

**Step 6 — Read Results**
- Results panel → **Safety Factor** (opens automatically)
- Target: Safety Factor > 2.0 (Blue = Pass), Von Mises Stress < 25 MPa, Displacement < 2mm
- Colour Guide: 🔵 Blue = Safe (SF > 6), 🟢 Green = Good (SF 4-6), 🟡 Yellow = Marginal (SF 2-4), 🔴 Red = Danger (SF < 2)

### 📊 EXPECTED RESULTS SUMMARY

| Simulation | Expected Result | If Failed |
|-----------|----------------|-----------|
| **Thermal** | Max 60–65°C on PCB | Add venting holes to esp32 enclosure |
| **Thermal** | DRV8833 < 85°C | Add thermal vias in BRD file |
| **Stress** | Safety Factor > 2.0 | Increase motor mount infill to 60% |
| **Stress** | Displacement < 2mm | Add internal ribs to chassis |
| **Stress** | Von Mises < 25 MPa | Switch PLA → PETG material |
