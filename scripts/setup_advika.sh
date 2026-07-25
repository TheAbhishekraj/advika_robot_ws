#!/bin/bash
# =============================================================================
# ADVIKA 3.0 - SINGLE COMMAND SETUP
# =============================================================================
# This script automates:
#   1. Clone repository to specified folder
#   2. Install all dependencies
#   3. Build workspace
#   4. Verify installation
#
# Usage:
#   bash <(curl -fsSL <RAW_URL>)           # Download and run
#   ./setup_advika.sh                      # Run locally
#   ./setup_advika.sh --dir /path/to/clone # Custom directory
#
# =============================================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
CLONE_DIR="$HOME/advika_robot_ws"
REPO_URL="https://github.com/TheAbhishekraj/advika_robot_ws.git"
BRANCH="main"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dir)
            CLONE_DIR="$2"
            shift 2
            ;;
        --url)
            REPO_URL="$2"
            shift 2
            ;;
        --branch)
            BRANCH="$2"
            shift 2
            ;;
        --help|-h)
            echo "Usage: $0 [--dir <path>] [--url <git-url>] [--branch <branch>]"
            echo "  --dir   Directory to clone into (default: ~/advika_robot_ws)"
            echo "  --url   Git repository URL (default: $REPO_URL)"
            echo "  --branch Git branch (default: main)"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}║       ADVIKA 3.0 SIMULATION - AUTOMATED SETUP                ║${NC}"
echo -e "${BLUE}║                                                                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Check OS
echo -e "${YELLOW}[1/6] Checking OS...${NC}"
if [[ $(lsb_release -rs) != "24.04" ]]; then
    echo -e "${RED}❌ ERROR: Ubuntu 24.04 LTS required!${NC}"
    echo -e "${RED}  Current: $(lsb_release -ds)${NC}"
    echo -e "${RED}  Please install Ubuntu 24.04 LTS first.${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Ubuntu 24.04 LTS verified${NC}"
echo ""

# Step 2: Clone or Update Repository
echo -e "${YELLOW}[2/6] Setting up repository...${NC}"

if [ -d "$CLONE_DIR/.git" ]; then
    echo -e "${YELLOW}Repository already exists at $CLONE_DIR${NC}"
    echo -e "${YELLOW}Updating...${NC}"
    cd "$CLONE_DIR"
    git checkout $BRANCH 2>/dev/null || true
    git pull origin $BRANCH
else
    echo -e "${YELLOW}Cloning repository to $CLONE_DIR...${NC}"
    git clone -b $BRANCH $REPO_URL "$CLONE_DIR"
    cd "$CLONE_DIR"
fi
echo -e "${GREEN}✅ Repository ready${NC}"
echo ""

# Step 3: Install System Dependencies
echo -e "${YELLOW}[3/6] Installing system dependencies (requires sudo)...${NC}"
echo -e "${YELLOW}This may take 10-20 minutes depending on your connection...${NC}"

sudo apt update

sudo apt install -y \
    ros-jazzy-desktop \
    ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup \
    ros-jazzy-slam-toolbox \
    ros-jazzy-ros-gz \
    ros-jazzy-teleop-twist-keyboard \
    ros-jazzy-robot-state-publisher \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-xacro \
    ros-jazzy-rviz2 \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controller \
    ros-jazzy-diff-drive-controller \
    ros-jazzy-joint-state-broadcaster \
    gz-harmonic \
    espeak-ng \
    python3-pip \
    xterm \
    && echo -e "${GREEN}✅ System packages installed${NC}" || {
        echo -e "${RED}❌ Failed to install system packages${NC}"
        exit 1
    }
echo ""

# Step 4: Install Python Dependencies
echo -e "${YELLOW}[4/6] Installing Python dependencies...${NC}"
pip3 install -r "$CLONE_DIR/requirements.txt" --break-system-packages \
    && echo -e "${GREEN}✅ Python packages installed${NC}" || {
        echo -e "${RED}❌ Failed to install Python packages${NC}"
        exit 1
    }
echo ""

# Step 5: Build Workspace
echo -e "${YELLOW}[5/6] Building ROS2 workspace...${NC}"
echo -e "${YELLOW}This may take 5-10 minutes...${NC}"

source /opt/ros/jazzy/setup.bash
cd "$CLONE_DIR"
colcon build --symlink-install 2>&1 | tee /tmp/build.log

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✅ Workspace built successfully${NC}"
else
    echo -e "${RED}❌ Build failed. Check /tmp/build.log for details${NC}"
    echo -e "${RED}Common issues:${NC}"
    echo -e "${RED}  - Missing ROS2 packages: Run 'source /opt/ros/jazzy/setup.bash' first${NC}"
    echo -e "${RED}  - Missing dependencies: Run 'rosdep install --from-paths src --ignore-src -r -y'${NC}"
    exit 1
fi
echo ""

# Step 6: Verify Installation
echo -e "${YELLOW}[6/6] Verifying installation...${NC}"

source "$CLONE_DIR/install/setup.bash"

PASS=0
FAIL=0

# Check ROS2
if ros2 --version &>/dev/null; then
    echo -e "${GREEN}✅ ROS2 Jazzy${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ ROS2 Jazzy not found${NC}"
    ((FAIL++))
fi

# Check Gazebo
if gz sim --version &>/dev/null; then
    echo -e "${GREEN}✅ Gazebo Harmonic${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ Gazebo not found${NC}"
    ((FAIL++))
fi

# Check workspace
if [ -f "$CLONE_DIR/install/setup.bash" ]; then
    echo -e "${GREEN}✅ Workspace built${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ Workspace not built${NC}"
    ((FAIL++))
fi

# Check URDF
if [ -f "$CLONE_DIR/src/advika_description/urdf/advika.urdf" ] || \
   [ -f "$CLONE_DIR/simulation/urdf/advika.urdf" ]; then
    echo -e "${GREEN}✅ URDF file found${NC}"
    ((PASS++))
else
    echo -e "${RED}❌ URDF file not found${NC}"
    ((FAIL++))
fi

echo ""

# Final Status
if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}║           ✅ SETUP COMPLETE! ALL CHECKS PASSED!                ║${NC}"
    echo -e "${GREEN}║                                                                ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Next Steps:${NC}"
    echo -e "  1. Source the workspace: ${YELLOW}source $CLONE_DIR/install/setup.bash${NC}"
    echo -e "  2. Launch simulation:    ${YELLOW}ros2 launch advika_sim sim_bringup.launch.py${NC}"
    echo -e "  3. Drive robot:          ${YELLOW}ros2 run teleop_twist_keyboard teleop_twist_keyboard${NC}"
    echo ""
    echo -e "${BLUE}Add to ~/.bashrc for convenience:${NC}"
    echo -e "  echo 'source $CLONE_DIR/install/setup.bash' >> ~/.bashrc"
    echo ""
else
    echo -e "${RED}╔════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║                                                                ║${NC}"
    echo -e "${RED}║           ❌ SETUP INCOMPLETE - FIX ERRORS ABOVE                ║${NC}"
    echo -e "${RED}║                                                                ║${NC}"
    echo -e "${RED}╚════════════════════════════════════════════════════════════════╝${NC}"
    echo -e "${RED}Passed: $PASS, Failed: $FAIL${NC}"
    exit 1
fi