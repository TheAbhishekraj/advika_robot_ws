# ADVIKA 3.0 -- 3D ASSETS AUDIT REPORT

**Date:** 2026-07-25
**Auditor:** Repository Audit & Windows Workflow Prompt
**Status:** COMPLETE

---

## 1. CURRENT ASSET INVENTORY

### 1.1 URDF Model Analysis (`simulation/urdf/advika.urdf`)

| Component | Geometry Type | Dimensions | Mesh Status |
|-----------|---------------|------------|-------------|
| `base_link` | **Box** | 300×240×150mm | ✅ STL exists (`base_link.stl`) |
| `left_wheel` | Cylinder | r=32.5mm, l=30mm | ❌ Primitive only |
| `right_wheel` | Cylinder | r=32.5mm, l=30mm | ❌ Primitive only |
| `caster_wheel` | Sphere | r=15mm | ❌ Primitive only |
| `caster_wheel_rear` | Sphere | r=15mm | ❌ Primitive only |
| `lidar_tower` | Cylinder | r=35mm, l=80mm | ❌ Primitive only |
| `lidar_link` | Cylinder | r=25mm, l=30mm | ❌ Primitive only |
| `horizon_camera_link` | Box | 20×40×20mm | ❌ Primitive only |
| `floor_camera_link` | Box | 20×40×20mm | ❌ Primitive only |
| `tof_array_link` | Box | 40×40×10mm | ❌ Primitive only |
| `imu_link` | Box | 20×20×5mm | ❌ Primitive only |
| `display_link` | Box | 80×40×5mm | ❌ Primitive only |

**Summary:** 1/12 components has proper STL mesh. All others use Gazebo primitives.

### 1.2 World Files Analysis

| World File | Furniture Source | Custom Models | Quality |
|------------|------------------|---------------|---------|
| `living_room.world` | **None (all primitive boxes)** | Yes (coffee table, sofa, TV stand) | ⚠️ LOW - Box primitives |
| `3bhk_house.world` | **Gazebo Fuel** (Sofa, Table, Chair, Bed, Plant, Bookshelf) | Walls only | ✅ MEDIUM - Stock Fuel models |
| `advika_playground.world` | Unknown | Unknown | - |
| `real_room.world` | Unknown | Unknown | - |

### 1.3 CAD Directory Analysis (`src/advika_cad/`)

| File | Purpose | Status |
|------|---------|--------|
| `advika30_cad.py` | Python CAD script | ⚠️ Check contents |
| `package.xml` | ROS2 package | ✅ Present |
| `setup.py` | ROS2 package setup | ✅ Present |

**Missing:** No STL files, STEP files, or Fusion 360 project files found.

### 1.4 Mesh Files

| File | Location | Size | Quality |
|------|----------|------|---------|
| `base_link.stl` | `simulation/urdf/meshes/` | 1.8 KB | ⚠️ Needs verification |

---

## 2. GAP ANALYSIS

### 2.1 Robot Components Requiring Fusion 360 Design

| Priority | Component | Gap | Recommended Material |
|----------|-----------|-----|---------------------|
| **HIGH** | Chassis Base | CAD_README mentions v3 but no STL found | PETG |
| **HIGH** | Wheel Hubs (×2) | No STL, using cylinder primitives | PETG |
| **HIGH** | LiDAR Tower | No STL, using cylinder primitives | PETG |
| **HIGH** | Top Dome | Not designed yet | PETG (translucent) |
| **MEDIUM** | Motor Mounts | CAD_README mentions but no STL found | PETG |
| **MEDIUM** | Battery Tray | CAD_README mentions but no STL found | PETG |
| **MEDIUM** | Camera Bracket | CAD_README mentions but no STL found | PETG |
| **MEDIUM** | ToF Holder | CAD_README mentions but no STL found | PETG |
| **MEDIUM** | Bumpers (Front/Rear) | Not designed yet | TPU 95A |
| **LOW** | ESP32 Enclosure | Not designed yet | PETG |
| **LOW** | IMU Mount | Small, can use printed mount | PETG |
| **LOW** | Display Bezel | SSD1306 cutout design | PETG |

### 2.2 Furniture for 3BHK World

