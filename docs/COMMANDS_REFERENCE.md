# ADVIKA 3.0 COMPLETE COMMAND REFERENCE

**Version:** 1.0 | **Date:** 2026-07-25
**All commands for: Ubuntu 24.04 + ROS2 Jazzy + Gazebo Harmonic

---

## 📚 COMMAND INDEX

1. [Setup & Installation](#1-setup--installation)
2. [Build & Workspace](#2-build--workspace)
3. [Launch Commands](#3-launch-commands)
4. [Teleop & Control](#4-teleop--control)
5. [Topic Commands](#5-topic-commands)
6. [Node Commands](#6-node-commands)
7. [Bag Recording](#7-bag-recording)
8. [RViz](#8-rviz)
9. [HITL Dashboard](#9-hitl-dashboard)
10. [Nav2 & SLAM](#10-nav2--slam)
11. [Gazebo](#11-gazebo)
12. [Build & Verification](#12-build--verification)
13. [TTS & Voice](#13-tts--voice)
14. [Utilities](#14-utilities)

---

## 1. SETUP & INSTALLATION

### Single Command Setup (First Time)
```bash
# Download and run automated setup
bash <(curl -fsSL https://raw.githubusercontent.com/TheAbhishekraj/advika_robot_ws/main/scripts/setup_advika.sh)

# Or with custom directory
bash <(curl -fsSL https://raw.githubusercontent.com/TheAbhishekraj/advika_robot_ws/main/scripts/setup_advika.sh) --dir /path/to/clone
```

### Manual Setup
```bash
# 1. Install system packages
sudo apt update
sudo apt install -y ros-jazzy-desktop ros-jazzy-navigation2 ros-jazzy-slam-toolbox ros-jazzy-ros-gz gz-harmonic

# 2. Install Python packages
pip3 install -r ~/advika_robot_ws/requirements.txt

# 3. Clone repository
cd ~
git clone https://github.com/TheAbhishekraj/advika_robot_ws.git
cd advika_robot_ws

# 4. Build
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install

# 5. Source workspace
source install/setup.bash
```

### Verify Prerequisites
```bash
# Run verification script
chmod +x ~/advika_robot_ws/scripts/setup_advika.sh
~/advika_robot_ws/scripts/setup_advika.sh --verify

# Or use the dedicated check
cat << 'EOF' | bash
#!/bin/bash
echo "Checking prerequisites..."
ros2 --version && gz sim --version && python3 -c "import fastapi" && echo "ALL OK"
EOF
```

---

## 2. BUILD & WORKSPACE

### Build Commands
```bash
# Full build with symlink install
colcon build --symlink-install

# Build specific package
colcon build --packages-select advika_sim

# Build with verbose output
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=DEBUG

# Clean and rebuild
rm -rf build/ install/ log/
colcon build --symlink-install

# Build up to package (don't continue on error)
colcon build --symlink-install --continue-on-error
```

### Workspace Sourcing
```bash
# Source ROS2 (add to ~/.bashrc)
source /opt/ros/jazzy/setup.bash

# Source workspace (add to ~/.bashrc)
source ~/advika_robot_ws/install/setup.bash

# Combined (for ~/.bashrc)
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
echo "source ~/advika_robot_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

---

## 3. LAUNCH COMMANDS

### Basic Launch
```bash
# Full simulation (Gazebo + RViz + Teleop)
ros2 launch advika_sim sim_bringup.launch.py

# With specific world
ros2 launch advika_sim sim_bringup.launch.py world_file:=3bhk_house.world

# Without RViz (headless-ish)
ros2 launch advika_sim sim_bringup.launch.py use_rviz:=false

# With Navigation2
ros2 launch advika_sim sim_bringup.launch.py use_nav2:=true

# With HITL dashboard
ros2 launch advika_sim sim_bringup.launch.py use_hitl:=true hitl_port:=8080

# All options enabled
ros2 launch advika_sim sim_bringup.launch.py use_nav2:=true use_hitl:=true
```

### Launch Arguments
```bash
# List all launch arguments
ros2 launch advika_sim sim_bringup.launch.py --show-args

# Arguments:
#   world_file    - World to load (default: advika_playground.world)
#   use_rviz     - Launch RViz2 (default: true)
#   use_nav2     - Launch Navigation2 (default: false)
#   use_hitl     - Launch HITL web server (default: false)
#   hitl_port    - HITL web port (default: 8080)
```

### Available Worlds
```bash
# List all worlds
ls ~/advika_robot_ws/src/advika_sim/worlds/

# Options:
ros2 launch advika_sim sim_bringup.launch.py world_file:=advika_playground.world  # Arena with obstacles
ros2 launch advika_sim sim_bringup.launch.py world_file:=3bhk_house.world         # Full house
ros2 launch advika_sim sim_bringup.launch.py world_file:=living_room.world       # Simple room
ros2 launch advika_sim sim_bringup.launch.py world_file:=real_room.world         # Realistic room
```

---

## 4. TELEOP & CONTROL

### Keyboard Teleop
```bash
# Standard teleop
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# With remap (if topic differs)
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=/advika/cmd_vel

# Speed parameters
#   i = Forward
#   , = Backward
#   j = Turn Left
#   l = Turn Right
#   k = Stop
#   q = Speed up
#   z = Speed down
#   w = Turn speed up
#   x = Turn speed down
```

### Programmatic Control
```bash
# Drive forward (0.2 m/s)
ros2 topic pub /advika/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" -1

# Rotate (0.5 rad/s)
ros2 topic pub /advika/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.5}}" -1

# Stop
ros2 topic pub /advika/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" -1

# Continuous forward
ros2 topic pub /advika/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2}}" -1
```

---

## 5. TOPIC COMMANDS

### List Topics
```bash
# All topics
ros2 topic list

# Advika topics only
ros2 topic list | grep advika

# Topic info
ros2 topic list -t | grep advika
```

### Echo Topics
```bash
# LiDAR scan
ros2 topic echo /advika/scan

# Odometry
ros2 topic echo /advika/odom

# IMU data
ros2 topic echo /advika/imu/data

# cmd_vel (what's being sent)
ros2 topic echo /advika/cmd_vel

# Camera images
ros2 topic echo /advika/horizon_camera/image_raw
ros2 topic echo /advika/floor_camera/image_raw

# Once only
ros2 topic echo /advika/scan --once
```

### Topic Info
```bash
# Topic type
ros2 topic type /advika/scan

# Topic Hz (rate)
ros2 topic hz /advika/scan
ros2 topic hz /advika/odom

# Topic bandwidth
ros2 topic bw /advika/scan

# Topic info
ros2 topic info /advika/scan
```

---

## 6. NODE COMMANDS

### List Nodes
```bash
# All running nodes
ros2 node list

# Nodes related to advika
ros2 node list | grep advika

# Node info
ros2 node info /robot_state_publisher
ros2 node info /joint_state_publisher
ros2 node info /gz_bridge
```

### Run Nodes
```bash
# Robot state publisher
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:="$(cat ~/advika_robot_ws/simulation/urdf/advika.urdf)"

# Joint state publisher
ros2 run joint_state_publisher joint_state_publisher

# Teleop
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

---

## 7. BAG RECORDING

### Record
```bash
# Record all topics
ros2 bag record -a

# Record specific topics
ros2 bag record /advika/scan /advika/odom /advika/cmd_vel

# Record with custom name
ros2 bag record -o my_run_001 /advika/scan /advika/odom

# Record with timestamp
ros2 bag record -o $(date +%Y%m%d_%H%M%S) -a

# Compress while recording
ros2 bag record -a --compression-mode folder
```

### Manage Bags
```bash
# List recorded bags
ros2 bag list

# Info about a bag
ros2 bag info my_run_001

# Play a bag
ros2 bag play my_run_001

# Play at slower speed
ros2 bag play my_run_001 -r 0.5

# Play from start
ros2 bag play my_run_001 --start 0

# Delete a bag
rm -rf my_run_001/
```

---

## 8. RVIZ

### Launch RViz
```bash
# With default config
ros2 run rviz2 rviz2

# With specific config
ros2 run rviz2 rviz2 -d ~/advika_robot_ws/simulation/config/advika_sim.rviz

# Or (after sourcing workspace)
rviz2 -d ~/advika_robot_ws/simulation/config/advika_sim.rviz
```

### RViz Displays to Add
```
RobotModel              - Shows robot mesh
LaserScan               - /advika/scan
Image                   - /advika/horizon_camera/image_raw
Image                   - /advika/floor_camera/image_raw
Odometry                - /advika/odom
Path                    - /plan (when Nav2 active)
TF                      - Transform tree
```

---

## 9. HITL DASHBOARD

### Launch HITL
```bash
# Via launch file
ros2 launch advika_sim sim_bringup.launch.py use_hitl:=true

# Standalone
python3 ~/advika_robot_ws/simulation/hitl/hitl_bridge.py --web

# Both ROS and web
python3 ~/advika_robot_ws/simulation/hitl/hitl_bridge.py --both
```

### HITL API Endpoints
```bash
# Get status
curl http://localhost:8080/api/status

# Get telemetry
curl http://localhost:8080/api/telemetry

# Get LiDAR data
curl http://localhost:8080/api/lidar

# Manual drive
curl -X POST "http://localhost:8080/api/manual_drive?linear=0.3&angular=0.0"

# Change mode
curl -X POST http://localhost:8080/api/mode/supervised

# Emergency stop
curl -X POST http://localhost:8080/api/emergency_stop

# Approve action
curl -X POST http://localhost:8080/api/approve/<action_id>

# Reject action
curl -X POST http://localhost:8080/api/reject/<action_id>
```

---

## 10. NAV2 & SLAM

### Navigation2 Launch
```bash
# Launch with Nav2
ros2 launch advika_sim sim_bringup.launch.py use_nav2:=true

# Run Nav2 bringup separately
ros2 launch nav2_bringup navigation_launch.py params_file:=~/advika_robot_ws/simulation/config/nav2_params.yaml
```

### Navigation Goals
```bash
# Send goal via action
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: map}, pose: {position: {x: 2.0, y: 0.0}}}}"

# Send goal via topic
ros2 topic pub /goal_pose geometry_msgs/PoseStamped \
  "{header: {frame_id: map}, pose: {position: {x: 2.0, y: 0.0}}}"
```

### SLAM
```bash
# Launch SLAM
ros2 launch advika_sim sim_bringup.launch.py use_slam:=true

# Or run SLAM Toolbox
ros2 run slam_toolbox async_slam_toolbox_node \
  --ros-args -p slam_params_file:=~/advika_robot_ws/simulation/config/slam_params.yaml

# Save map
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```

---

## 11. GAZEBO

### Gazebo Commands
```bash
# Launch empty world
gz sim

# Launch specific world
gz sim ~/advika_robot_ws/src/advika_sim/worlds/3bhk_house.world

# Gazebo version
gz sim --version

# List worlds
ls ~/advika_robot_ws/src/advika_sim/worlds/
```

### Gazebo Controls (GUI)
```
Scroll       - Zoom in/out
Left drag    - Rotate view
Right drag   - Pan view
Shift+drag   - Orbit
Double-click - Reset view
Delete       - Delete selected
```

---

## 12. BUILD & VERIFICATION

### Build Verification
```bash
# Check build status
ls install/setup.bash && echo "Build OK"

# Verify workspace
source ~/advika_robot_ws/install/setup.bash
ros2 pkg list | grep advika

# Check URDF
ros2 run xacro xacro ~/advika_robot_ws/simulation/urdf/advika.urdf > /dev/null && echo "URDF OK"
```

### Verification Script
```bash
# Run complete verification
~/verify_prerequisites.sh

# Quick check
python3 -c "import fastapi, cv2, numpy, yaml, websockets" && echo "Python deps OK"
ros2 --version && gz sim --version && echo "ROS2 + Gazebo OK"
```

---

## 13. TTS & VOICE

### espeak-ng
```bash
# Basic speech
espeak-ng "Hello, I am Advika"

# Slow speech
espeak-ng "Moving forward" -s 120

# Fast speech
espeak-ng "Obstacle detected" -s 180

# Save to file
espeak-ng "Navigation complete" -w announcement.wav

# Other voices
espeak-ng "Hello" -v en-us
espeak-ng "Hello" -v en-gb
espeak-ng "Hello" -v fr
```

---

## 14. UTILITIES

### Git Commands
```bash
# Clone
git clone https://github.com/TheAbhishekraj/advika_robot_ws.git

# Pull latest
cd ~/advika_robot_ws && git pull

# Check status
cd ~/advika_robot_ws && git status

# Check branches
cd ~/advika_robot_ws && git branch -a

# Switch to main
cd ~/advika_robot_ws && git checkout main
```

### File Operations
```bash
# Count lines in URDF
grep -c "<link name=" ~/advika_robot_ws/simulation/urdf/advika.urdf
grep -c "<joint name=" ~/advika_robot_ws/simulation/urdf/advika.urdf

# View URDF
cat ~/advika_robot_ws/simulation/urdf/advika.urdf

# Validate URDF XML
xmllint --noout ~/advika_robot_ws/simulation/urdf/advika.urdf && echo "URDF XML OK"

# Validate world XML
xmllint --noout ~/advika_robot_ws/src/advika_sim/worlds/3bhk_house.world && echo "World XML OK"
```

### Process Management
```bash
# Kill all simulation
pkill -f gz
pkill -f ros2
pkill -f rviz2

# Kill specific
kill $(ps aux | grep sim_bringup | grep -v grep | awk '{print $2}')

# Check running processes
ps aux | grep -E "gz|ros2|rviz" | grep -v grep
```

### Network/Debug
```bash
# Check ports
sudo lsof -i :8080
sudo lsof -i :9090

# Ping (if networked)
ping localhost

# Check display
echo $DISPLAY
```

---

## 📋 QUICK REFERENCE CARD

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                     ADVIKA 3.0 QUICK COMMANDS                             ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  SETUP:                                                                   ║
║    bash <(curl .../setup_advika.sh)     # One-time setup                  ║
║    source install/setup.bash           # Source workspace               ║
║                                                                           ║
║  LAUNCH:                                                                  ║
║    ros2 launch advika_sim sim_bringup.launch.py    # Full sim             ║
║    ros2 launch advika_sim sim_bringup.launch.py use_nav2:=true  # +Nav2  ║
║    ros2 launch advika_sim sim_bringup.launch.py use_hitl:=true  # +HITL ║
║                                                                           ║
║  DRIVE:                                                                   ║
║    ros2 run teleop_twist_keyboard teleop_twist_keyboard                   ║
║    ros2 topic pub /advika/cmd_vel ... -1   # Programmatic                  ║
║                                                                           ║
║  TOPICS:                                                                  ║
║    ros2 topic list | grep advika          # List advika topics           ║
║    ros2 topic echo /advika/scan           # LiDAR data                    ║
║    ros2 topic echo /advika/odom           # Odometry                      ║
║                                                                           ║
║  BAG:                                                                     ║
║    ros2 bag record -a                        # Record all                  ║
║    ros2 bag play <bag_name>                 # Playback                    ║
║                                                                           ║
║  HITL:                                                                    ║
║    curl http://localhost:8080/api/status   # Status                       ║
║    curl -X POST .../emergency_stop          # E-Stop                       ║
║                                                                           ║
║  BUILD:                                                                  ║
║    colcon build --symlink-install          # Build workspace             ║
║    source install/setup.bash               # Re-source                   ║
║                                                                           ║
║  TTS:                                                                    ║
║    espeak-ng "Hello"                         # Robot speaks                ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

---

## 🔧 TROUBLESHOOTING COMMANDS

```bash
# Something not working? Try these in order:

# 1. Kill everything
pkill -f gz; pkill -f ros2; pkill -f rviz2

# 2. Re-source
source ~/advika_robot_ws/install/setup.bash

# 3. Clean rebuild
rm -rf build/ install/ log/
colcon build --symlink-install

# 4. Check prerequisites
ros2 --version && gz sim --version

# 5. Verify URDF
ros2 run xacro xacro ~/advika_robot_ws/simulation/urdf/advika.urdf > /dev/null

# 6. Try launching again
ros2 launch advika_sim sim_bringup.launch.py
```

---

*End of Command Reference*
*For full tutorials, see SIMULATION_MASTER_GUIDE.md*