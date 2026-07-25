# 🚀 ADVIKA 3.0 MASTER SETUP & EXECUTION GUIDE

**Target OS:** Ubuntu 24.04 LTS | **ROS2:** Jazzy Jalisco | **Simulator:** Gazebo Harmonic (8.11.0+)

> 📌 **Note:** This document is mirrored at the repository root as [SETUP.md](../SETUP.md).

---

## 📌 MASTER ONBOARDING FLOW (STEPS 1–5)

Follow these 5 steps in exact sequence to set up, verify, and run the Advika 3.0 AMR simulation environment.

---

### Step 1: Clone the Repository (if not already cloned)

```bash
cd ~
git clone https://github.com/TheAbhishekraj/advika_robot_ws.git
cd advika_robot_ws
```

---

### Step 2: Pull Latest Changes

```bash
cd ~/advika_robot_ws
git pull origin main
```

---

### Step 3: Check System Prerequisites

Run the automated verification script. It will check OS version, disk space, RAM, CPU cores, ROS2 Jazzy, Gazebo Harmonic, and Python dependencies.

```bash
bash ~/advika_robot_ws/scripts/verify_prerequisites.sh
```

> **Note:** The script automatically sources ROS2 (`/opt/ros/jazzy/setup.bash`).
> All essential checks must show **✅ PASS** before proceeding.
> See [PREREQUISITES_CHECK.md](PREREQUISITES_CHECK.md) for full manual verification criteria.

---

### Step 4: Build the Workspace

```bash
# 1. Source ROS2 Jazzy
source /opt/ros/jazzy/setup.bash

# 2. Build workspace using colcon
cd ~/advika_robot_ws
colcon build --symlink-install

# 3. Source built workspace
source install/setup.bash
```

> **Pro Tip:** Add automatic sourcing to your `~/.bashrc` so you don't need to run it every time:
> ```bash
> echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
> echo "source ~/advika_robot_ws/install/setup.bash" >> ~/.bashrc
> source ~/.bashrc
> ```

---

### Step 5: Run First Simulation

Launch the complete simulation stack (Gazebo + RViz2 + Teleop Keyboard):

```bash
ros2 launch advika_sim sim_bringup.launch.py
```

**Expected Results:**
- 🟢 **Gazebo Harmonic Window**: Shows the Advika AMR model in the playground environment.
- 🟢 **RViz2 Window**: Displays 3D robot model, TF frame tree, and sensor visualizations.
- 🟢 **Teleop Terminal**: Active keyboard controls (`i` = forward, `,` = backward, `j`/`l` = turn, `k` = stop).

---

## 🗺️ PHASE-BY-PHASE MASTER LEARNING PATH

Once Steps 1–5 are complete, follow this 9-week master curriculum to validate simulation, master CAD design, and prepare for physical hardware.

```
┌─────────────────────────────────────────────────────────────┐
│   STEP 1–5 SETUP → PHASE 1 SIM → PHASE 2 CAD → PHASE 3 HW   │
│        ↓              ↓            ↓            ↓           │
│      Day 1         Weeks 1-4    Weeks 5-8    Week 9+        │
└─────────────────────────────────────────────────────────────┘
```

---

### 🟢 PHASE 1: SIMULATION MASTERY (Weeks 1–4)

*Goal: Verify robot navigation, SLAM mapping, and HITL dashboard before touching hardware.*

| Week | Target | Primary Action / Command | Key Document |
|------|--------|--------------------------|--------------|
| **Week 1** | Basic Bringup & Teleop | `ros2 launch advika_sim sim_bringup.launch.py` | [SIMULATION_MASTER_GUIDE.md](SIMULATION_MASTER_GUIDE.md) |
| **Week 2** | URDF & Sensor Inspection | Inspect `/advika/scan`, `/advika/odom`, `/advika/imu/data` | [PREREQUISITES_CHECK.md](PREREQUISITES_CHECK.md) |
| **Week 3** | 3BHK World Navigation & SLAM | `ros2 launch advika_sim sim_bringup.launch.py world_file:=3bhk_house.world use_nav2:=true` | [3BHK_SIMULATION.md](3BHK_SIMULATION.md) |
| **Week 4** | HITL Web Dashboard | `ros2 launch advika_sim sim_bringup.launch.py use_hitl:=true` → Visit `http://localhost:8080` | [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) |

---

### 🟡 PHASE 2: CAD DESIGN & VERIFICATION (Weeks 5–8)

*Goal: Design and 3D print all 9 custom chassis components.*

1. **Generate CAD Files**: Run `bash ~/advika_robot_ws/src/advika_cad/scripts/install_and_generate.sh`.
2. **View Assembly**: Import `src/advika_cad/step/advika30_assembly.step` into FreeCAD or Fusion 360.
3. **Print Custom Parts**: Follow [PRINT_SETTINGS.md](PRINT_SETTINGS.md) and print components.
4. **Export STLs** to `src/advika_cad/meshes/` (done automatically during generation).
5. **Update URDF** with new mesh files (Follow [MESH_EXPORT_GUIDE.md](MESH_EXPORT_GUIDE.md)).

---

### 🔴 PHASE 3: PRE-HARDWARE PREPARATION (Week 9+)

*Goal: BOM completion, parts ordering, physical assembly.*

1. Complete Bill of Materials check in [BOM.md](BOM.md).
2. Order electronics (Raspberry Pi 5 8GB, ESP32-S3, JGA25 motors, LD06 LiDAR, VL53L5CX ToF, Dual Cameras).
3. Assemble physical robot and flash ESP32 motor bridge firmware (`firmware/esp32_motor_bridge`).

---

## 📚 DOCUMENTATION DIRECTORY INDEX

| Priority | Document | Purpose |
|----------|----------|---------|
| 🔴 **High** | [SETUP.md](../SETUP.md) | **Master Setup Guide** — Complete step-by-step setup & execution path |
| 🔴 **High** | [PREREQUISITES_CHECK.md](PREREQUISITES_CHECK.md) | Detailed prerequisite check sheet with expected values |
| 🟡 **Medium** | [SIMULATION_MASTER_GUIDE.md](SIMULATION_MASTER_GUIDE.md) | 9-week simulation learning curriculum & sensor tuning |
| 🟡 **Medium** | [COMMANDS_REFERENCE.md](COMMANDS_REFERENCE.md) | Complete searchable command reference for all terminal tasks |
| 🟡 **Medium** | [SIMULATION_FIRST_CHECKLIST.md](SIMULATION_FIRST_CHECKLIST.md) | Milestone verification checklist for each phase |
| 🔵 **Low** | [TROUBLESHOOTING.md](../TROUBLESHOOTING.md) | Common errors and resolutions |

---

*Built with care by the Advika Robotics Team.*
