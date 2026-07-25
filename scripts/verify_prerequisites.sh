#!/bin/bash
echo "=============================================="
echo "ADVIKA 3.0 PREREQUISITES VERIFICATION"
echo "=============================================="
echo ""

fail=0

# Source ROS2 if not already sourced
if [ -z "$ROS_DISTRO" ]; then
    if [ -f /opt/ros/jazzy/setup.bash ]; then
        source /opt/ros/jazzy/setup.bash
    fi
fi

# Check Ubuntu
if [[ $(lsb_release -rs) == "24.04" ]]; then
    echo "✅ Ubuntu 24.04 LTS"
else
    echo "❌ Ubuntu 24.04 LTS required (found: $(lsb_release -rs))"
    fail=1
fi

# Check Disk Space (minimum 30GB free)
FREE_GB=$(df -BG / | awk 'NR==2 {gsub("G",""); print $4}')
if [ "$FREE_GB" -ge 30 ] 2>/dev/null; then
    echo "✅ Disk space: ${FREE_GB}GB free"
else
    echo "⚠️  Disk space: ${FREE_GB}GB free (recommend 30GB+)"
fi

# Check RAM (minimum 8GB)
RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
if [ "$RAM_GB" -ge 8 ] 2>/dev/null; then
    echo "✅ RAM: ${RAM_GB}GB"
else
    echo "⚠️  RAM: ${RAM_GB}GB (recommend 8GB+)"
fi

# Check CPU Cores
CORES=$(nproc)
if [ "$CORES" -ge 4 ] 2>/dev/null; then
    echo "✅ CPU Cores: $CORES"
else
    echo "⚠️  CPU Cores: $CORES (recommend 4+)"
fi

# Check ROS2 Jazzy
if [ "$ROS_DISTRO" == "jazzy" ]; then
    ROS_VER=$(ros2 --version 2>/dev/null || echo "unknown")
    echo "✅ ROS2 Jazzy installed ($ROS_VER)"
elif ros2 --version &>/dev/null; then
    echo "⚠️  ROS2 installed but distro is: $ROS_DISTRO (expected: jazzy)"
else
    echo "❌ ROS2 Jazzy not found"
    echo "   Fix: sudo apt install ros-jazzy-desktop"
    fail=1
fi

# Check Gazebo Harmonic
if gz sim --version &>/dev/null 2>&1; then
    GZ_VER=$(gz sim --version 2>&1 | head -1)
    echo "✅ Gazebo Harmonic installed ($GZ_VER)"
else
    echo "❌ Gazebo not found"
    echo "   Fix: sudo apt install gz-harmonic"
    fail=1
fi

# Check ROS-Gazebo bridge
if ros2 pkg list 2>/dev/null | grep -q "ros_gz_bridge"; then
    echo "✅ ROS-Gazebo bridge installed"
else
    echo "❌ ros_gz_bridge not found"
    echo "   Fix: sudo apt install ros-jazzy-ros-gz"
    fail=1
fi

# Check Python packages
echo ""
echo "--- Python packages ---"
for pkg in fastapi cv2 numpy yaml websockets; do
    if python3 -c "import $pkg" 2>/dev/null; then
        VER=$(python3 -c "import $pkg; print(getattr($pkg, '__version__', 'OK'))" 2>/dev/null)
        echo "✅ Python $pkg ($VER)"
    else
        echo "❌ Python $pkg not installed"
        fail=1
    fi
done

# Check workspace
echo ""
echo "--- Workspace ---"
if [ -d ~/advika_robot_ws/install ] && [ -f ~/advika_robot_ws/install/setup.bash ]; then
    echo "✅ Workspace built"
else
    echo "⚠️  Workspace not built"
    echo "   Fix: cd ~/advika_robot_ws && colcon build --symlink-install"
fi

# Check URDF
if [ -f ~/advika_robot_ws/src/advika_description/urdf/advika.urdf ]; then
    echo "✅ URDF file exists"
else
    echo "⚠️  URDF file not found (src/advika_description/urdf/advika.urdf)"
fi

# Check world files
if ls ~/advika_robot_ws/src/advika_sim/worlds/*.world 2>/dev/null | head -1 | grep -q ".world"; then
    echo "✅ World files exist"
else
    echo "⚠️  World files not found (src/advika_sim/worlds/)"
fi

# Check optional tools
echo ""
echo "--- Optional Tools ---"
ros2 pkg list 2>/dev/null | grep -q "slam_toolbox" && echo "✅ SLAM Toolbox" || echo "⚠️  slam_toolbox not installed (sudo apt install ros-jazzy-slam-toolbox)"
ros2 pkg list 2>/dev/null | grep -q "teleop_twist_keyboard" && echo "✅ teleop_twist_keyboard" || echo "⚠️  teleop_twist_keyboard not installed"
ros2 pkg list 2>/dev/null | grep -q "^rviz2" && echo "✅ RViz2" || echo "⚠️  rviz2 not installed"
which espeak-ng 2>/dev/null && echo "✅ espeak-ng (TTS)" || echo "⚠️  espeak-ng not installed (optional)"

echo ""
echo "=============================================="
if [ $fail -eq 0 ]; then
    echo "✅ ALL ESSENTIAL CHECKS PASSED!"
    echo "Ready to run: ros2 launch advika_sim sim_bringup.launch.py"
else
    echo "❌ SOME CHECKS FAILED - Fix before proceeding"
fi
echo "=============================================="
