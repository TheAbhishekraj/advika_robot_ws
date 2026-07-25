# ADVIKA 3.0 — CAD DESIGN OVERVIEW

**Version:** 1.0 | **Date:** 2026-07-25

> 📌 **Master Setup:** Follow [SETUP.md](../SETUP.md) for workspace setup before running CAD generation.

---

## 🏗️ Mechanical Architecture

| Property | Value |
|----------|-------|
| **Form Factor** | Compact differential-drive AMR |
| **Envelope** | 300 × 240 × 150mm (230mm with LiDAR dome) |
| **Target Weight** | 2.5 kg (assembled, no battery) |
| **Ground Clearance** | 15mm |
| **Materials** | PETG (structural), TPU 95A (bumpers/gaskets) |
| **Fasteners** | M3 brass heat-set inserts (~40), M3 SHCS (~40), M4 shoulder bolts (8) |

---

## 📦 Component Inventory (20 Printed Parts)

| # | Part Name | Qty | Material | Infill | Dimensions |
|---|-----------|-----|----------|--------|------------|
| A | Base Plate | 1 | PETG | 50% | 300×240×5mm |
| B | Mid Frame | 1 | PETG | 30% | 300×240×150mm (walls) |
| C | Top Cover (w/ LiDAR dome) | 1 | PETG | 30% | 300×240×2.5mm + dome |
| D | Motor Mount Bracket (L/R) | 2 | PETG | 30% | Split-collar JGA25 |
| E | Wheel Hub (L/R) | 2 | PETG | 50% | 65mm dia, 6mm D-bore |
| F | Caster Housing (F/R) | 2 | PETG | 30% | 20×20×8mm, 15mm ball |
| G | Camera Mount — Horizon (15° up) | 1 | PETG | 30% | 30×29×4mm |
| H | Camera Mount — Floor (45° down) | 1 | PETG | 30% | 30×29×4mm |
| I | Battery Retainer (sliding) | 1 | PETG | 30% | 71×20×3mm |
| J | Bumper Front/Rear | 2 | TPU 95A | 40% | 280×220×60mm shell |
| K | ToF Sensor Mount | 1 | PETG | 30% | 70×15×3mm, 60mm spacing |
| L | ESP32 Enclosure | 1 | PETG | 30% | 59×32×15mm |
| M | IMU Mount | 1 | PETG | 30% | 30×37×3mm |
| N | Gasket — Top Perimeter | 1 | TPU 95A | — | 2mm thick seal |
| O | Gasket — Pi Vibration Pad | 1 | TPU 95A | — | 85×56×3mm |
| P | Gasket — Motor Isolation | 2 | TPU 95A | — | Ø25mm ring |

---

## 🔧 CAD Generation

### Generate All Parts
To automatically install dependencies (CadQuery) and generate all STL and STEP files:
```bash
# One-command universal generation
bash ~/advika_robot_ws/src/advika_cad/scripts/install_and_generate.sh
```

### FreeCAD Rendering Automation
Want to see the colors natively applied in FreeCAD? Once you have run the generation script above, open FreeCAD and run our automatic styling macro from the Python Console:
```python
exec(open("/home/abhishek/advika_robot_ws/scripts/freecad_macro.py").read())
```
This macro will start a fresh document, sequentially load the 17 STLs we just compiled, map exact RGB HEX codes, and inject structural dimensions for computing modules!

### Output
```
src/advika_cad/
├── scripts/
│   ├── generate_all.py       # Parametric Python CAD generator
│   └── generate_all.sh       # Shell runner script
├── meshes/                   # STL files for 3D printing
│   ├── advika30_base_plate.stl
│   ├── advika30_mid_frame.stl
│   ├── advika30_wheel_hub_L.stl
│   └── ... (20 STL files total)
├── step/                     # STEP files for mechanical review
│   ├── advika30_base_plate.step
│   └── advika30_assembly.step
├── fcstd/                    # FreeCAD native documents
│   └── advika30_base_plate.FCStd
├── advika30_cad.py           # CadQuery-based model (legacy)
└── advika_cad/               # ROS2 package
```

---

## 📚 Related Documentation

| Document | Purpose |
|----------|---------|
| [PRINT_SETTINGS.md](PRINT_SETTINGS.md) | PETG & TPU slicing parameters |
| [ASSEMBLY_GUIDE.md](ASSEMBLY_GUIDE.md) | Step-by-step assembly instructions |
| [MESH_EXPORT_GUIDE.md](MESH_EXPORT_GUIDE.md) | STL → DAE → URDF mesh pipeline |
| [FUSION360_WORKFLOW.md](FUSION360_WORKFLOW.md) | Importing STEP files into Fusion 360 |
| [BOM.md](BOM.md) | Complete Bill of Materials |
