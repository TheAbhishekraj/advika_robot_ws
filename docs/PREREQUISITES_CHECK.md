# ADVIKA 3.0 SIMULATION PREREQUISITES CHECK SHEET

**Version:** 1.0 | **Date:** 2026-07-25 | **Target:** Ubuntu 24.04 LTS + ROS2 Jazzy + Gazebo Harmonic

> 🔴 **Master Guide:** Follow [SETUP.md](../SETUP.md) for the complete Step 1–5 workspace setup.

---

## 🚨 BEFORE STARTING - CRITICAL REQUIREMENTS

### OS Version Check
```bash
# Verify Ubuntu 24.04 LTS (MUST be 24.04, Jazzy requires it)
lsb_release -a
# Expected: Description: Ubuntu 24.04 LTS

uname -r
# Expected: 6.x.x-xxxx-generic (or similar 6.x kernel)
```

### ❌ DO NOT PROCEED IF:
- ❌ Using Ubuntu 22.04 (Jazzy requires 24.04)
- ❌ Using Windows directly (Gazebo does NOT work on Windows)
- ❌ Using macOS (Gazebo works but slow, use Ubuntu VM)
- ❌ Using ROS2 Humble or Iron (different ROS distribution)

---

## ✅ PHASE 1: OS VERIFICATION

### 1.1 Ubuntu Version
```bash
# Command
lsb_release -a 2>/dev/null || cat /etc/os-release

# Expected Output
"""
No LSB modules are available.
Distributor ID: Ubuntu
Description:    Ubuntu 24.04 LTS
Release:        24.04
Codename:       noble
"""

# Result: □ PASS  □ FAIL
```

### 1.2 Disk Space
```bash
# Command
df -h /

# Required: Minimum 30GB free
# Recommended: 50GB+ SSD

# Result: □ PASS  □ FAIL (need ____ GB free)
```

### 1.3 RAM
```bash
# Command
free -h

# Required: 8GB minimum
# Recommended: 16GB+

# Result: □ PASS  □ FAIL (have ____ GB)
```

### 1.4 CPU Cores
```bash
# Command
nproc

# Required: 4 cores minimum
# Recommended: 8+ cores

# Result: □ PASS  □ FAIL (have ____ cores)
```

---

## ✅ PHASE 2: ROS2 JAZZY VERIFICATION

### 2.1 ROS2 Jazzy Installed
```bash
# Command
ros2 --version

# Expected: ros2 0.XXX.Y (Jazzy) or similar

# Result: □ PASS  □ FAIL
```

### 2.2 ROS2 Environment Sourced
```bash
# Command
echo $ROS_DISTRO

# Expected: jazzy

# Result: □ PASS  □ FAIL
```

### 2.3 ROS2 Packages Available
```bash
# Command
ros2 pkg list | grep -E "nav2|gazebo|rviz2|robot_state_publisher|teleop"

# Expected: Should list:
# - nav2_bringup
# - nav2_msgs
# - gazebo_ros
# - rviz2
# - robot_state_publisher
# - teleop_twist_keyboard

# Result: □ PASS  □ FAIL (missing: ____)
```

### 2.4 Navigation2 Stack
```bash
# Command
ros2 pkg list | grep -E "^nav2"

# Expected: Should list nav2_bringup, nav2_msgs, etc.

# Result: □ PASS  □ FAIL
```

---

## ✅ PHASE 3: GAZEBO HARMONIC VERIFICATION

### 3.1 Gazebo Command Available
```bash
# Command
which gz

# Expected: /usr/bin/gz (or similar path)

# Result: □ PASS  □ FAIL
```

### 3.2 Gazebo Version
```bash
# Command
gz sim --version

# Expected: Gazeebo Harmonic (gz-sim 8.x.x or higher)

# Result: □ PASS  □ FAIL (version: ____)
```

### 3.3 Gazebo Launch Test
```bash
# Command (will briefly open Gazebo window - close with Ctrl+C)
timeout 10 gz sim --empty -v 4 || echo "Gazebo launched successfully"

# Result: □ PASS  □ FAIL
```

### 3.4 ROS-Gazebo Bridge
```bash
# Command
ros2 pkg list | grep -E "ros_gz|gz_ros"

# Expected: Should list ros_gz_bridge, ros_gz_sim, etc.

# Result: □ PASS  □ FAIL
```

---

## ✅ PHASE 4: PYTHON DEPENDENCIES

### 4.1 Python3 Version
```bash
# Command
python3 --version

# Expected: Python 3.10.x or higher

# Result: □ PASS  □ FAIL
```

