# ADVIKA 3.0 SIMULATION MASTER GUIDE

**Version:** 1.0 | **Date:** 2026-07-25
**Target:** Ubuntu 24.04 LTS + ROS2 Jazzy + Gazebo Harmonic
**Mentor:** This guide is your complete learning path for simulation mastery

---

## 📋 TABLE OF CONTENTS

1. [Prerequisites Checklist](#prerequisites-checklist)
2. [Quick Start (5 Minutes)](#quick-start-5-minutes)
3. [Understanding the Launch](#understanding-the-launch)
4. [Simulation Tasks (Week by Week)](#simulation-tasks-week-by-week)
5. [Sensor Tuning Guide](#sensor-tuning-guide)
6. [Dashboard & Monitoring](#dashboard--monitoring)
7. [Recording & Screenshots](#recording--screenshots)
8. [Robot Voice / TTS](#robot-voice--tts)
9. [3D Visualization](#3d-visualization)
10. [Model-View Interaction](#model-view-interaction)
11. [Automation Scripts](#automation-scripts)
12. [Troubleshooting](#troubleshooting)
13. [Future Enhancements](#future-enhancements)

---

## 1. PREREQUISITES CHECKLIST

### Run This First - All Must Be PASS

```bash
# ============================================
# PREREQUISITES VERIFICATION COMMAND
# Run this and verify ALL checks pass
# ============================================

cat << 'EOF' > ~/verify_prerequisites.sh
#!/bin/bash
echo "=============================================="
echo "ADVIKA 3.0 PREREQUISITES CHECK"
echo "=============================================="

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0

check() {
    if eval "$1" &>/dev/null; then
        echo -e "${GREEN}✅ $2${NC}"
        ((PASS++))
    else
        echo -e "${RED}❌ $2${NC}"
        ((FAIL++))
    fi
}

# OS
check "[[ \$(lsb_release -rs) == '24.04' ]]" "Ubuntu 24.04 LTS"
check "[[ \$(df -h / | tail -1 | awk '{print \$4}' | sed 's/[A-Za-z]//') -gt 30 ]]" "30GB+ disk space"
check "[[ \$(free -m | head -2 | tail -1 | awk '{print \$2}') -gt 8000 ]]" "8GB+ RAM"
check "[[ \$(nproc) -ge 4 ]]" "4+ CPU cores"

# ROS2
check "ros2 --version &>/dev/null" "ROS2 Jazzy installed"
check "[[ \$ROS_DISTRO == 'jazzy' ]]" "ROS distro set to jazzy"

# Gazebo
check "gz sim --version &>/dev/null" "Gazebo Harmonic installed"

# Python
for pkg in fastapi cv2 numpy yaml websockets; do
    check "python3 -c \"import $pkg\"" "Python $pkg"
done

# Workspace
check "[[ -d ~/advika_robot_ws/install ]]" "Workspace built"
check "[[ -f ~/advika_robot_ws/src/advika_description/urdf/advika.urdf ]] || [[ -f ~/advika_robot_ws/simulation/urdf/advika.urdf ]]" "URDF file exists"

echo ""
echo "=============================================="
echo "Result: $PASS passed, $FAIL failed"
echo "=============================================="

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✅ READY TO LAUNCH SIMULATION!${NC}"
else
    echo -e "${RED}❌ FIX FAILURES BEFORE PROCEEDING${NC}"
fi
EOF
chmod +x ~/verify_prerequisites.sh
~/verify_prerequisites.sh
```

### Expected Output (All Green Checks)
```
==============================================
ADVIKA 3.0 PREREQUISITES CHECK
==============================================
✅ Ubuntu 24.04 LTS
✅ 30GB+ disk space
✅ 8GB+ RAM
✅ 4+ CPU cores
✅ ROS2 Jazzy installed
✅ ROS distro set to jazzy
✅ Gazebo Harmonic installed
✅ Python fastapi
✅ Python cv2
✅ Python numpy
✅ Python yaml
✅ Python websockets
✅ Workspace built
✅ URDF file exists

==============================================
Result: 14 passed, 0 failed
==============================================
✅ READY TO LAUNCH SIMULATION!
```

---

## 2. QUICK START (5 MINUTES)

### Single Command Setup (First Time Only)

```bash
# Option A: Automated setup (recommended for first time)
bash <(curl -fsSL https://raw.githubusercontent.com/TheAbhishekraj/advika_robot_ws/main/scripts/setup_advika.sh)

# Option B: If already cloned, build manually
cd ~/advika_robot_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install
source install/setup.bash
```

### Launch Simulation

```bash
# Terminal 1: Launch everything (Gazebo + RViz + Teleop)
ros2 launch advika_sim sim_bringup.launch.py
```

**Expected Result:**
- Gazebo window opens showing the robot in the arena
- RViz window opens with robot model and sensor displays
- xterm window opens with teleop keyboard active

### Drive the Robot

```bash
# In the teleop xterm window, use:
#   i = Forward
#   , = Backward
#   j = Turn Left
#   l = Turn Right
#   k = Stop
#   q/z = Speed up/down
```

---

## 3. UNDERSTANDING THE LAUNCH

### What Gets Started

When you run `ros2 launch advika_sim sim_bringup.launch.py`:

```
┌────────────────────────────────────────────────────────────────────┐
│                    SIM_BRINGUP.LAUNCH.PY                          │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  1. GAZEBO SIMULATOR (gz sim)                                      │
│     └── Loads: advika_playground.world (or specified world)        │
│                                                                    │
│  2. ROBOT STATE PUBLISHER                                          │
│     └── Publishes: robot_description from URDF                     │
│                                                                    │
│  3. JOINT STATE PUBLISHER                                          │
│     └── Publishes: joint_states from /joint_states topic          │
│                                                                    │
│  4. SPAWN ROBOT IN GAZEBO                                          │
│     └── Creates robot from /robot_description topic               │
│                                                                    │
│  5. ROS-GAZEBO BRIDGE                                              │
│     └── Bridges: cmd_vel, odom, scan, camera, imu, clock         │
│                                                                    │
│  6. RVIZ2 (if use_rviz:=true)                                      │
│     └── Shows: Robot model, LaserScan, Cameras, TF tree           │
│                                                                    │
│  7. TELEOP TWIST KEYBOARD                                          │
│     └── Subscribes: /advika/cmd_vel                                │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### Launch Arguments

```bash
# Full syntax
ros2 launch advika_sim sim_bringup.launch.py \
    world_file:=3bhk_house.world \
    use_rviz:=true \
    use_nav2:=false \
    use_hitl:=false \
    hitl_port:=8080
```

### Launch Arguments Explained

| Argument | Default | Description |
|----------|---------|-------------|
| `world_file` | `advika_playground.world` | Which world to load |
| `use_rviz` | `true` | Launch RViz2 visualization |
| `use_nav2` | `false` | Launch Navigation2 stack |
| `use_hitl` | `false` | Launch HITL web dashboard |
| `hitl_port` | `8080` | HITL web server port |

### Available World Files

```bash
# List all worlds
ls ~/advika_robot_ws/src/advika_sim/worlds/

# Options:
# - advika_playground.world    (obstacle course)
# - 3bhk_house.world          (full 3BHK house)
# - living_room.world         (simple room)
# - real_room.world           (realistic room)
```

---

## 4. SIMULATION TASKS (WEEK BY WEEK)

### WEEK 1: GET RUNNING ✓

#### Task 1.1: Launch and Verify

**Command:**
```bash
ros2 launch advika_sim sim_bringup.launch.py
```

**Expected Windows:**
1. **Gazebo** - Robot visible in arena
2. **RViz** - Green robot model, TF tree
3. **xterm** - Teleop ready

**Verification:**
- Robot in Gazebo matches URDF dimensions
- TF tree shows all links (base_link, wheels, lidar_link, etc.)

**Result:** □ PASS □ FAIL
**Screenshot:** Save as `week1_task1_launch.png`

---

#### Task 1.2: Drive Robot Forward

**Command:**
```bash
# In teleop xterm, press 'i' to move forward
# Observe robot moving in Gazebo
```

**Verification:**
- Robot moves in +X direction
- Wheels rotate (if visual enabled)
- /advika/odom topic shows position changing

**Check topic:**
```bash
ros2 topic echo /advika/odom --once
```

**Result:** □ PASS □ FAIL
**Screenshot:** Save as `week1_task2_drive_forward.png`

---

#### Task 1.3: Rotate Robot

**Command:**
```bash
# In teleop xterm:
#   j = Turn left (CCW)
#   l = Turn right (CW)
```

**Verification:**
- Robot rotates around Z-axis
- /advika/odom shows orientation changing

**Result:** □ PASS □ FAIL
**Screenshot:** Save as `week1_task3_rotate.png`

---

### WEEK 2: URDF EXPLORATION

#### Task 2.1: Understand Robot Structure

**Command:**
```bash
# View complete URDF
cat ~/advika_robot_ws/simulation/urdf/advika.urdf

# Or in RViz: Click on robot model to see link hierarchy
```

**Verification:**
- Identify all 12 links
- Identify all joints
- Note parent-child relationships

**Learning:**
```bash
# Count links
grep -c "<link name=" ~/advika_robot_ws/simulation/urdf/advika.urdf
# Expected: 12

# Count joints
grep -c "<joint name=" ~/advika_robot_ws/simulation/urdf/advika.urdf
# Expected: 11
```

**Result:** □ PASS □ FAIL
**Notes:** Document link hierarchy

---

#### Task 2.2: Modify Base Color

**Exercise:** Change robot base from blue to red

**Command:**
```bash
# Edit URDF
nano ~/advika_robot_ws/simulation/urdf/advika.urdf

# Find and change:
# <material name="blue">
#   <color rgba="0.1 0.3 0.8 1.0"/>
# To:
# <material name="red">
#   <color rgba="0.8 0.1 0.1 1.0"/>
```

**Verify:**
```bash
# Rebuild (if using xacro) or restart launch
# Robot should appear red in Gazebo
```

**Result:** □ PASS □ FAIL
**Screenshot:** Save as `week2_task2_color_change.png`

---

#### Task 2.3: Inspect Sensor Topics

**Command:**
```bash
# List all advika topics
ros2 topic list | grep advika

# Check LiDAR scan
ros2 topic echo /advika/scan --once

# Check odometry
ros2 topic echo /advika/odom --once

# Check IMU
ros2 topic echo /advika/imu/data --once
```

**Expected Data:**
```
/advika/scan: sensor_msgs/LaserScan with ranges[]
/advika/odom: nav_msgs/Odometry with position, orientation
/advika/imu/data: sensor_msgs/Imu with orientation, angular_velocity
/advika/horizon_camera/image_raw: sensor_msgs/Image
/advika/floor_camera/image_raw: sensor_msgs/Image
```

**Result:** □ PASS □ FAIL

---

### WEEK 3: NAVIGATION

#### Task 3.1: Enable Navigation2

**Command:**
```bash
# Launch with Nav2 enabled
ros2 launch advika_sim sim_bringup.launch.py use_nav2:=true
```

**Verify:**
```bash
# Check Nav2 nodes
ros2 node list | grep -E "nav2|amcl|controller"

# Check costmaps
ros2 topic list | grep costmap
```

**Result:** □ PASS □ FAIL

---

#### Task 3.2: Send Navigation Goal

**Command:**
```bash
# Use RViz:
# 1. Click "2D Pose Estimate" - click on map to set starting position
# 2. Click "2D Nav Goal" - click on map to set destination

# Or via command line:
ros2 topic pub /goal_pose geometry_msgs/PoseStamped "{header: {frame_id: map}, pose: {position: {x: 2.0, y: 0.0}}}"

# Alternative via action:
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: map}, pose: {position: {x: 2.0, y: 0.0}}}}"
```

**Verification:**
- Robot navigates to goal
- Path shown in RViz (green line)
- Robot avoids obstacles

**Result:** □ PASS □ FAIL
**Screenshot:** Save as `week3_task2_navigation.png`

---

#### Task 3.3: Test Obstacle Avoidance

**Command:**
```bash
# Place obstacles in Gazebo manually:
# In Gazebo window: Insert -> Bricks/Cones/Boxes

# Or add via world file (later task)

# Drive toward obstacle
# Robot should stop before collision
```

**Verification:**
- Safety monitor triggers auto-stop
- Console shows: "OBSTACLE DETECTED - STOPPING"

**Result:** □ PASS □ FAIL

---

### WEEK 4: HITL DASHBOARD

#### Task 4.1: Launch HITL Dashboard

**Command:**
```bash
# Launch with HITL enabled
ros2 launch advika_sim sim_bringup.launch.py use_hitl:=true hitl_port:=8080

# Open browser: http://localhost:8080
```

**Dashboard Features:**
- Real-time camera feeds
- LiDAR visualization
- Telemetry panel
- Action queue
- Mode selector
- Safety log
- Manual drive controls

**Result:** □ PASS □ FAIL
**Screenshot:** Save as `week4_task1_hitl_dashboard.png`

---

#### Task 4.2: Manual Drive via Dashboard

**Command:**
```bash
# In browser dashboard:
# 1. Click "MANUAL" mode
# 2. Use on-screen controls to drive

# Or via API:
curl -X POST "http://localhost:8080/api/manual_drive?linear=0.3&angular=0.0"
```

**Result:** □ PASS □ FAIL

---

#### Task 4.3: Test Safety Override

**Command:**
```bash
# Drive robot toward wall using teleop

# Click EMERGENCY STOP in dashboard
curl -X POST http://localhost:8080/api/emergency_stop

# Verify robot stops immediately
ros2 topic echo /advika/cmd_vel --once
# Should show all zeros
```

**Result:** □ PASS □ FAIL

---

## 5. SENSOR TUNING GUIDE

### 5.1 LiDAR Parameters

**URDF Location:** `/advika/scan` topic from `lidar_link`

**Tune these in URDF:**
```xml
<gazebo reference="lidar_link">
  <sensor name="lidar_sensor" type="gpu_lidar">
    <topic>/advika/scan</topic>
    <update_rate>10</update_rate>  <!-- Hz -->
    <lidar>
      <range>
        <min>0.12</min>           <!-- meters -->
        <max>12.0</max>           <!-- meters -->
        <resolution>0.01</resolution>
      </range>
      <scan>
        <horizontal>
          <samples>360</samples>  <!-- Higher = more detailed -->
          <resolution>1</resolution>
          <min_angle>-3.14159</min_angle>
          <max_angle>3.14159</max_angle>
        </horizontal>
      </scan>
      <noise>
        <type>gaussian</type>
        <mean>0.0</mean>
        <stddev>0.01</stddev>    <!-- Tune for realism -->
      </noise>
    </ladar>
  </sensor>
</gazebo>
```

**Real Sensor Matching (LD06):**
```yaml
range_min: 0.12m
range_max: 12.0m
samples: 360
scan_rate: 10Hz
noise_stddev: 0.01 (tuned)
```

**Verify Changes:**
```bash
# Restart simulation
ros2 launch advika_sim sim_bringup.launch.py

# Check scan data
ros2 topic echo /advika/scan --once
```

---

### 5.2 Camera Parameters

**Tune in URDF:**
```xml
<gazebo reference="horizon_camera_link">
  <sensor name="horizon_camera" type="camera">
    <topic>/advika/horizon_camera/image_raw</topic>
    <update_rate>30</update_rate>    <!-- Hz -->
    <camera>
      <horizontal_fov>1.22</horizontal_fov>  <!-- radians (~70°) -->
      <image>
        <width>640</width>
        <height>480</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>           <!-- meters -->
        <far>100</far>             <!-- meters -->
      </clip>
    </camera>
  </sensor>
</gazebo>
```

**Real Sensor Matching (Pi Camera Module 3 Wide):**
```yaml
horizontal_fov: 1.309 rad (~75°)
resolution: 640x480
update_rate: 30Hz
clip_near: 0.1m
clip_far: 100m
```

---

### 5.3 IMU Parameters

**Tune in URDF:**
```xml
<gazebo reference="imu_link">
  <sensor name="imu_sensor" type="imu">
    <topic>/advika/imu/data</topic>
    <update_rate>100</update_rate>   <!-- Hz -->
    <!-- Noise parameters -->
  </sensor>
</gazebo>
```

---

### 5.4 ToF Array Parameters

**URDF Location:** `/advika/tof` (if published)

**Configuration:**
- Range: 0.1m - 4.0m
- 8x8 array = 64 distance measurements
- Update rate: 15-60 Hz (configurable)

**Verify ToF data:**
```bash
# Check if ToF topic exists
ros2 topic list | grep tof

# Echo data
ros2 topic echo /advika/tof/data --once
```

---

## 6. DASHBOARD & MONITORING

### 6.1 HITL Dashboard (Web Interface)

**URL:** http://localhost:8080

**Sections:**

| Section | What It Shows | How to Use |
|---------|--------------|------------|
| **Camera Feeds** | Horizon + Floor camera | Monitor vision |
| **LiDAR Viz** | 2D top-down scan | See obstacles |
| **Telemetry** | Position, velocity, battery | Monitor status |
| **Action Queue** | Pending AI actions | Approve/reject |
| **Mode Selector** | FULL_AUTO/SUPERVISED/MANUAL/EMERGENCY | Change mode |
| **Safety Log** | Collision warnings, stops | Review events |
| **Manual Drive** | On-screen controls | Direct control |

---

### 6.2 API Endpoints

```bash
# Get all telemetry
curl http://localhost:8080/api/telemetry

# Get LiDAR data
curl http://localhost:8080/api/lidar

# Get robot position
curl http://localhost:8080/api/position

# Change mode
curl -X POST http://localhost:8080/api/mode/supervised

# Manual drive
curl -X POST "http://localhost:8080/api/manual_drive?linear=0.2&angular=0.5"

# Emergency stop
curl -X POST http://localhost:8080/api/emergency_stop

# Get safety events
curl http://localhost:8080/api/safety_events
```

---

### 6.3 RViz Displays

**Add these displays in RViz:**

| Display | Topic | Purpose |
|---------|-------|---------|
| RobotModel | - | Show robot mesh |
| LaserScan | /advika/scan | LiDAR visualization |
| Image | /advika/horizon_camera/image_raw | Horizon camera |
| Image | /advika/floor_camera/image_raw | Floor camera |
| TF | - | Transform tree |
| Odometry | /advika/odom | Position arrow |
| Path | /plan | Planned path |

---

### 6.4 Monitor Topics

```bash
# List all topics
ros2 topic list

# Topic bandwidth
ros2 topic hz /advika/scan
ros2 topic hz /advika/odom
ros2 topic hz /advika/imu/data

# Topic data size
ros2 topic bw /advika/scan

# Echo specific topic
ros2 topic echo /advika/cmd_vel
```

---

## 7. RECORDING & SCREENSHOTS

### 7.1 Take Screenshot (Gazebo)

**GUI Method:**
1. Click Gazebo window
2. File → Save screenshot
3. Screenshot saved to `~/.gazebo/screenshots/`

**CLI Method:**
```bash
# Take screenshot via Gazebo transport
gz topic -t /gui/screenshot -m gz.msgs.Image -p "data: $(date +%s)" > screenshot.png

# Or use scrot
scrot -u screenshot_$(date +%Y%m%d_%H%M%S).png
```

### 7.2 Take Screenshot (RViz)

**GUI Method:**
1. Click RViz window
2. File → Save screenshot
3. Or Ctrl+S to save config, Ctrl+Shift+S for screenshot

**CLI Method:**
```bash
# Use gnome-screenshot
gnome-screenshot -w  # Window
gnome-screenshot -a  # Area
```

### 7.3 Record Bag File

```bash
# Record all topics
ros2 bag record -a

# Record specific topics
ros2 bag record /advika/scan /advika/odom /advika/cmd_vel

# Record with custom name
ros2 bag record -o my_run_001 /advika/scan /advika/odom

# List recorded bags
ros2 bag list

# Playback recorded bag
ros2 bag play my_run_001
```

### 7.4 Automated Recording Script

```bash
cat << 'EOF' > ~/record_simulation.sh
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="$HOME/advika_bags"

mkdir -p "$OUTPUT_DIR"

echo "Recording simulation to $OUTPUT_DIR/run_$DATE..."
echo "Press Ctrl+C to stop"

# Record with timestamp
ros2 bag record -o "$OUTPUT_DIR/run_$DATE" -a

# When done, info will be saved
echo "Recording saved to $OUTPUT_DIR/run_$DATE"
EOF
chmod +x ~/record_simulation.sh
```

---

## 8. ROBOT VOICE / TTS

### 8.1 Test TTS

```bash
# Test espeak-ng
espeak-ng "Hello, I am Advika"

# Adjust speed
espeak-ng "Hello" -s 150  # 150 words per minute

# Save to file
espeak-ng "Autonomous navigation started" -w announcement.wav
```

### 8.2 Robot Speech via API

```bash
# If HITL bridge supports TTS
curl -X POST "http://localhost:8080/api/speak?message=Obstacle%20detected"

# Or via terminal
python3 -c "
import subprocess
subprocess.run(['espeak-ng', 'Path obstructed, recalculating trajectory'])
"
```

### 8.3 TTS Integration in Code

```python
import subprocess

def robot_speak(message: str, speed: int = 150):
    """Make robot speak using espeak-ng"""
    subprocess.run(['espeak-ng', message, '-s', str(speed)])

# Usage
robot_speak("Moving forward")
robot_speak("Obstacle detected, stopping")
robot_speak("Navigation complete")
```

---

## 9. 3D VISUALIZATION

### 9.1 Gazebo 3D View

**Controls:**
| Key | Action |
|-----|--------|
| Scroll | Zoom in/out |
| Left drag | Rotate view |
| Right drag | Pan view |
| Shift + drag | Orbit |
| Double-click | Reset view |

**View Models:**
- Click on robot to select
- Show bounding box: View → Bounding box
- Show link frames: View → Wireframe

### 9.2 RViz 3D View

**Add displays:**
1. Click "Add" button (bottom left)
2. Select "RobotModel" - shows full robot
3. Select "TF" - shows transform frames
4. Select "LaserScan" - shows scan as 3D points
5. Select "Camera" - shows image overlay

### 9.3 Understanding Coordinate Frames

```bash
# Show TF tree
ros2 run rqt_tf_tree rqt_tf_tree

# Or via command line
ros2 run tf2_tools view_frames.py

# Echo TF transforms
ros2 topic echo /tf_static
ros2 topic echo /tf
```

**Frames in Advika:**
```
map → odom → base_footprint → base_link → wheels, lidar, cameras, etc.
```

---

## 10. MODEL-VIEW INTERACTION

### 10.1 Move Objects in Gazebo

**Select Object:**
- Left-click on object in Gazebo
- Blue outline = selected

**Move Object:**
- Drag arrow handles to move
- Shift+drag to rotate
- Scroll wheel on handles to adjust

**Spawn New Object:**
1. Click "Insert" tab (left panel)
2. Select category (building, furniture, etc.)
3. Click in world to place

**Delete Object:**
- Select object
- Press Delete key

### 10.2 Save Modified World

```bash
# In Gazebo: File → Save World As
# Saves to: ~/.gazebo/games/user-XXXXX/default.world

# Or save programmatically:
gz world -o my_modified_world
```

### 10.3 Interactive Markers

```bash
# Create interactive marker
ros2 run interactive_markers tutorial_server

# View in RViz: Add → InteractiveMarker
```

---

## 11. AUTOMATION SCRIPTS

### 11.1 Multi-Window Launch Script

```bash
cat << 'EOF' > ~/launch_advika_full.sh
#!/bin/bash
# Launch all simulation windows

# Terminal 1: Gazebo + Simulation
xterm -title "Gazebo Simulation" -e "ros2 launch advika_sim sim_bringup.launch.py; bash" &
sleep 3

# Terminal 2: RViz (if not already included)
xterm -title "RViz" -e "source ~/advika_robot_ws/install/setup.bash; ros2 run rviz2 rviz2 -d ~/advika_robot_ws/simulation/config/advika_sim.rviz; bash" &
sleep 2

# Terminal 3: Teleop (if not already included)
xterm -title "Teleop" -e "source ~/advika_robot_ws/install/setup.bash; ros2 run teleop_twist_keyboard teleop_twist_keyboard; bash" &

echo "All windows launched!"
EOF
chmod +x ~/launch_advika_full.sh
```

### 11.2 Auto-Test Script

```bash
cat << 'EOF' > ~/test_simulation.sh
#!/bin/bash
# Automated simulation test

echo "=== Advika Simulation Test ==="

# Test 1: Launch
echo "[1/5] Launching simulation..."
timeout 30s ros2 launch advika_sim sim_bringup.launch.py &
sleep 15

# Test 2: Check topics
echo "[2/5] Checking topics..."
ros2 topic list | grep advika || exit 1

# Test 3: Check LiDAR
echo "[3/5] Checking LiDAR..."
ros2 topic echo /advika/scan --once | grep -q ranges || exit 1

# Test 4: Drive test
echo "[4/5] Testing drive..."
timeout 5s ros2 topic pub /advika/cmd_vel geometry_msgs/Twist "{linear: {x: 0.2}}" || true

# Test 5: Stop
echo "[5/5] Stopping..."
timeout 2s ros2 topic pub /advika/cmd_vel geometry_msgs/Twist "{linear: {x: 0.0}}" || true

echo "=== Test Complete ==="
pkill -f "gz sim" || true
pkill -f "ros2 launch" || true
EOF
chmod +x ~/test_simulation.sh
```

---

## 12. TROUBLESHOOTING

### Problem: Gazebo won't start

```bash
# Check if Gazebo is installed
gz sim --version

# Try software rendering
export LIBGL_ALWAYS_SOFTWARE=1
ros2 launch advika_sim sim_bringup.launch.py

# Check for port conflict
lsof -i :8080
lsof -i :9090
```

### Problem: Robot not visible in Gazebo

```bash
# Check robot spawn
ros2 topic echo /robot_description --once | head

# Manually spawn
ros2 run ros_gz_sim create -name advika -topic robot_description

# Check for errors
ros2 launch advika_sim sim_bringup.launch.py --ros-args --log-level debug
```

### Problem: Robot doesn't move

```bash
# Check cmd_vel being published
ros2 topic echo /advika/cmd_vel

# Check if bridge is running
ros2 node list | grep bridge

# Restart bridge
ros2 run ros_gz_bridge parameter_bridge /advika/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist
```

### Problem: No LiDAR data

```bash
# Check scan topic
ros2 topic list | grep scan

# Check Gazebo sensor
gz topic -l | grep scan

# Enable sensor visualization in Gazebo
# View → Sensors → Show All
```

### Problem: RViz crashes

```bash
# Clear RViz config
rm ~/.rviz2/*.rviz

# Launch with fresh config
ros2 run rviz2 rviz2
```

---

## 13. FUTURE ENHANCEMENTS

### AI Integration (Future)
```bash
# Connect AI agent
ros2 run mcp_servers/ai_agent.py

# Agent will:
# - Subscribe to sensor topics
# - Make decisions
# - Publish cmd_vel
# - Use HITL for oversight
```

### SLAM Mapping (Future)
```bash
# Enable SLAM
ros2 launch advika_sim sim_bringup.launch.py use_slam:=true

# Save map
ros2 run nav2_map_server map_saver_cli -f ~/my_map
```

### Multi-Robot (Future)
```bash
# Launch robot 1
ros2 launch advika_sim sim_bringup.launch.py namespace:=advika_1 x:=0.0 y:=0.0

# Launch robot 2
ros2 launch advika_sim sim_bringup.launch.py namespace:=advika_2 x:=2.0 y:=0.0
```

---

## 14. WORKING, PENDING & FUTURE STATUS

### ✅ COMPLETED (Working)
| Item | Status | Verification |
|------|--------|--------------|
| Prerequisites check script | ✅ DONE | Run `~/verify_prerequisites.sh` |
| Single command setup | ✅ DONE | Run `setup_advika.sh` |
| Launch simulation | ✅ DONE | `ros2 launch advika_sim sim_bringup.launch.py` |
| Multi-window launch | ✅ DONE | `launch_advika_full.sh` |
| Teleop control | ✅ DONE | Keyboard i,j,k,l |
| Basic navigation | ✅ DONE | Nav2 with `use_nav2:=true` |
| HITL dashboard | ✅ DONE | http://localhost:8080 |
| Recording tools | ✅ DONE | `ros2 bag record` |
| TTS (espeak-ng) | ✅ DONE | `espeak-ng "text"` |

### ⏳ PENDING (Not Yet Working)
| Item | Status | Required Action |
|------|--------|-----------------|
| 3BHK world navigation | ⏳ PENDING | Need SLAM + good map |
| Autonomous goal navigation | ⏳ PENDING | Test in living_room first |
| Safety auto-stop verified | ⏳ PENDING | Test with obstacle |
| Camera feeds in dashboard | ⏳ PENDING | Verify `/advika/horizon_camera/image_raw` |
| TTS via API | ⏳ PENDING | Add `/api/speak` endpoint to hitl_bridge |

### 🚀 FUTURE (Not Implemented)
| Item | Status | Notes |
|------|--------|-------|
| AI agent integration | 🚀 TODO | MCP server needed |
| Custom furniture models | 🚀 TODO | Design in Fusion 360 |
| SLAM map save/load | 🚀 TODO | Complete mapping first |
| Multi-floor navigation | 🚀 TODO | Not in current world |
| Voice commands | 🚀 TODO | Needs AI + TTS integration |

---

## 15. QUICK COMMAND REFERENCE

```bash
# ============================================
# QUICK COMMAND REFERENCE
# ============================================

# LAUNCH
ros2 launch advika_sim sim_bringup.launch.py                              # Full simulation
ros2 launch advika_sim sim_bringup.launch.py use_nav2:=true            # With Nav2
ros2 launch advika_sim sim_bringup.launch.py use_hitl:=true            # With HITL

# WORLD
ros2 launch advika_sim sim_bringup.launch.py world_file:=3bhk_house.world

# TELEOP
ros2 run teleop_twist_keyboard teleop_twist_keyboard                    # Keyboard drive

# TOPICS
ros2 topic list                                                          # List all
ros2 topic echo /advika/scan                                             # LiDAR
ros2 topic echo /advika/odom                                             # Odometry
ros2 topic echo /advika/cmd_vel                                         # Drive commands

# NODES
ros2 node list                                                           # List all
ros2 node info /robot_state_publisher                                   # Node info

# BAG
ros2 bag record -a                                                      # Record all
ros2 bag play <bag_name>                                                 # Playback

# RVIZ
ros2 run rviz2 rviz2 -d ~/advika_robot_ws/simulation/config/advika_sim.rviz

# HITL
curl http://localhost:8080/api/status                                    # Status
curl -X POST http://localhost:8080/api/emergency_stop                   # E-Stop

# BUILD
cd ~/advika_robot_ws && colcon build --symlink-install && source install/setup.bash

# VERIFY
~/verify_prerequisites.sh                                                # Check deps
```

---

## 16. SAVE THIS GUIDE

```bash
# Save the full guide as a script you can run
cp ~/advika_robot_ws/docs/SIMULATION_MASTER_GUIDE.md ~/SIMULATION_MASTER_GUIDE.md

# Create quick reference card
cat << 'EOF' > ~/QUICK_REF.txt
╔═══════════════════════════════════════════════════════╗
║          ADVIKA 3.0 QUICK REFERENCE                  ║
╠═══════════════════════════════════════════════════════╣
║                                                       ║
║  LAUNCH:     ros2 launch advika_sim sim_bringup.launch.py  ║
║  TELEOP:     i=forward  k=stop  j/l=turn              ║
║  NAV2:       ros2 launch advika_sim use_nav2:=true    ║
║  HITL:       http://localhost:8080                     ║
║  E-STOP:     curl -X POST http://localhost:8080/api/emergency_stop ║
║                                                       ║
║  TOPICS:     ros2 topic list | grep advika            ║
║  RECORD:     ros2 bag record -a                       ║
║  BUILD:      colcon build --symlink-install           ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
EOF
```

---

*End of Simulation Master Guide*
*Mentor says: Practice each task until you understand it. Then move on.*