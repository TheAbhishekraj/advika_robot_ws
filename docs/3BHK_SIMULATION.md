# Advika 3.0 AMR — 3BHK Simulation Guide

**Workspace:** `~/Documents/Robotics/advika_robot_ws`
**ROS2:** Jazzy Jalisco | **Gazebo:** Harmonic 8.10.0

---

## 🚀 Quick Start

```bash
cd ~/Documents/Robotics/advika_robot_ws
source install/setup.bash

# Option A: Auto-launcher (recommended)
python3 scripts/auto_sim.py

# Option B: Manual launch
ros2 launch advika_sim sim_bringup.launch.py
```

### With Teleop
```bash
python3 scripts/auto_sim.py --teleop
# OR manually in a new terminal:
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r cmd_vel:=/advika/cmd_vel
```

---

## 🏠 3BHK World Layout

The virtual house (`3bhk_house.world`) covers a **12 m × 10 m** footprint:

| Room           | Width | Depth | Notes          |
|----------------|-------|-------|----------------|
| Living Room    | 6.0 m | 4.5 m | Robot start zone |
| Kitchen        | 3.6 m | 3.0 m | —              |
| Master Bedroom | 4.5 m | 3.6 m | —              |
| Bedroom 2      | 3.6 m | 3.0 m | —              |
| Bedroom 3      | 3.6 m | 3.0 m | —              |
| Bathroom 1 & 2 | 2.4 m | 1.8 m | 0.8 m doorways |
| Hallway        | 0.6 m | var.  | Connects rooms |

---

## ⚙️ Tuned Parameters

| Component        | Parameter            | Value       | Why            |
|------------------|----------------------|-------------|----------------|
| DiffDrive        | max_linear_velocity  | 0.5 m/s     | Safe indoor    |
| DiffDrive        | max_angular_velocity | 1.0 rad/s   | Tight corners  |
| LiDAR            | max_range            | 5.0 m       | Room scale     |
| LiDAR            | update_rate          | 20 Hz       | Better mapping |
| Camera           | resolution           | 320 × 240   | Faster RTF     |
| Camera           | FOV                  | 1.22 rad    | 70° wide-angle |
| Wheel friction   | mu1/mu2              | 0.8         | Tile floor     |
| Physics RTF      | real_time_factor     | 2.0         | Faster sim     |
| AMCL             | update_min_d         | 0.1 m       | Finer updates  |

---

## 🗺️ SLAM Mapping

```bash
# Terminal 1: Launch SLAM
ros2 launch advika_navigation slam.launch.py

# Terminal 2: Drive through all rooms
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r cmd_vel:=/advika/cmd_vel

# Terminal 3: Save map when done
ros2 run nav2_map_server map_saver_cli \
  -f ~/Documents/Robotics/advika_robot_ws/maps/advika_3bhk_map
```

---

## 🤖 Autonomous Navigation

```bash
ros2 launch advika_navigation nav2.launch.py \
  map:=~/Documents/Robotics/advika_robot_ws/maps/advika_3bhk_map.yaml
```
Then in RViz:
1. **2D Pose Estimate** → click robot location
2. **Nav2 Goal** → click destination room

---

## 🔌 Hardware Test

```bash
python3 scripts/test_peripherals.py
```

> ⚠️ **Safety:** Wheels must be off the ground before enabling motors!

---

## 📊 Diagnostics

| Report | Path |
|--------|------|
| Hardware Test (TRX) | `docs/reports/diagnostic_report.trx` |
| Audit Report (MD) | `docs/reports/audit_report.md` |

---

## 🔧 Common Fixes

**RViz TF queue full:**
→ Fixed: `Fixed Frame` changed from `map` → `odom` in `simulation/config/advika_sim.rviz`

**Robot not spawning:**
→ Fixed: Spawn delay increased to 5 seconds in `sim_bringup.launch.py`

**xterm not found:**
→ Fixed: Teleop removed from launch file; run manually in a new terminal

---

## 📁 File Structure

```
advika_robot_ws/
├── scripts/
│   ├── auto_sim.py          ← Auto-launcher (NEW)
│   └── test_peripherals.py
├── src/advika_sim/
│   └── worlds/3bhk_house.world   ← 3BHK world (NEW)
├── simulation/config/
│   ├── advika_sim.rviz      ← Fixed TF frame
│   └── nav2_params.yaml     ← Tuned Nav2
├── maps/
│   └── real_room.yaml       ← Simulated map
└── docs/reports/
    ├── audit_report.md
    └── diagnostic_report.trx
```
