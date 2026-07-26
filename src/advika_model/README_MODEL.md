# ADVIKA 3.0 — COMPLETE MODEL DESIGN PACKAGE
**Source:** `C:\Users\HP\Advika_3.0\` (mirror)
**Purpose:** Complete design reference — STL generation, ROS2 config, assembly, PDCA

---

## 📁 Directory Structure

```
advika_model/
├── ADVIKA_3_0_README.md     ← Complete Fusion 360 usage guide
├── Advika_3_0_PDCA.md        ← PDCA improvement plan
│
├── ros2/
│   ├── advika_3_0.urdf       ← ROS2 URDF (Gazebo-ready)
│   ├── config/
│   │   ├── advika_controllers.yaml
│   │   ├── nav2_params.yaml
│   │   └── slam_params.yaml
│   └── launch/
│       ├── display.launch.py
│       ├── gazebo.launch.py
│       └── slam.launch.py
│
├── meshes/
│   ├── visual/                ← STLs for RViz/Gazebo visual
│   │   └── advika_*.stl      (16 STLs)
│   └── collision/             ← Low-poly STLs for physics
│       └── advika_*_col.stl   (16 STLs)
│
├── docs/
│   ├── 3D_PRINT_GUIDE.md     ← Print settings per part
│   ├── PROJECT_INDEX.md      ← Project index
│   ├── bom_stl.csv           ← STL BOM
│   ├── reports/
│   │   ├── FINAL_PDCA_REPORT.md
│   │   ├── advika_bom.csv
│   │   ├── advika_pdca_report.csv
│   │   └── advika_pdca_v2_improvements.csv
│   └── wiring_diagram_placeholder.txt
│
├── assembly/
│   └── ASSEMBLY_STEPS.md     ← Step-by-step assembly guide
│
├── scripts/
│   └── advika_3_0_generator.py ← Fusion 360 API script
│
└── excel/
    └── advika_3_0_master.xlsx  ← Master spreadsheet
```

---

## 🔧 STL Generation (Fusion 360)

### Run the Generator Script
```
1. Copy to: %APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\Advika3_0\
2. Open Fusion 360 → New Design → "Advika 3.0" → Units: mm
3. Press Shift + S → Scripts → Advika3_0 → Run
4. Wait for 14 components to be created
5. Export each as Binary STL at 0.01mm (Fine) quality
```

### STL Filenames (EXACT — 16 files)
```
advika_chassis.stl           300×240×5mm
advika_motor_mount_L.stl     Ø30×20mm
advika_motor_mount_R.stl     mirror
advika_wheel_hub_L.stl      Ø65×20mm
advika_wheel_hub_R.stl       mirror
advika_lidar_tower.stl       Ø70×150mm hollow
advika_top_dome.stl         Ø115×80mm
advika_camera_horizon.stl    25×24×8mm
advika_camera_floor.stl       25×24×8mm
advika_imu_mount.stl         20×20×5mm
advika_battery_tray.stl      80×70×25mm hollow
advika_bumper_front.stl      280×30×20mm hollow
advika_bumper_rear.stl        mirror
advika_esp32_enclosure.stl  55×30×15mm hollow
advika_esp32_lid.stl         55×30×2mm
advika_axle_shaft.stl        Ø8×170mm (steel, not printed)
```

---

## 🤖 ROS2 Usage

```bash
# Launch Gazebo simulation
ros2 launch advika_model gazebo.launch.py

# SLAM mapping
ros2 launch advika_model slam.launch.py

# Display / RViz
ros2 launch advika_model display.launch.py
```

---

## 📊 PDCA Summary

| Component | Status | Notes |
|-----------|--------|-------|
| v1.0 Initial (14 parts) | ✅ PASS | All dimensions verified |
| v2.0 Improvements (4 items) | ✅ PASS | Tyre tread, D-flat bore, cable channels, ESP32 lid |
| STL files (16) | ✅ Ready | Export from Fusion 360 |
| ROS2 URDF | ✅ Ready | Gazebo DiffDrive plugin |
| Assembly Guide | ✅ Ready | Step-by-step |

---

## 🔗 Related Docs

| Document | Location | Purpose |
|----------|----------|---------|
| STL Requirements | `src/advika_description/stl/STL_REQUIREMENTS.md` | Exact specs for each STL |
| PCB Design | `src/firmware/Advika30_PCB/` | Eagle BRD + Gerbers |
| Wiring | `docs/pcb/pin_mapping.md` | GPIO table |
| BOM | `docs/BOM.md` | Full INR BOM |
| Learning Manual | `docs/LEARNING_MANUAL.md` | "I am 5" style guide |

---

**Version:** 1.0 | **Source:** `C:\Users\HP\Advika_3.0\` | **Date:** 2026-07-26