# 📋 Advika 3.0 — Complete Simulation Checklist

**Repository:** https://github.com/TheAbhishekraj/advika_robot_ws  
**Workspace:** `~/Documents/Robotics/advika_robot_ws`  
**ROS2:** Jazzy Jalisco | **Gazebo:** Harmonic 8.10.0

---

## 🏁 PHASE A: Robot Spawning

| # | Task | Command | Status |
|---|------|---------|--------|
| A1 | Check spawn_entity | `grep -r "spawn_entity" src/advika_sim/launch/` | ✅ |
| A2 | Check spawn delay | `grep -A5 -B5 "spawn_entity" src/advika_sim/launch/*.py` | ✅ |
| A3 | Check URDF path | `ls src/advika_description/urdf/` | ✅ |
| A5 | Fix spawn delay | TimerAction 5.0s in launch file | ✅ |

### ✅ CHECKPOINT A
- [x] Entity Tree shows **`advika`** in Gazebo
- [x] Robot visible in Gazebo world

---

## 🏠 PHASE B: 3BHK Environment

| # | Task | Details | Status |
|---|------|---------|--------|
| B1 | Create world SDF | `src/advika_sim/worlds/3bhk_house.world` | ✅ |
| B2 | Living Room | 6.0 × 4.5 m | ✅ |
| B3 | Kitchen | 3.6 × 3.0 m | ✅ |
| B4 | Master Bedroom | 4.5 × 3.6 m | ✅ |
| B5-B7 | Bedrooms 2 & 3, Bathrooms | 3.6×3.0, 2.4×1.8 m | ✅ |
| B8 | Hallway | 0.6 m wide | ✅ |
| B9 | Update launch file | Points to `3bhk_house.world` | ✅ |
| B10 | Rebuild workspace | `colcon build --symlink-install` | ✅ |

### ✅ CHECKPOINT B
- [x] Gazebo shows 3BHK house with all walls
- [x] Entity Tree: wall_north, wall_south, wall_east, wall_west, wall_inner_1, wall_inner_2

---

## ⚙️ PHASE C: Parameter Tuning

| # | Parameter | File | Value | Status |
|---|-----------|------|-------|--------|
| C1 | max_linear_velocity | `advika.urdf` | 0.5 m/s | ✅ |
| C2 | max_angular_velocity | `advika.urdf` | 1.0 rad/s | ✅ |
| C3 | Wheel friction mu | `advika.urdf` | 0.8 (tile) | ✅ |
| C4 | LiDAR max_range | `advika.urdf` | 5.0 m | ✅ |
| C5 | LiDAR update_rate | `advika.urdf` | 20 Hz | ✅ |
| C6 | Camera resolution | `advika.urdf` | 320×240 px | ✅ |
| C7 | Camera FOV | `advika.urdf` | 1.22 rad (70°) | ✅ |
| C8 | Physics RTF | `3bhk_house.world` | 2.0x | ✅ |
| C9 | Nav2 max_vel_x | `nav2_params.yaml` | 0.5 | ✅ |
| C10 | Nav2 AMCL update_min | `nav2_params.yaml` | 0.1 m | ✅ |

### ✅ CHECKPOINT C — All parameters tuned and applied

---

## 🚗 PHASE D: Drive in 3BHK

| # | Task | Status |
|---|------|--------|
| D1 | Launch 3BHK world | ✅ |
| D2 | Teleop active (speed 0.50, turn 1.00) | ✅ |
| D3 | Robot drives in living room | ✅ |
| D4 | LiDAR scan active | ✅ |
| D5 | Camera feeds visible | ✅ |

```bash
# Launch:
ros2 launch advika_sim sim_bringup.launch.py
# OR one-liner:
python3 scripts/auto_sim.py --teleop

# Teleop (new terminal):
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args -r cmd_vel:=/advika/cmd_vel
```

### ✅ CHECKPOINT D — Robot drives, LiDAR and cameras confirmed

---

## 🗺️ PHASE E: SLAM Mapping

| # | Task | Command | Status |
|---|------|---------|--------|
| E1 | Launch SLAM | `ros2 launch advika_navigation slam.launch.py` | ☐ |
| E2 | Drive all rooms | Teleop through each room | ☐ |
| E3 | Watch map build | Enable Map display in RViz | ☐ |
| E4 | Save map | `ros2 run nav2_map_server map_saver_cli -f ~/Documents/Robotics/advika_robot_ws/maps/advika_3bhk_map` | ☐ |

```bash
CheckPoint: E | Status: [PASS/FAIL/STUCK]
Files: advika_3bhk_map.yaml [YES/NO] | advika_3bhk_map.pgm [YES/NO]
```

---

## 🎯 PHASE F: Autonomous Navigation

| # | Task | Status |
|---|------|--------|
| F1 | Launch Nav2 with map | ☐ |
| F2 | Set 2D Pose Estimate in RViz | ☐ |
| F3 | Send Nav2 Goal → Kitchen | ☐ |
| F4 | Send Nav2 Goal → Bedroom 2 | ☐ |
| F5 | Verify obstacle avoidance | ☐ |
| F6 | Verify doorway navigation | ☐ |

```bash
ros2 launch advika_navigation nav2.launch.py \
  map:=~/advika_3bhk_map.yaml

CheckPoint: F | Status: [PASS/FAIL/STUCK]
Goals: Kitchen [YES/NO] | Bedroom [YES/NO] | Avoids Walls: [YES/NO]
```

---

## 🏆 Final Status

| Phase | Status | Date |
|-------|--------|------|
| A: Robot Spawning | ✅ PASS | 2026-07-25 |
| B: 3BHK Environment | ✅ PASS | 2026-07-25 |
| C: Parameter Tuning | ✅ PASS | 2026-07-25 |
| D: Test Driving | ✅ PASS | 2026-07-25 |
| E: SLAM Mapping | ☐ Pending | — |
| F: Autonomous Nav | ☐ Pending | — |

---

## 📝 Progress Report Template

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ADVIKA 3.0 — PROGRESS REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Phase: [A/B/C/D/E/F] | Task: [#]
What I did: 
Command run: 
Actual output: 
Status: [PASS/FAIL/STUCK]
Screenshots: [YES/NO]
Errors: 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
