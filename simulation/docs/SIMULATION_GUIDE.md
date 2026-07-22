# Advika 3.0 Simulation Guide -- Complete Setup & HITL Tutorial

> **Run Advika 3.0 in Gazebo simulation before deploying to physical hardware.**  
> This guide covers Gazebo Harmonic, ROS2 Jazzy, Navigation2, SLAM, and Human-in-the-Loop (HITL) testing.

---

## Table of Contents

1. [Why Simulate?](#why-simulate)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Simulation Architecture](#simulation-architecture)
6. [HITL -- Human-in-the-Loop](#hitl-human-in-the-loop)
7. [Running Scenarios](#running-scenarios)
8. [Troubleshooting](#troubleshooting)
9. [From Sim to Real](#from-sim-to-real)

---

## Why Simulate?

**Simulation-first robotics development** is the gold standard for autonomous mobile robots (AMRs). Before running Advika on physical hardware, validate everything in simulation:

| Benefit | Description |
|---------|-------------|
| 🛡️ **Safety** | Test collision avoidance without damaging hardware or surroundings |
| 💰 **Cost** | No battery wear, no broken parts, no replacement motors |
| ⚡ **Speed** | Run 100x scenarios in the time it takes to run 1 physical test |
| 🔁 **Repeatability** | Identical starting conditions for every test run |
| 🧪 **Edge Cases** | Test impossible physical scenarios (sudden obstacles, sensor failure) |
| 👨‍👩‍👧 **HITL** | Train human operators safely before real-world deployment |
| 🧒 **Education** | Let kids interact with the robot without physical risk |

> **Rule of thumb:** If it doesn't work in simulation, it won't work on hardware.

---

## Prerequisites

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 4 cores (Intel i5 / AMD Ryzen 5) | 8+ cores (Intel i7 / AMD Ryzen 7) |
| RAM | 8 GB | 16 GB |
| GPU | Integrated (Intel UHD) | Dedicated (NVIDIA GTX 1060+) |
| Storage | 20 GB free | 50 GB SSD |
| OS | Ubuntu 24.04 LTS | Ubuntu 24.04 LTS |

### Software Requirements

```bash
# ROS2 Jazzy Jalisco
sudo apt install ros-jazzy-desktop ros-jazzy-navigation2 ros-jazzy-nav2-bringup

# Gazebo Harmonic
sudo apt install ros-jazzy-ros-gz ros-jazzy-gz-ros2-control

# Python dependencies
pip3 install fastapi uvicorn websockets opencv-python numpy

# SLAM Toolbox
sudo apt install ros-jazzy-slam-toolbox

# Teleoperation
sudo apt install ros-jazzy-teleop-twist-keyboard
```

### Verify Installation

```bash
# Check ROS2
ros2 --version

# Check Gazebo
gz sim --version

# Check Navigation2
ros2 pkg list | grep nav2
```

---

## Installation

### 1. Clone the Workspace

```bash
cd ~/
git clone https://github.com/your-org/advika_robot_ws.git
cd advika_robot_ws
```

### 2. Build Simulation Package

```bash
# Create a ROS2 package for simulation
mkdir -p src/advika_sim
cp -r simulation/* src/advika_sim/

# Build
colcon build --packages-select advika_sim --symlink-install
source install/setup.bash
```

### 3. Set Environment Variables

Add to your `~/.bashrc`:

```bash
# Advika Simulation
export ADVIKA_WS="$HOME/advika_robot_ws"
export GZ_SIM_RESOURCE_PATH="$ADVIKA_WS/simulation/gazebo_worlds:$GZ_SIM_RESOURCE_PATH"
export PYTHONPATH="$ADVIKA_WS/simulation/scripts:$PYTHONPATH"
```

---

## Quick Start

### Launch Full Simulation Stack

```bash
# Terminal 1: Launch everything
ros2 launch advika_sim sim_bringup.launch.py

# This starts:
# - Gazebo with advika_playground.world
# - Robot State Publisher
# - ROS-Gazebo Bridge
# - RViz visualization
# - SLAM Toolbox
# - Navigation2
# - Teleop keyboard control
# - Safety Monitor
# - HITL Web Server (port 8080)
```

### Manual Control

```bash
# Terminal 2: Keyboard teleop (if not auto-launched)
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/advika/cmd_vel

# Controls:
#   i - Forward    k - Stop    , - Backward
#   j - Turn Left  l - Turn Right
#   q/z - Increase/decrease speed
#   w/x - Increase/decrease turn rate
```

### Open HITL Dashboard

```bash
# Open in browser:
# http://localhost:8080

# Features:
# - Real-time camera feed
# - LiDAR visualization
# - Telemetry dashboard
# - Mode switching (Auto/Supervised/Manual/Emergency)
# - Action approval queue
# - Safety event log
# - Manual drive controls
```

---

## Simulation Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ADVIKA 3.0 SIMULATION STACK                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌─────────────────┐     ┌──────────────────┐         │
│  │   HITL Web   │     │   AI Agent      │     │   Keyboard       │         │
│  │   Dashboard  │◄───►│   (MCP Client)  │     │   Teleop         │         │
│  │   :8080      │     │                 │     │                  │         │
│  └──────────────┘     └────────┬────────┘     └────────┬─────────┘         │
│                                │                       │                    │
│                                ▼                       ▼                    │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    MCP PROTOCOL (JSON-RPC 2.0)                       │   │
│  │                                                                      │   │
│  │  mcp_esp32_drive()  mcp_get_spatial_telemetry()  mcp_stop_motors()  │   │
│  │  mcp_speak_message()  mcp_capture_stitched_frame()                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                │                                            │
│                                ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │              SIMULATION MCP BRIDGE (sim_mcp_bridge.py)               │   │
│  │                                                                      │   │
│  │  • Subscribes to: /advika/scan, /advika/odom, /advika/camera        │   │
│  │  • Publishes to:  /advika/cmd_vel                                    │   │
│  │  • Maintains identical API to hardware MCP servers                   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                │                                            │
│              ┌─────────────────┼─────────────────┐                         │
│              ▼                 ▼                 ▼                         │
│  ┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐               │
│  │  Safety Monitor │  │  HITL Bridge │  │  ROS-Gazebo     │               │
│  │  (safety_monitor)│  │  (hitl_bridge)│  │  Bridge         │               │
│  │                 │  │              │  │                 │               │
│  │  • Collision    │  │  • Human     │  │  • cmd_vel      │               │
│  │    detection    │  │    approval  │  │  • scan         │               │
│  │  • Auto-stop    │  │  • Override  │  │  • camera       │               │
│  │  • Recovery     │  │  • Telemetry │  │  • odometry     │               │
│  └─────────────────┘  └──────────────┘  └─────────────────┘               │
│                                │                                            │
│                                ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         GAZEBO HARMONIC                              │   │
│  │                                                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │  Physics │  │  LiDAR   │  │  Cameras │  │  IMU     │           │   │
│  │  │  Engine  │  │  Plugin  │  │  Plugins │  │  Plugin  │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │              advika.urdf (Differential Drive)                 │   │   │
│  │  │  • Base link, wheels, caster, LiDAR, cameras, ToF, IMU      │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  │                                                                      │   │
│  │  ┌──────────────────────────────────────────────────────────────┐   │   │
│  │  │         advika_playground.world (Room with obstacles)         │   │   │
│  │  │  • Walls, table, sofa, bookshelf, cones, blocks, ramp       │   │   │
│  │  └──────────────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                │                                            │
│                                ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                    ROS2 JAZZY NAVIGATION STACK                       │   │
│  │                                                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │   │
│  │  │  AMCL    │  │  Nav2    │  │  SLAM    │  │  Planner │           │   │
│  │  │          │  │  Controller│  │  Toolbox │  │  Server  │           │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │   │
│  │                                                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                        │   │
│  │  │  Global  │  │  Local   │  │  Recovery│                        │   │
│  │  │  Costmap │  │  Costmap │  │  Server  │                        │   │
│  │  └──────────┘  └──────────┘  └──────────┘                        │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## HITL -- Human-in-the-Loop

### What is HITL?

**Human-in-the-Loop (HITL)** is a control paradigm where a human operator maintains oversight of an AI agent's decisions. The human can:

- **Approve** AI-proposed actions before execution
- **Reject** unsafe or incorrect actions
- **Override** AI control with manual commands
- **Monitor** real-time sensor data and telemetry
- **Trigger emergency stops** instantly

### HITL Operating Modes

| Mode | AI Control | Human Role | Use Case |
|------|-----------|-----------|----------|
| **FULL_AUTO** | 100% | Monitor only | Confident, low-risk environments |
| **SUPERVISED** | Proposes | Approves/rejects each step | New environments, testing |
| **MANUAL** | Suggests | Human executes | Training, debugging, demos |
| **EMERGENCY** | 0% | Full control | Safety incidents, system faults |

### HITL Workflow

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   AI AGENT  │────►│  HITL MANAGER   │────►│  HUMAN OPERATOR │
│  Proposes   │     │  Queues action  │     │  Reviews &      │
│  action     │     │  for approval   │     │  decides        │
└─────────────┘     └─────────────────┘     └─────────────────┘
                            │                         │
                            ▼                         ▼
                     ┌─────────────────┐     ┌─────────────────┐
                     │  APPROVED       │     │  REJECTED       │
                     │  → Execute      │     │  → Cancel       │
                     │  → Log decision │     │  → Notify AI    │
                     └─────────────────┘     └─────────────────┘
```

### Launching HITL

```bash
# HITL is auto-launched with sim_bringup.launch.py
# Access dashboard at: http://localhost:8080

# Or launch HITL standalone:
ros2 run advika_sim hitl_bridge --ros-args -p port:=8080

# Launch web server only:
python3 simulation/hitl/hitl_bridge.py --web

# Launch both ROS node and web server:
python3 simulation/hitl/hitl_bridge.py --both
```

### HITL API Endpoints

```bash
# Get status
curl http://localhost:8080/api/status

# Get pending actions
curl http://localhost:8080/api/pending_actions

# Approve an action
curl -X POST http://localhost:8080/api/approve/act_1234567890_0

# Reject an action
curl -X POST http://localhost:8080/api/reject/act_1234567890_0

# Change mode
curl -X POST http://localhost:8080/api/mode/supervised

# Emergency stop
curl -X POST http://localhost:8080/api/emergency_stop

# Manual drive
curl -X POST "http://localhost:8080/api/manual_drive?linear=0.3&angular=0.0"

# Get telemetry
curl http://localhost:8080/api/telemetry?limit=10

# Get safety events
curl http://localhost:8080/api/safety_events?limit=20
```

### WebSocket Real-Time Updates

Connect to `ws://localhost:8080/ws` for real-time:
- Action requests (when AI proposes an action)
- Action updates (when human approves/rejects)
- Safety alerts (collision warnings, obstacles)
- Telemetry snapshots (10Hz)

---

## Running Scenarios

### Scenario 1: Basic Navigation

```bash
# Launch simulation
ros2 launch advika_sim sim_bringup.launch.py

# In RViz, use "2D Goal Pose" tool to click a destination
# Watch Advika navigate autonomously
```

### Scenario 2: Find the Red Cone

```bash
# Launch with object detection
ros2 launch advika_sim sim_bringup.launch.py detect_objects:=true

# In HITL dashboard, send command:
# "Advika, find the red cone and stop 30cm in front of it"
# Watch AI propose actions, approve each step in the dashboard
```

### Scenario 3: Obstacle Avoidance Test

```bash
# Place obstacles in Gazebo
# Drive toward obstacle using teleop
# Watch safety monitor trigger auto-stop and recovery
```

### Scenario 4: SLAM Mapping

```bash
# Launch with SLAM only (no Nav2)
ros2 launch advika_sim sim_bringup.launch.py use_nav2:=false

# Drive around the room manually
# Watch map build in RViz
# Save map:
ros2 run nav2_map_server map_saver_cli -f my_room_map
```

### Scenario 5: HITL Supervised Mode

```bash
# Set HITL mode to SUPERVISED via dashboard
# Give AI a complex goal
# Approve/reject each proposed action
# Observe how AI adapts to rejections
```

### Scenario 6: Emergency Stop Drill

```bash
# Drive robot toward wall
# Press E-Stop in dashboard or physical button
# Verify immediate stop and recovery procedure
```

---

## Troubleshooting

### Gazebo Won't Start

```bash
# Check Gazebo installation
gz sim --version

# Try software rendering
export LIBGL_ALWAYS_SOFTWARE=1
ros2 launch advika_sim sim_bringup.launch.py

# Check for conflicting Gazebo versions
sudo apt remove ignition-gazebo3  # Remove old Ignition if present
```

### Robot Doesn't Move

```bash
# Check cmd_vel is being published
ros2 topic echo /advika/cmd_vel

# Check odometry is being published
ros2 topic echo /advika/odom

# Check Gazebo bridge is running
ros2 node list | grep bridge

# Restart bridge manually
ros2 run ros_gz_bridge parameter_bridge /advika/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

### LiDAR Not Visible

```bash
# Check scan topic
ros2 topic echo /advika/scan

# Check in RViz: Add LaserScan display, topic /advika/scan
# Set fixed frame to "lidar_link" or "base_link"
```

### HITL Dashboard Not Loading

```bash
# Check if server is running
curl http://localhost:8080/api/status

# Check port availability
sudo lsof -i :8080

# Launch standalone
python3 simulation/hitl/hitl_bridge.py --web
```

### Navigation Fails

```bash
# Check costmaps are publishing
ros2 topic echo /global_costmap/costmap

# Check AMCL has localization
ros2 topic echo /amcl_pose

# Reset localization
ros2 service call /reinitialize_global_localization std_srvs/srv/Empty
```

---

## From Sim to Real

### Code Compatibility

The simulation uses **identical MCP APIs** to the physical robot:

| MCP Tool | Simulation | Hardware | Notes |
|----------|-----------|----------|-------|
| `mcp_esp32_drive()` | Publishes cmd_vel | Sends UART to ESP32 | Same parameters |
| `mcp_get_spatial_telemetry()` | Reads Gazebo sensors | Reads real sensors | Same return format |
| `mcp_stop_motors()` | Publishes zero cmd_vel | Sends stop command | Same API |
| `mcp_speak_message()` | Logs to console | Runs espeak-ng | Same API |
| `mcp_capture_stitched_frame()` | Captures Gazebo camera | Captures real cameras | Same return format |

### Migration Checklist

```
□ Simulation tests pass (all scenarios green)
□ HITL supervised mode tested for 10+ missions
□ Safety monitor triggers correctly in all edge cases
□ SLAM map quality verified
□ Navigation paths are collision-free
□ Recovery procedures tested
□ Battery monitoring calibrated
□ Physical E-Stop button tested
□ All sensors calibrated (LiDAR, ToF, cameras, IMU)
□ Motor PID tuned for load
□ Wireless connectivity stable
□ Logging and telemetry verified
```

### Hardware Bringup

```bash
# 1. Flash ESP32 firmware
cd firmware/esp32_motor_bridge
pio run --target upload

# 2. Run hardware diagnostics
python3 scripts/test_peripherals.py

# 3. Start MCP servers
python3 mcp_servers/hardware_bridge.py &
python3 mcp_servers/vision_bridge.py &

# 4. Test with same AI agent that passed simulation
# The agent code is IDENTICAL -- just change MCP server endpoints
```

---

## Advanced Topics

### Custom Worlds

Create new `.world` files in `simulation/gazebo_worlds/`:

```xml
<model name="my_custom_obstacle">
  <static>true</static>
  <pose>x y z roll pitch yaw</pose>
  <link name="link">
    <collision><geometry><box><size>w h d</size></box></geometry></collision>
    <visual><geometry><box><size>w h d</size></box></geometry></visual>
  </link>
</model>
```

### Sensor Noise Tuning

Edit URDF sensor plugins to match real sensor characteristics:

```xml
<noise>
  <type>gaussian</type>
  <mean>0.0</mean>
  <stddev>0.01</stddev>  <!-- Match real LiDAR noise -->
</noise>
```

### Multi-Robot Simulation

Launch multiple Advika instances with different namespaces:

```bash
ros2 launch advika_sim sim_bringup.launch.py namespace:=advika_1 x:=0.0 y:=0.0
ros2 launch advika_sim sim_bringup.launch.py namespace:=advika_2 x:=2.0 y:=0.0
```

---

## Resources

- [Gazebo Harmonic Documentation](https://gazebosim.org/docs/harmonic)
- [ROS2 Jazzy Documentation](https://docs.ros.org/en/jazzy/)
- [Navigation2 Tutorials](https://navigation.ros.org/)
- [SLAM Toolbox Wiki](https://github.com/SteveMacenski/slam_toolbox)
- [Advika GitHub Repository](https://github.com/your-org/advika_robot_ws)

---

*Simulation is not a substitute for reality -- but it's the best way to get there safely.* 🤖🌍