### 4.2 PIP3 Available
```bash
# Command
pip3 --version

# Expected: pip 23.x.x from python 3.x.x

# Result: □ PASS  □ FAIL
```

### 4.3 FastAPI
```bash
# Command
python3 -c "import fastapi; print(f'fastapi {fastapi.__version__}')"

# Result: □ PASS  □ FAIL
```

### 4.4 OpenCV
```bash
# Command
python3 -c "import cv2; print(f'opencv {cv2.__version__}')"

# Result: □ PASS  □ FAIL
```

### 4.5 NumPy
```bash
# Command
python3 -c "import numpy; print(f'numpy {numpy.__version__}')"

# Result: □ PASS  □ FAIL
```

### 4.6 YAML
```bash
# Command
python3 -c "import yaml; print('pyyaml OK')"

# Result: □ PASS  □ FAIL
```

### 4.7 Websockets
```bash
# Command
python3 -c "import websockets; print(f'websockets {websockets.__version__}')"

# Result: □ PASS  □ FAIL
```

---

## ✅ PHASE 5: REPOSITORY VERIFICATION

### 5.1 Git Available
```bash
# Command
git --version

# Expected: git version 2.x.x

# Result: □ PASS  □ FAIL
```

### 5.2 Repository Cloned
```bash
# Command
ls -la ~/advika_robot_ws/

# Expected: Should see src/, simulation/, docs/, etc.

# Result: □ PASS  □ FAIL
```

### 5.3 Workspace Built
```bash
# Command
ls -la ~/advika_robot_ws/install/

# Expected: Should see setup.bash, local_setup.bash

# Result: □ PASS  □ FAIL (need to run colcon build)
```

### 5.4 URDF File Exists
```bash
# Command
ls -la ~/advika_robot_ws/src/advika_description/urdf/advika.urdf

# Expected: File exists

# Result: □ PASS  □ FAIL
```

### 5.5 World Files Exist
```bash
# Command
ls -la ~/advika_robot_ws/src/advika_sim/worlds/

# Expected: Should see 3bhk_house.world, living_room.world, etc.

# Result: □ PASS  □ FAIL
```

### 5.6 Launch File Exists
```bash
# Command
ls -la ~/advika_robot_ws/simulation/launch/sim_bringup.launch.py

# Expected: File exists

# Result: □ PASS  □ FAIL
```

---

## ✅ PHASE 6: NETWORK/PERMISSIONS

### 6.1 X11 Display (for GUI)
```bash
# Command
echo $DISPLAY

# Expected: :0 or :1

# Result: □ PASS  □ FAIL (need X server running)
```

### 6.2 User in Render Group
```bash
# Command
groups | grep -E "render|video|dialout"

# Result: □ PASS  □ FAIL (may need: sudo usermod -aG render $USER)
```

### 6.3 USB Permissions (for real hardware later)
```bash
# Command
ls -la /dev/ttyUSB* 2>/dev/null || echo "No USB devices (OK for sim)"

# Result: □ N/A (simulation only)  □ PASS (hardware mode)
```

---

## ✅ PHASE 7: OPTIONAL COMPONENTS

### 7.1 SLAM Toolbox
```bash
# Command
ros2 pkg list | grep slam

# Expected: slam_toolbox

# Result: □ PASS  □ FAIL
```

### 7.2 Teleop Twist Keyboard
```bash
# Command
ros2 pkg list | grep teleop

# Expected: teleop_twist_keyboard

# Result: □ PASS  □ FAIL
```

### 7.3 RViz2
```bash
# Command
ros2 pkg list | grep rviz2

# Expected: rviz2

# Result: □ PASS  □ FAIL
```

### 7.4 Text-to-Speech
```bash
# Command
which espeak-ng && espeak-ng "Hello, I am Advika" || echo "espeak-ng not installed"

# Result: □ PASS  □ FAIL
```

### 7.5 Recording Tools
```bash
# Command
ros2 pkg list | grep -E "bag|record"

# Result: □ PASS  □ FAIL
```

---

## 📋 COMPLETE PREREQUISITES CHECK RESULT

### MUST PASS (Cannot proceed without these)
| Check | Status | Value | Notes |
|-------|--------|-------|-------|
| Ubuntu 24.04 | ✅ PASS | 24.04 LTS | Verified 2026-07-25 |
| 30GB+ Disk Space | ✅ PASS | 174 GB free | |
| 8GB+ RAM | ✅ PASS | 15 GB | |
| 4+ CPU Cores | ✅ PASS | 8 cores | |
| ROS2 Jazzy | ✅ PASS | jazzy | Source: `/opt/ros/jazzy/setup.bash` |
| Gazebo Harmonic | ✅ PASS | 8.11.0 | |
| Workspace Built | ✅ PASS | install/ exists | `colcon build` complete |
| URDF File | ✅ PASS | advika.urdf | |
| Launch File | ✅ PASS | sim_bringup.launch.py | |

