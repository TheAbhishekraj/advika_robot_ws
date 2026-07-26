# ADVIKA 3.0 â MASTER PROJECT INDEX

> **Version:** 3.0 Final  
> **Last Audit:** 2026-07-26  
> **Status:** Electronics complete | Mechanical complete | Docs consolidated  
> **Robot Type:** Differential Drive Indoor Mobile Robot  

---

## ð Electronics â C:\Users\HP\Documents\

| File | Size | Role | Status |
|------|------|------|--------|
| `Advika30_CLEAN.brd` | 56.89 KB | Master board design (CLEAN, latest) | â |
| `Advika30_Gerber_Manufacturing.zip` | 5.12 KB | Gerber ZIP for fab | â |
| `Advika30_Main_PCB.pro` | 0.74 KB | Project file | â |
| `pcb_bom.csv` | 2.15 KB | Electronics BOM (25 line items) | â |
| `pcb_top_layer.png` | 21.94 KB | Top layer render | â |
| `pcb_bottom_layer.png` | 11.70 KB | Bottom layer render | â |
| `pcb_top_layer.svg` | 29.38 KB | Top layer vector | â |
| `pcb_bottom_layer.svg` | 7.90 KB | Bottom layer vector | â |
| `pin_mapping.md` | 2.96 KB | GPIO + connector reference | â |
| `wiring_diagram.html` | 2.98 KB | Interactive wiring reference | â |
| `schematic.pdf` | â | Schematic reference HTML | â (re-export PDF from Fusion) |

## ð Gerber Files â C:\Users\HP\Documents\gerber_files\

| File | Layer | Status |
|------|-------|--------|
| `Advika30_Top_Copper.gtl` | Top copper | â Fab-ready |
| `Advika30_Bottom_Copper.gbl` | Bottom copper | â Fab-ready |
| `Advika30_Top_SolderMask.gts` | Top solder mask | â Fab-ready |
| `Advika30_Top_Silkscreen.gto` | Top silkscreen | â Fab-ready |
| `Advika30_Board_Outline.gko` | Board outline | â Fab-ready |
| `Advika30_Drill.drl` | Drill file | â Fab-ready |
| `Advika30_Bottom_SolderMask.gbs` | Bottom solder mask | â ï¸ Placeholder â re-export |
| `Advika30_Bottom_Silkscreen.gbo` | Bottom silkscreen | â ï¸ Placeholder â re-export |
| `Advika30_Netlist.ipc` | IPC netlist | â |
| `Advika30_PickPlace.csv` | Pick & place | â |

## ð Mechanical â C:\Users\HP\Advika_3.0\STL\ (16 parts)

| STL File | Dimensions | Material | Infill | Status |
|----------|-----------|----------|--------|--------|
| advika_chassis.stl | 200Ã150Ã3mm | PLA Dark Grey | 20% | â |
| advika_motor_mount_L.stl | 30Ã30Ã20mm | PLA Blue | 40% | â |
| advika_motor_mount_R.stl | 30Ã30Ã20mm | PLA Blue | 40% | â |
| advika_wheel_hub_L.stl | Ã60Ã10mm | PLA Black | 50% | â |
| advika_wheel_hub_R.stl | Ã60Ã10mm | PLA Black | 50% | â |
| advika_axle_shaft.stl | Ã8Ã170mm | PLA/Steel | 100% | â |
| advika_lidar_tower.stl | 40Ã40Ã80mm | PLA Lt Grey | 30% | â |
| advika_top_dome.stl | Ã100Ã50mm | PLA Green | 15% | â |
| advika_camera_horizon.stl | 50Ã30Ã20mm | PLA Amber | 25% | â |
| advika_camera_floor.stl | 40Ã25Ã15mm | PLA Amber | 25% | â |
| advika_imu_mount.stl | 30Ã30Ã8mm | PLA Purple | 30% | â |
| advika_battery_tray.stl | 150Ã80Ã20mm | PLA Orange | 30% | â |
| advika_bumper_front.stl | 210Ã15Ã10mm | PLA Red | 45% | â |
| advika_bumper_rear.stl | 210Ã15Ã10mm | PLA Red | 45% | â |
| advika_esp32_enclosure.stl | 60Ã40Ã20mm | PLA Cyan | 25% | â |
| advika_esp32_lid.stl | 60Ã40Ã5mm | PLA Cyan | 25% | â |

## ð Documentation â C:\Users\HP\Advika_3.0\docs\

| File | Contents | Status |
|------|----------|--------|
| `BOM.csv` | Full mechanical + hardware BOM | â |
| `pcb_electronics_bom.csv` | Electronics BOM (copy) | â |
| `pin_mapping.md` | ESP32 GPIO + power + connectors | â |
| `wiring_diagram.html` | Interactive wiring reference | â |
| `pcb_assembly.pdf` | PCB assembly sequence (HTML) | â (re-export PDF from Fusion) |
| `pcb_3d_view.png` | PCB top layer preview | â |
| `pcb_top_layer.png` | PCB top render | â |
| `pcb_bottom_layer.png` | PCB bottom render | â |
| `PROJECT_INDEX.md` | This file | â |
| `3D_PRINT_GUIDE.md` | Print settings guide | â |
| `FINAL_PDCA_REPORT.md` | PDCA report | â |

## ð ROS2 â C:\Users\HP\Advika_3.0\ROS2\

| File/Folder | Status |
|-------------|--------|
| `urdf/advika_3_0.urdf` | â Full URDF with sensors & Gazebo plugins |
| `launch/display.launch.py` | â |
| `launch/gazebo.launch.py` | â |
| `launch/slam.launch.py` | â |
| `config/nav2_params.yaml` | â |
| `config/slam_params.yaml` | â |
| `config/advika_controllers.yaml` | â |
| `meshes/visual/` (16 STLs) | â |
| `meshes/collision/` (16 STLs) | â |

## â ï¸ Outstanding Items (Manual Actions Required)

| Item | Task | Location |
|------|------|----------|
| F1 | Open & verify BRD in Fusion Electronics â confirm 21 components, 100Ã80mm dimensions | Fusion Electronics â Advika30_CLEAN.brd |
| F2 | Run DRC inside Fusion Electronics (Ctrl+D) â confirm 0 errors | Fusion Electronics |
| F3 | Export STEP (File â Export â STEP â pcb_3d.step) | Fusion Electronics |
| F3 | Capture 3D PCB screenshot â pcb_3d_view.png | Fusion Electronics |
| F5 | Export official PDF schematic (File â Export â Schematic as PDF) | Fusion Electronics |
| F6 | Open chassis .f3d or insert pcb_3d.step into assembly at Z=10mm | Fusion 360 Design |
| F7 | Run Thermal simulation (RPi5 5W, DRV8833 1W, ESP32 0.5W, ambient 25Â°C) | Fusion Simulation |
| F8 | Run Static Stress sim on chassis (2.5kg load, PETG material) | Fusion Simulation |
| F4 | Re-export GBS + GBO from Fusion Electronics (placeholder files exist) | Fusion Electronics |

---
_Generated by Advika 3.0 Master Audit | 2026-07-26_
