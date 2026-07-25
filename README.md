# Advika 3.0 -- Agentic Autonomous Mobile Robot

[![ROS2](https://img.shields.io/badge/ROS2-Jazzy-blue)](https://docs.ros.org/en/jazzy/)
[![Gazebo](https://img.shields.io/badge/Gazebo-Harmonic-orange)](https://gazebosim.org/)
[![Platform](https://img.shields.io/badge/Platform-ARM64-green)](https://www.raspberrypi.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![HITL](https://img.shields.io/badge/HITL-Enabled-red)](simulation/docs/SIMULATION_GUIDE.md)

> **Advika** (Sanskrit: अद्विका) -- "Unique, unparalleled."  
> A ROS2 Jazzy-based, LLM-orchestrated AMR running on Raspberry Pi 4/5 with ESP32 motor bridge, dual-camera vision, LD06 LiDAR, and 8x8 ToF depth sensing.

<p align="center">
  <img src="docs/advika_render.png" alt="Advika 3.0 Robot" width="600"/>
</p>

---

## Table of Contents

- [Setup & Master Guide](SETUP.md)
- [Quick Start](#quick-start)
- [System Architecture](#system-architecture)
- [Hardware](#hardware)
- [Simulation](#simulation)
- [Safety](#safety)
- [HITL -- Human-in-the-Loop](#hitl--human-in-the-loop)
- [CAD Design](#cad-design)
- [Furniture Design](#furniture-design)
- [Mentorship Program](#mentorship-program)
- [I am 5 -- Child Manual](#i-am-5--child-friendly-robot-manual)
- [File Structure](#file-structure)
- [Contributing](#contributing)

---

## Quick Start

### Hardware (Physical Robot)

```bash
# 1. Flash ESP32 firmware
cd firmware/esp32_motor_bridge
pio run --target upload

# 2. Test all peripherals
python3 scripts/test_peripherals.py

# 3. Start MCP servers
python3 mcp_servers/hardware_bridge.py &
python3 mcp_servers/vision_bridge.py &

# 4. Launch robot
bash scripts/launch_robot.sh start
```

### Simulation & CAD Workspace Setup (Step-by-Step Flow)

> 🔴 **Full Step-by-Step Guide:** See [SETUP.md](SETUP.md) for detailed instructions.

```bash
# Step 1 — Clone the repo
git clone https://github.com/TheAbhishekraj/advika_robot_ws.git
cd advika_robot_ws

# Step 2 — Check system prerequisites (Ubuntu 24.04, ROS2 Jazzy, Gazebo Harmonic, Python)
bash scripts/verify_prerequisites.sh

# Step 3 — Automatically Generate World-Class CAD Models (STLs & STEP)
bash src/advika_cad/scripts/install_and_generate.sh

# Step 4 — Inject CAD STLs directly into the ROS2 URDF
python3 scripts/update_urdf.py

# Step 5 — Build the workspace (now includes the generated meshes!)
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select advika_cad advika_description advika_sim
source install/setup.bash

# Step 6 — Launch full simulation stack in the 3BHK Environment
ros2 launch advika_sim sim_bringup.launch.py world_file:=3bhk_house.world
```

---

## System Architecture

```
+------------------+     +------------------+     +------------------+
|   AI Agent Core  |<--->|  MCP Protocol    |<--->| Hardware Bridge  |
|  (Claude/GPT-4)  |     |  JSON-RPC 2.0    |     |  ESP32 + Sensors |
+------------------+     +------------------+     +------------------+
         |                                              |
         v                                              v
+------------------+                           +------------------+
|  ROS2 Jazzy      |                           |  JGA25 Motors    |
|  Navigation2     |                           |  LD06 LiDAR      |
|  SLAM Toolbox    |                           |  VL53L5CX ToF    |
+------------------+                           |  Dual Cameras    |
         |                                      +------------------+
         v
+------------------+
|  Raspberry Pi 5  |
|  Ubuntu 24.04    |
+------------------+
```

---

## Hardware

| Component | Model | Specs |
|-----------|-------|-------|
| Compute | Raspberry Pi 5 | 8GB RAM, ARM64 |
| Motor Controller | ESP32-S3 | Dual PID, encoder feedback |
| Motors | JGA25-370 | 170 RPM, 334 PPR encoders |
| LiDAR | LD06 | 360 deg, 12m range, 10Hz |
| Depth Sensor | VL53L5CX | 8x8 ToF array, 4m range |
| Cameras | Dual USB | Horizon 75deg + Floor 120deg |
| Battery | 3S LiPo | 5000mAh, BMS monitored |
| Display | SSD1306 | 128x64 OLED status indicator |

---

## Simulation

Full Gazebo Harmonic simulation with identical MCP APIs to hardware:

| Feature | Description |
|---------|-------------|
| **Gazebo World** | 10m x 10m indoor playground with furniture, cones, obstacles |
| **URDF Model** | Complete robot with differential drive, all sensors |
| **Nav2** | Autonomous navigation with global/local costmaps |
| **SLAM** | Real-time mapping with SLAM Toolbox |
| **MCP Bridge** | Same API as hardware -- zero code changes |
| **Scenarios** | 5 built-in automated test scenarios |

### Quick Start Commands

```bash
# Verify prerequisites first
bash ~/advika_robot_ws/scripts/verify_prerequisites.sh

# Source environment
source /opt/ros/jazzy/setup.bash
source ~/advika_robot_ws/install/setup.bash

# Launch simulation
ros2 launch advika_sim sim_bringup.launch.py

# With Navigation2
ros2 launch advika_sim sim_bringup.launch.py use_nav2:=true

# With HITL dashboard
ros2 launch advika_sim sim_bringup.launch.py use_hitl:=true
```

### Key Simulation Documents

| Priority | Document | Purpose |
|----------|----------|---------|
| 🔴 **High** | [SETUP.md](SETUP.md) | **Start Here:** Step 1–5 workspace setup & phase-by-phase curriculum |
| 🔴 **High** | [PREREQUISITES_CHECK.md](docs/PREREQUISITES_CHECK.md) | System requirements & verification check sheet |
| 🟡 **Medium** | [SIMULATION_MASTER_GUIDE.md](docs/SIMULATION_MASTER_GUIDE.md) | Complete 9-week learning path & sensor tuning |
| 🟡 **Medium** | [COMMANDS_REFERENCE.md](docs/COMMANDS_REFERENCE.md) | All terminal commands in one place |
| 🟡 **Medium** | [SIMULATION_FIRST_CHECKLIST.md](docs/SIMULATION_FIRST_CHECKLIST.md) | Milestone verification checklist |
| ⚪ **Audit** | [AUDIT_CHECKLIST.md](docs/AUDIT_CHECKLIST.md) | External review / third-party audit |

> ✅ **Verified 2026-07-25:** Ubuntu 24.04 · ROS2 Jazzy · Gazebo Harmonic 8.11.0 · All Python packages · Workspace built — all checks passed.

See [simulation/docs/SIMULATION_GUIDE.md](simulation/docs/SIMULATION_GUIDE.md) for full details.

---

## 🏠 3BHK Indoor World

Advika 3.0 now includes a fully furnished 3 Bedroom Hall Kitchen (3BHK) indoor environment for realistic navigation testing.

### House Layout
- **Living Room**: 6.0m × 4.5m with sofa, coffee table, TV unit
- **Kitchen**: 3.6m × 3.0m with dining table and chairs
- **Master Bedroom**: 4.5m × 3.6m with bed and nightstand
- **Bedroom 2**: 3.6m × 3.0m with bed
- **Bedroom 3**: 3.6m × 3.0m with desk and chair
- **Hallway**: 0.6m wide connecting all rooms
- **Bathrooms**: 2.4m × 1.8m each (2 total)

### Launch 3BHK Simulation
```bash
ros2 launch advika_sim sim_bringup.launch.py
```

This launches:
- Gazebo with the 3BHK house
- Advika robot in the living room
- RViz with complete sensor visualization
- LiDAR, cameras, and IMU streaming

### Screenshots
![3BHK House](docs/images/3bhk_house.png)
![Robot in Living Room](docs/images/robot_living_room.png)

---

## Safety

Advika implements a **multi-layer safety system**:

1. **Hardware E-Stop** -- Physical button triggers ESP32 ISR (< 1ms response)
2. **Software Safety Monitor** -- Independent collision detection and auto-stop
3. **MCP Safety Limits** -- All drive commands clamped to safe ranges
4. **HITL Oversight** -- Human approval for AI actions in supervised mode
5. **Audit Logging** -- Every decision logged to `/var/log/advika/decisions.jsonl`

> **Never leave Advika running unattended with motors armed.**

---

## HITL -- Human-in-the-Loop

Real-time web dashboard for human oversight of AI decisions:

| Mode | AI Control | Human Role |
|------|-----------|-----------|
| **FULL_AUTO** | 100% | Monitor only |
| **SUPERVISED** | Proposes | Approve/reject each step |
| **MANUAL** | Suggests | Human executes everything |
| **EMERGENCY** | Suspended | Full human control |

**Dashboard:** `http://localhost:8080`

Features: Live camera, LiDAR viz, telemetry, action queue, safety log, manual controls

---

## CAD Design

Advika 3.0 includes Fusion 360-compatible CAD files for 3D printing custom components.

### Available Components

| Component | Material | Status | Priority |
|-----------|----------|--------|----------|
| Chassis Base v3 | PETG | ⚠️ Design needed | HIGH |
| Wheel Hubs (×2) | PETG | ⚠️ Design needed | HIGH |
| LiDAR Tower | PETG | ⚠️ Design needed | HIGH |
| Top Dome | PETG | ⚠️ Design needed | HIGH |
| Motor Mounts | PETG | ⚠️ Design needed | MEDIUM |
| Battery Tray | PETG | ⚠️ Design needed | MEDIUM |
| Camera Bracket | PETG | ⚠️ Design needed | MEDIUM |
| ToF Holder | PETG | ⚠️ Design needed | MEDIUM |
| Bumpers | TPU 95A | ⚠️ Design needed | MEDIUM |

### CAD Workflow

1. Open [FUSION360_WORKFLOW.md](docs/FUSION360_WORKFLOW.md) for design specifications
2. Export STL files to `src/advika_cad/meshes/`
3. Export STEP files to `src/advika_cad/step/`
4. Update URDF with mesh references (see [MESH_EXPORT_GUIDE.md](docs/MESH_EXPORT_GUIDE.md))

### Directory Structure

```
src/advika_cad/
├── meshes/           # STL files for 3D printing
├── step/             # STEP files for mechanical design
├── fusion360/        # Fusion 360 project files
└── advika_cad/       # ROS2 package
```

### Print Settings

| Material | Nozzle | Layer Height | Infill | Perimeters |
|----------|--------|--------------|--------|------------|
| PETG | 0.4mm | 0.2mm | 30-50% | 3-4 |
| TPU 95A | 0.4mm | 0.24mm | 20% | 3 |

---

## Furniture Design

Custom furniture models for realistic indoor simulation in the 3BHK world.

### Living Room
- Sofa (3-seater + 2-seater) - 2200×900×800mm
- Coffee Table - 1200×600×400mm (glass top)
- TV Unit - 1800×450×1200mm
- Floor Lamp - 1600mm height

### Kitchen
- L-Shaped Counter - 2400×600×900mm
- Dining Table - 1500×900×750mm (seats 6)
- Dining Chairs (×4)
- Refrigerator - 700×700×1800mm

### Bedrooms
- Double Bed (Master) - 2000×1800mm mattress
- Single Beds (×2) - 1900×900mm mattress
- Wardrobes, Study Desks, Bookshelf

### Documentation

See [3BHK_FURNITURE_SPEC.md](docs/3BHK_FURNITURE_SPEC.md) for complete dimensions, materials, and Gazebo placement coordinates.

---

## Mentorship Program

Follow this structured path to complete simulation and CAD design BEFORE hardware.

### Your Learning Path

```
Phase 1: SIMULATION MASTER (Weeks 1-4)
├── Week 1: Get Gazebo running, drive robot
├── Week 2: URDF deep dive, modify robot
├── Week 3: Navigate 3BHK world with Nav2
└── Week 4: Get HITL dashboard working

Phase 2: DESIGN FLUENCY (Weeks 5-8)
├── Week 5: Learn Fusion 360 basics
├── Week 6: Design wheel hub
├── Week 7: Design chassis base
└── Week 8: Design remaining components

Phase 3: HARDWARE PREP (Week 9+)
├── Create Bill of Materials
├── Find print service or buy printer
└── Order electronic components
```

### Key Documents

| Document | Purpose |
|----------|---------|
| [MENTORSHIP_GUIDE.md](docs/MENTORSHIP_GUIDE.md) | Full 9-week curriculum |
| [SIMULATION_FIRST_CHECKLIST.md](docs/SIMULATION_FIRST_CHECKLIST.md) | Week-by-week checklist |
| [FUSION360_WORKFLOW.md](docs/FUSION360_WORKFLOW.md) | CAD design specs |

### Graduation Requirements

Before buying hardware, you must demonstrate:
- ✅ Robot navigates 3BHK autonomously
- ✅ All 9 STL files designed and printed
- ✅ URDF updated with real meshes
- ✅ Bill of Materials completed

**Remember:** Simulation validates. Design perfects. Hardware is the reward.

---

## I am 5 -- Child-Friendly Robot Manual

A complete guide for children ages 5+ to safely interact with Advika:

- **Meet Advika!** -- What the robot is, what it can do, personality
- **Safety Rules** -- Golden rules, traffic light system, play area checklist
- **Fun Commands** -- Spoken commands, games, challenges, secret codes
- **Sticker Sheet** -- Printable robot alphabet, coloring pages, achievement badges

See [manuals/i_am_5/](manuals/i_am_5/) for all chapters.

---

## File Structure

```
advika_robot_ws/
|-- CLAUDE.md                          # Master system prompt (Advika identity)
|-- README.md                          # This file
|-- LICENSE                            # MIT License
|-- .gitignore                         # Git ignore rules
|
|-- config/
|   |-- opencode_config.json           # CLI agent configuration
|   |-- robot_params.yaml              # Hardware parameters & safety limits
|
|-- firmware/
|   |-- esp32_motor_bridge/
|   |   |-- platformio.ini             # ESP32 build config
|   |   |-- src/
|   |   |   |-- main.cpp             # Dual PID motor control
|   |   |   |-- safety_interrupt.h   # Hardware E-Stop ISR
|
|-- mcp_servers/
|   |-- __init__.py
|   |-- hardware_bridge.py             # ESP32/sensors MCP server
|   |-- vision_bridge.py               # OpenCV/YOLO vision MCP server
|
|-- scripts/
|   |-- launch_robot.sh                # Auto-start daemon
|   |-- test_peripherals.py            # Hardware diagnostics (9 tests)
|   |-- verify_prerequisites.sh        # ✅ Environment verification script
|   |-- setup_advika.sh                # First-time workspace setup
|   |-- auto_sim.py                    # Automated simulation runner
|
|-- manuals/
|   |-- i_am_5/                        # Child-friendly robot manual
|   |   |-- README.md
|   |   |-- cover.md
|   |   |-- meet_advika.md
|   |   |-- safety_rules.md
|   |   |-- fun_commands.md
|   |   |-- sticker_sheet.md
|
|-- docs/
|   |-- CAD_README.md                  # 3D chassis print guide
|   |-- Wiring_README.md               # Electrical schematic docs
|   |-- FUSION360_WORKFLOW.md          # Fusion 360 design workflow
|   |-- 3BHK_FURNITURE_SPEC.md         # Furniture dimensions/materials
|   |-- MESH_EXPORT_GUIDE.md           # STL/DAE/URDF export guide
|   |-- fusion360/                     # Fusion 360 documentation
|   |-- furniture/                    # Furniture design docs
|   |-- images/                       # Screenshots and renders
|   |-- reports/                      # Audit reports
|
|-- simulation/                          # FULL SIMULATION SUITE
|   |-- urdf/
|   |   |-- advika.urdf                # Complete robot URDF
|   |-- gazebo_worlds/
|   |   |-- advika_playground.world    # Test environment
|   |-- launch/
|   |   |-- sim_bringup.launch.py      # Complete sim bringup
|   |-- config/
|   |   |-- nav2_params.yaml           # Navigation2 config
|   |   |-- slam_params.yaml           # SLAM Toolbox config
|   |   |-- advika_sim.rviz            # RViz layout
|   |-- scripts/
|   |   |-- sim_mcp_bridge.py          # MCP-to-sim bridge
|   |   |-- safety_monitor.py          # Sim safety monitor
|   |   |-- run_scenario.py            # Automated test scenarios
|   |-- hitl/
|   |   |-- __init__.py
|   |   |-- hitl_bridge.py             # HITL WebSocket bridge
|   |   |-- web_interface/
|   |   |   |-- static/
|   |   |   |   |-- style.css
|   |   |   |-- templates/
|   |   |   |   |-- dashboard.html     # Real-time HITL dashboard
|   |-- docs/
|   |   |-- SIMULATION_GUIDE.md        # Complete sim tutorial
|
|-- src/
|   |-- advika_bringup/               # Robot bringup launch files
|   |-- advika_description/           # URDF and mesh assets
|   |-- advika_cad/                   # 3D CAD files for printing
|   |   |-- meshes/                   # STL files for 3D printing
|   |   |-- step/                     # STEP files for mechanical
|   |   |-- fusion360/                # Fusion 360 project files
|   |-- advika_sim/                   # Gazebo simulation
|   |   |-- worlds/                   # World files (3BHK, living_room, etc.)
|   |   |-- urdf/
|   |   |-- launch/
|   |   |-- config/
|   |   |-- scripts/
|   |   |-- hitl/
```

---

## Language Breakdown

| Language | Files | Purpose |
|----------|-------|---------|
| **C++** | `main.cpp`, `safety_interrupt.h` | ESP32 firmware (motor control, safety ISR) |
| **Python** | `hardware_bridge.py`, `vision_bridge.py`, `hitl_bridge.py`, `sim_mcp_bridge.py`, `safety_monitor.py`, `run_scenario.py`, `test_peripherals.py` | MCP servers, HITL, simulation, diagnostics |
| **Bash** | `launch_robot.sh`, `verify_prerequisites.sh`, `setup_advika.sh` | Service orchestration & environment setup |
| **YAML** | `robot_params.yaml`, `nav2_params.yaml`, `slam_params.yaml` | Configuration |
| **JSON** | `opencode_config.json` | Agent configuration |
| **XML/URDF** | `advika.urdf` | Robot model |
| **SDF** | `advika_playground.world` | Gazebo world |
| **HTML/CSS/JS** | `dashboard.html`, `style.css` | HITL web interface |
| **Markdown** | `CLAUDE.md`, `README.md`, `*.md` | Documentation |

---

## Contributing

Pull requests welcome! Please:
1. Open an issue first to discuss major changes
2. Follow existing code style
3. Test in simulation before hardware PRs
4. Update relevant documentation

---

## License

[MIT License](LICENSE) -- See file for details.

---

*Built with care by the Advika Robotics Team.*  
*Advika means "one of a kind" -- just like every builder who uses this project.*