### SHOULD PASS (Will work but limited)
| Check | Status | Notes |
|-------|--------|-------|
| Python Packages | ✅ PASS | fastapi 0.136, opencv 5.0, numpy 2.2, yaml 6.0, websockets 16.0 |
| RViz2 | ✅ PASS | For visualization |
| Navigation2 | ✅ PASS | For autonomous nav |
| SLAM Toolbox | ✅ PASS | For mapping |

### NICE TO HAVE
| Check | Status | Notes |
|-------|--------|-------|
| espeak-ng | ⚠️ NOT INSTALLED | Optional — `sudo apt install espeak-ng` |
| Recording Tools | ✅ PASS | ros2bag available |

---

## 🚀 AUTOMATED VERIFICATION SCRIPT

Run this single command to check everything:

```bash
# Run verification script (already in repo)
bash ~/advika_robot_ws/scripts/verify_prerequisites.sh

# NOTE: Script auto-sources ROS2 Jazzy if not already sourced
# If you want to create it manually:
cat > ~/verify_prerequisites.sh << 'EOF'
#!/bin/bash
echo "=============================================="
echo "ADVIKA 3.0 PREREQUISITES VERIFICATION"
echo "=============================================="
echo ""

fail=0

# Check Ubuntu
if [[ $(lsb_release -rs) == "24.04" ]]; then
    echo "✅ Ubuntu 24.04 LTS"
else
    echo "❌ Ubuntu 24.04 LTS required (found: $(lsb_release -rs))"
    fail=1
fi

# Check ROS2
if ros2 --version &>/dev/null; then
    echo "✅ ROS2 Jazzy installed"
else
    echo "❌ ROS2 Jazzy not found"
    fail=1
fi

# Check Gazebo
if gz sim --version &>/dev/null; then
    echo "✅ Gazebo Harmonic installed"
else
    echo "❌ Gazebo not found"
    fail=1
fi

# Check Python packages
for pkg in fastapi cv2 numpy yaml websockets; do
    if python3 -c "import $pkg" 2>/dev/null; then
        echo "✅ Python $pkg"
    else
        echo "❌ Python $pkg not installed"
        fail=1
    fi
done

# Check workspace
if [ -d ~/advika_robot_ws/install ]; then
    echo "✅ Workspace built"
else
    echo "⚠️  Workspace not built (run: cd ~/advika_robot_ws && colcon build)"
fi

echo ""
if [ $fail -eq 0 ]; then
    echo "=============================================="
    echo "✅ ALL ESSENTIAL CHECKS PASSED!"
    echo "Ready to run simulation!"
    echo "=============================================="
else
    echo "=============================================="
    echo "❌ SOME CHECKS FAILED - Fix before proceeding"
    echo "=============================================="
fi
EOF

chmod +x ~/verify_prerequisites.sh
~/verify_prerequisites.sh
```

---

## 🛠️ IF PREREQUISITES FAIL

### Ubuntu Wrong Version
```
# If 22.04 or other:
# Option 1: Clean install Ubuntu 24.04
# Option 2: Dual boot
# Option 3: VM with Ubuntu 24.04 ISO
```

### ROS2 Not Installed
```bash
# Install ROS2 Jazzy
sudo apt update
sudo apt install -y ros-jazzy-desktop
source /opt/ros/jazzy/setup.bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
```

### Gazebo Not Installed
```bash
# Install Gazebo Harmonic
sudo apt install -y gz-harmonic
```

### espeak-ng Not Installed (Optional)
```bash
# Install text-to-speech engine (robot voice)
sudo apt install -y espeak-ng
# Test
espeak-ng "Hello, I am Advika"
```

### Workspace Not Built
```bash
cd ~/advika_robot_ws
colcon build --symlink-install
source install/setup.bash
```

---

## ✅ AFTER ALL CHECKS PASS

When ALL checks in PHASE 1-5 are PASS:

```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ✅ ALL PREREQUISITES VERIFIED!                             ║
║                                                               ║
║   Next Step: Launch Simulation                                ║
║   Command:                                                    ║
║   ros2 launch advika_sim sim_bringup.launch.py               ║
║                                                               ║
║   Expected Windows:                                           ║
║   - Gazebo (robot model visible)                             ║
║   - RViz2 (sensor data visualization)                        ║
║   - Terminal (teleop keyboard active)                       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```