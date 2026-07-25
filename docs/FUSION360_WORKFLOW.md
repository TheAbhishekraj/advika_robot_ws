# ADVIKA 3.0 — FUSION 360 / FREECAD WORKFLOW

**Version:** 1.0 | **Date:** 2026-07-25

---

## 📋 Overview

Advika 3.0 CAD models are generated parametrically in **FreeCAD** (Linux) or **CadQuery** (Python). This guide covers:
1. Using FreeCAD on Ubuntu for direct editing
2. Importing STEP files into Fusion 360 (Windows/Mac) for modifications
3. Exporting back to STL/STEP for the Advika pipeline

---

## 🐧 FreeCAD Workflow (Linux — Primary)

### Install FreeCAD
```bash
sudo apt update
sudo apt install -y freecad
```

### Generate All Parts
```bash
# Automated generation
bash ~/advika_robot_ws/src/advika_cad/scripts/generate_all.sh

# Manual via FreeCAD CLI
freecadcmd ~/advika_robot_ws/src/advika_cad/scripts/generate_all.py
```

### Edit Parts in FreeCAD GUI
```bash
# Open a specific part
freecad ~/advika_robot_ws/src/advika_cad/fcstd/advika30_base_plate.FCStd
```

### Key FreeCAD Operations
| Action | Menu / Shortcut |
|--------|----------------|
| Create Box | Part → Primitives → Box |
| Create Cylinder | Part → Primitives → Cylinder |
| Boolean Cut | Part → Boolean → Cut |
| Boolean Union | Part → Boolean → Union |
| Fillet Edges | Part → Fillet |
| Measure Distance | View → Measure → Distance |
| Export STL | File → Export → Mesh (STL) |
| Export STEP | File → Export → STEP |

### Parametric Editing (Python Console)
FreeCAD has a built-in Python console for parametric changes:
```python
# In FreeCAD Python console:
import FreeCAD
doc = FreeCAD.ActiveDocument

# Change base plate dimensions
base = doc.getObject("base_plate")
# Modify and recompute
doc.recompute()

# Re-export
import Mesh
Mesh.export([base], "/path/to/advika30_base_plate.stl")
```

---

## 🪟 Fusion 360 Workflow (Windows/Mac — Secondary)

### Import STEP Files
1. Open Fusion 360
2. **File → Open → Open from my computer**
3. Select STEP file from `src/advika_cad/step/advika30_*.step`
4. Fusion 360 imports all bodies and features

### Recommended Project Setup
```
Fusion 360 Projects
└── Advika_3_0/
    ├── 01_Base_Plate
    ├── 02_Mid_Frame
    ├── 03_Top_Cover
    ├── 04_Motor_Mount
    ├── 05_Wheel_Hub
    ├── 06_Caster_Housing
    ├── 07_Camera_Mount_Horizon
    ├── 08_Camera_Mount_Floor
    ├── 09_Battery_Retainer
    ├── 10_Bumper
    ├── 11_ToF_Mount
    ├── 12_ESP32_Enclosure
    └── 13_IMU_Mount
```

### Modify in Fusion 360
1. Right-click imported body → **Edit Feature**
2. Modify sketches, extrusions, fillets
3. Add your own features (extra mounting holes, aesthetic changes)
4. **Design → Inspect → Mass Properties** — verify weight

### Export Back to STL
1. Right-click body → **Save As Mesh**
2. Format: **STL (Binary)**
3. Refinement: **High**
4. Save to `src/advika_cad/meshes/`

### Export STEP for Sharing
1. **File → Export**
2. Format: **STEP (.step)**
3. Save to `src/advika_cad/step/`

---

## 🔄 Bidirectional Workflow

```
┌─────────────┐     STEP      ┌─────────────┐
│   FreeCAD   │ ──────────→  │  Fusion 360  │
│   (Linux)   │ ←──────────  │  (Windows)   │
└──────┬──────┘     STEP      └──────┬──────┘
       │                              │
       ├── STL → 3D Print             ├── STL → 3D Print
       ├── DAE → Gazebo               ├── OBJ → Gazebo
       └── FCStd → Parametric         └── F3D → Parametric
```

- **STEP** is the universal interchange format
- Always re-export **STL** from the modified source (FreeCAD or Fusion)
- Never edit STL directly (mesh-based, loses parametric info)

---

## 📐 Design Guidelines

| Rule | Value | Reason |
|------|-------|--------|
| Min wall thickness | 2.0mm | FDM printability |
| Min hole diameter | 2.0mm (pilot), 3.3mm (M3 clearance) | Drill/insert fit |
| Fillet radius (external) | 3.0mm minimum | Child safety |
| Fillet radius (internal) | 2.0mm minimum | FDM stress concentration |
| Overhang angle max | 45° | Print without supports |
| Feature separation | ≥ 1.0mm | FDM resolution limit |
| Heat-set insert boss OD | 10.0mm | M3 insert spec |
| Heat-set insert pilot Ø | 4.2mm × 3.5mm deep | Manufacturer spec |

---

## 📚 Resources

- [FreeCAD Documentation](https://wiki.freecad.org/)
- [Fusion 360 Tutorials](https://youtube.com/@AutodeskFusion360)
- [CadQuery Documentation](https://cadquery.readthedocs.io/)
- [STEP File Format](https://en.wikipedia.org/wiki/ISO_10303-21)