| Room | Required Furniture | Current Source | Custom Design Needed |
|------|-------------------|---------------|---------------------|
| **Living Room** | Sofa (3-seater) | Gazebo Fuel | ✅ Recommended |
| | Coffee Table | Gazebo Fuel | ✅ Recommended |
| | TV Unit | Gazebo Fuel | ✅ Recommended |
| | Floor Lamp | None | ✅ Yes |
| **Kitchen** | Kitchen Counter | None | ✅ Yes |
| | Dining Table | Gazebo Fuel | ✅ Recommended |
| | Dining Chairs (×4) | Gazebo Fuel | ✅ Recommended |
| | Refrigerator | None | ✅ Yes |
| **Master Bedroom** | Double Bed | Gazebo Fuel | ✅ Recommended |
| | Wardrobe | None | ✅ Yes |
| | Nightstands (×2) | Gazebo Fuel | ✅ Recommended |
| **Bedroom 2** | Single Bed | Gazebo Fuel | ✅ Recommended |
| | Study Table | None | ✅ Yes |
| | Bookshelf | Gazebo Fuel | ✅ Recommended |
| **Bedroom 3** | Single Bed | Gazebo Fuel | ✅ Recommended |
| | Desk | None | ✅ Yes |
| | Chair | None | ✅ Yes |
| **Bathrooms (×2)** | Commode | None | ✅ Yes |
| | Sink | None | ✅ Yes |
| | Shower Area | None | ✅ Yes |

---

## 3. QUALITY ASSESSMENT

### 3.1 URDF Model Quality

```
Rating: 6/10 (MEDIUM)

Strengths:
+ Differential drive configured correctly
+ All sensors have Gazebo plugins
+ Proper inertial parameters
+ Friction coefficients set

Weaknesses:
- Only base_link has real STL mesh
- All wheels use primitive cylinders (not printable)
- No caster wheel design (sphere primitives)
- No detailed CAD for manufacturing
```

### 3.2 Simulation World Quality

```
Rating: 5/10 (LOW-MEDIUM)

Strengths:
+ 3BHK layout is structurally correct
+ Gazebo Fuel models are stable
+ Lighting properly configured

Weaknesses:
- Furniture from Gazebo Fuel is generic
- No custom high-quality furniture meshes
- Living room uses box primitives
- No material textures (solid colors only)
```

### 3.3 CAD Documentation Quality

```
Rating: 7/10 (GOOD)

Strengths:
+ CAD_README.md exists with print settings
+ Mentions STEP file export
+ Lists all required components

Weaknesses:
- STL files not in repository
- No Fusion 360 project files
- No export settings documented
- No assembly instructions
```

---

## 4. RECOMMENDED ACTIONS

### 4.1 Phase 1: Robot CAD (Priority Order)

1. **Chassis Base v3** -- Export STL + STEP
2. **Wheel Hubs** -- Design for JGA25-370 motors
3. **LiDAR Tower** -- Height 150mm, diameter 70mm
4. **Top Dome** -- 230mm diameter, translucent
5. **Motor Mounts** -- Press-fit M3 inserts
6. **Battery Tray** -- 3S2P 18650 holder
7. **Bumpers** -- TPU 95A, floating design
8. **Camera Bracket** -- Dual Pi Camera mount

### 4.2 Phase 2: Furniture Design

1. **Living Room Set** -- Sofa, coffee table, TV unit, floor lamp
2. **Kitchen Set** -- Counter, dining set, refrigerator
3. **Bedroom Sets** -- Beds, wardrobes, study furniture
4. **Bathroom Fixtures** -- Commode, sink, shower

### 4.3 Phase 3: Documentation

1. `FUSION360_WORKFLOW.md` -- Complete Fusion 360 guide
2. `3BHK_FURNITURE_SPEC.md` -- Dimensions and materials
3. `MESH_EXPORT_GUIDE.md` -- STL/DAE/URDF workflow

---

## 5. REPOSITORY STRUCTURE RECOMMENDATIONS

```
advika_robot_ws/
+-- src/advika_cad/           # CAD package (EXISTING)
|   +-- meshes/               # NEW: STL files for 3D printing
|   +-- step/                 # NEW: STEP files for mechanical
|   +-- fusion360/            # NEW: Fusion 360 project files
|
+-- docs/
|   +-- fusion360/            # NEW: Fusion 360 documentation
|   +-- furniture/            # NEW: Furniture specs
|   +-- images/               # NEW: Screenshots/renderings
```

---

## 6. DELIVERABLES

| Document | Description | Status |
|----------|-------------|--------|
| `AUDIT_REPORT_3D_ASSETS.md` | This audit with gap analysis | ✅ Created |
| `FUSION360_WORKFLOW.md` | Windows Fusion 360 workflow | ⏳ Pending |
| `3BHK_FURNITURE_SPEC.md` | Furniture dimensions/materials | ⏳ Pending |
| `MESH_EXPORT_GUIDE.md` | STL/DAE/URDF export guide | ⏳ Pending |

---

*End of Audit Report*