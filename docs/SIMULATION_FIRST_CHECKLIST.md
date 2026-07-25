# 🚀 QUICK START: SIMULATION FIRST CHECKLIST

**Rule #1:** No hardware purchases until simulation is complete
**Rule #2:** Design must be validated in CAD before printing
**Rule #3:** Print small test parts before large expensive ones

---

## IMMEDIATE ACTION: STEPS 1–5 (First 15 Minutes)

Follow [SETUP.md](../SETUP.md) for full instructions:

```bash
# Step 1: Clone repo
git clone https://github.com/TheAbhishekraj/advika_robot_ws.git && cd advika_robot_ws

# Step 2: Pull latest changes
git pull origin main

# Step 3: Check system prerequisites
bash ~/advika_robot_ws/scripts/verify_prerequisites.sh

# Step 4: Build workspace
source /opt/ros/jazzy/setup.bash && colcon build --symlink-install && source install/setup.bash

# Step 5: Run first simulation
ros2 launch advika_sim sim_bringup.launch.py
```

- [ ] Step 1 & 2: Repository updated (`git pull origin main`)
- [ ] Step 3: All prerequisite checks passed (`verify_prerequisites.sh`)
- [ ] Step 4: Workspace built (`colcon build`)
- [ ] Step 5: Gazebo & RViz2 open successfully without errors
- [ ] Robot model visible in playground

If NO → See [SETUP.md](../SETUP.md) or [TROUBLESHOOTING.md](../TROUBLESHOOTING.md). Stop here. Do not proceed to hardware.

---

## PHASE 1 CHECKLIST: SIMULATION (Complete before Week 2)

### Basic Functionality
- [ ] Launch `advika_sim` without errors
- [ ] Robot visible in Gazebo playground
- [ ] Send `cmd_vel` and robot moves
- [ ] Screenshot: Robot moved from origin

### URDF Understanding
- [ ] Open `simulation/urdf/advika.urdf`
- [ ] Identify all 12 links (base_link, wheels, sensors, etc.)
- [ ] Change base_link color from blue to red
- [ ] Rebuild and verify color change
- [ ] Screenshot: Red robot

### 3BHK World
- [ ] Launch with 3BHK world (or living_room)
- [ ] Teleoperate through at least 2 rooms
- [ ] Screenshot: Robot in 3BHK environment

### Navigation
- [ ] Run SLAM Toolbox
- [ ] Drive around and create map
- [ ] Save map with `map_saver`
- [ ] Navigate to a waypoint autonomously
- [ ] Screenshot: Saved map

### HITL Dashboard
- [ ] Launch hitl_bridge
- [ ] Open http://localhost:8080
- [ ] Drive robot via web interface
- [ ] Screenshot: Dashboard with controls

**PHASE 1 COMPLETE when:** All boxes checked. Screenshots saved.

---

## PHASE 2 CHECKLIST: DESIGN (Complete before Week 6)

### Fusion 360 Setup
- [ ] Fusion 360 installed on Windows
- [ ] Created "Advika_Learning" project
- [ ] Completed one beginner tutorial

### First Component
- [ ] Designed 50×50×10mm test block
- [ ] Exported as STL
- [ ] Printed successfully
- [ ] Photo: Printed block with ruler

### Wheel Hub (Your First Real Part)
- [ ] Analyzed wheel hub requirements (65mm OD, 6mm bore, 12mm height)
- [ ] Created sketch with all features
- [ ] Extruded 3D model
- [ ] Exported STL
- [ ] Printed with PETG
- [ ] Photo: Wheel hub, front and side view

### Chassis Base (The Big One)
- [ ] Analyzed requirements (300×240×5mm, mounting holes)
- [ ] Created full sketch with all holes and channels
- [ ] Extruded 3D model
- [ ] Exported STL
- [ ] **Printed in draft mode first** (fast, low quality)
- [ ] Verified dimensions with caliper
- [ ] Reprinted in final mode if needed
- [ ] Photo: Chassis with all holes visible

### Remaining Components
- [ ] LiDAR Tower designed
- [ ] Top Dome designed
- [ ] Motor mounts designed
- [ ] Battery tray designed
- [ ] Camera bracket designed
- [ ] All exported as STL

**PHASE 2 COMPLETE when:** 9 STL files in `src/advika_cad/meshes/`

---

## PHASE 3 CHECKLIST: PRE-HARDWARE (Week 9+)

### Documentation
- [ ] Bill of Materials created (`docs/BOM.md`)
- [ ] Hardware cost estimate completed
- [ ] Supplier links collected

### URDF Integration
- [ ] Replaced all primitive geometries with STL meshes in URDF
- [ ] Verified collision geometry matches visual
- [ ] Robot looks correct in Gazebo with new meshes
- [ ] Screenshot: Robot with STL meshes

### Manufacturing
- [ ] Identified print service or bought 3D printer
- [ ] Printed full chassis in PETG
- [ ] All holes tapped for M3 threads
- [ ] Test-fitted all components
- [ ] Photo: Parts laid out for assembly

### Parts Ordering
- [ ] Raspberry Pi 5 (8GB) - ~$80
- [ ] ESP32-S3 DevKit - ~$15
- [ ] JGA25-370 Motors ×2 - ~$30
- [ ] LD06 LiDAR - ~$60
- [ ] VL53L5CX ToF - ~$40
- [ ] Pi Cameras ×2 - ~$40
- [ ] 3S 5000mAh LiPo - ~$30
- [ ] Total estimate: ~$295

**PHASE 3 COMPLETE when:** Money ready. Parts ordered. Simulation validated.

---

## THE GOLDEN RULE

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   SIMULATION FIRST → CAD DESIGN → VERIFY PRINT → ORDER HW  │
│        ↓              ↓           ↓           ↓            │
│     4 weeks        4 weeks     1 week      1 week          │
│                                                             │
│   Total: 9 weeks minimum before touching real hardware    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Why?** A $20 motor mistake in CAD = redesign. A $30 motor mistake in real life = lost time, lost money, frustration.

---

## WHERE TO GET STUCK

| Problem | Resource |
|---------|----------|
| Gazebo won't launch | `simulation/docs/SIMULATION_GUIDE.md` |
| URDF questions | docs.ros.org/en/jazzy/Tutorials/URDF/ |
| Fusion 360 tutorial | youtube.com/@AutodeskFusion360 |
| Nav2 issues | navigation.ros.org/ |
| ROS2 in general | answers.ros.org |

---

## YOUR NEXT 3 ACTIONS (Do Now)

1. **Try to launch Gazebo** - `ros2 launch advika_sim sim_bringup.launch.py`
2. **Read SIMULATION_GUIDE.md** - `docs/SIMULATION_GUIDE.md`
3. **Join the Discord/Forum** - Link in repo if available

---

*Simulation validates. Design perfects. Hardware is the reward.*