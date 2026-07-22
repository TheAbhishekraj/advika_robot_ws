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

- [Quick Start](#quick-start)
- [System Architecture](#system-architecture)
- [Hardware](#hardware)
- [Simulation](#simulation)
- [Safety](#safety)
- [HITL -- Human-in-the-Loop](#hitl--human-in-the-loop)
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

### Simulation (No Hardware Required)

```bash
# Launch full simulation stack
ros2 launch advika_sim sim_bringup.launch.py

# Open HITL dashboard
# http://localhost:8080

# Run automated test scenarios
python3 simulation/scripts/run_scenario.py --all
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

See [SIMULATION_GUIDE.md](simulation/docs/SIMULATION_GUIDE.md) for full details.

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
```

---

## Language Breakdown

| Language | Files | Purpose |
|----------|-------|---------|
| **C++** | `main.cpp`, `safety_interrupt.h` | ESP32 firmware (motor control, safety ISR) |
| **Python** | `hardware_bridge.py`, `vision_bridge.py`, `hitl_bridge.py`, `sim_mcp_bridge.py`, `safety_monitor.py`, `run_scenario.py`, `test_peripherals.py` | MCP servers, HITL, simulation, diagnostics |
| **Bash** | `launch_robot.sh` | Service orchestration |
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
