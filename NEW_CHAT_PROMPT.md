=============================================================
ADVIKA 3.0 — NEXT SESSION LAUNCH PROMPT
Use this at the start of every new AI chat session.
=============================================================

PROJECT: Advika 3.0 — Agentic Autonomous Mobile Robot
REPO: TheAbhishekraj/advika_robot_ws
PATH: /home/abhishek/Documents/Robotics/advika_robot_ws
SYMLINK: ~/advika_robot_ws → above path (already created)
PLATFORM: Raspberry Pi 5 (8GB), Ubuntu 24.04, ROS2 Jazzy
REFERENCE KIT: /home/abhishek/Documents/Robotics/advika30_project_kit

-------------------------------------------------------------
CURRENT STATUS (as of 2026-07-24)
-------------------------------------------------------------
Phase: Phase 3 — Software & ROS2 (in progress)
Audit Score: 52/100 → targeting 70/100 for v1.0

DONE THIS SESSION:
✅ src/ with all 8 ROS2 packages scaffolded (package.xml + setup.py)
   - advika_sim      ← sim, HITL, MCP bridge (MOST IMPORTANT)
   - advika_bringup  ← launch files
   - advika_description ← URDF/xacro
   - advika_hardware ← ESP32 bridge node
   - advika_navigation ← Nav2 + SLAM
   - advika_sensors  ← LD06, ToF, IMU, cameras
   - advika_viz      ← RViz configs
   - advika_msgs     ← custom messages
✅ sim_bringup.launch.py path fix (os.path.realpath)
✅ TROUBLESHOOTING.md, CHANGELOG.md, docs/LED_STATUS.md
✅ .github/workflows/ci.yml (GitHub Actions, ROS2 Jazzy)
✅ .pre-commit-config.yaml (black + flake8)
✅ logbook/, checkpoints/, pdca/, photos/ dirs created

STILL NEEDED (user must do in terminal):
1. sudo mkdir -p /var/log/advika /var/run/advika
   sudo chown $USER:$USER /var/log/advika /var/run/advika
2. echo 'export ROS_DOMAIN_ID=42' >> ~/.bashrc && source ~/.bashrc
3. source /opt/ros/jazzy/setup.bash && cd ~/advika_robot_ws
   colcon build --symlink-install
4. git push origin main
5. git tag -a v0.2.0 -m "feat: ROS2 packages, CI, docs"

-------------------------------------------------------------
TO LAUNCH SIMULATION NOW (after colcon build):
-------------------------------------------------------------
source /opt/ros/jazzy/setup.bash
source ~/advika_robot_ws/install/setup.bash
ros2 launch simulation/launch/sim_bringup.launch.py

# What starts:
# T+0s   → Gazebo Harmonic (advika_playground.world)
# T+3s   → Robot spawned, gz_bridge active
# T+4s   → Safety monitor
# T+5s   → SLAM Toolbox
# T+6s   → sim_mcp_bridge
# T+8s   → HITL dashboard → http://localhost:8080
# T+10s  → Nav2 stack

# Test all 5 scenarios:
python3 simulation/scripts/run_scenario.py --all

-------------------------------------------------------------
KEY FILES (know these):
-------------------------------------------------------------
CLAUDE.md              ← AI agent identity + 4 MCP tools
config/robot_params.yaml ← ALL hardware params (modify here)
simulation/launch/sim_bringup.launch.py ← main launch
simulation/config/nav2_params.yaml ← Nav2 tuning
simulation/config/slam_params.yaml ← SLAM config
simulation/urdf/advika.urdf ← robot model
scripts/test_peripherals.py ← hardware diagnostics
scripts/launch_robot.sh ← hardware start/stop
mcp_servers/hardware_bridge.py ← ESP32 MCP server
TROUBLESHOOTING.md ← debug guide
docs/LED_STATUS.md ← LED pattern reference

-------------------------------------------------------------
HARDWARE LAUNCH (when physical robot ready):
-------------------------------------------------------------
# 1. Flash ESP32
cd ~/advika_robot_ws/firmware/esp32_motor_bridge && pio run --target upload

# 2. Test all peripherals (must ALL pass)
python3 scripts/test_peripherals.py

# 3. Start MCP servers + robot
bash scripts/launch_robot.sh start

# Monitor:
bash scripts/launch_robot.sh status
bash scripts/launch_robot.sh stop

-------------------------------------------------------------
NEXT BUILD TASKS (in priority order):
-------------------------------------------------------------
[ ] colcon build — get workspace compiling green
[ ] Test sim launch end-to-end (Gazebo + Nav2 + HITL)
[ ] Fill logbook: logbook/2026-07-24_phase-3_step-06_simulation.md
[ ] Create advika_hardware esp32_bridge_node.py (Phase 3 Step 3.5)
[ ] Create advika_sensors driver nodes (LD06, ToF, IMU, cameras)
[ ] Run SLAM in sim, save map, test autonomous navigation
[ ] Fill checkpoint: checkpoints/phase-3_CP3.5.md
[ ] Migrate URDF to xacro (parameterised)
[ ] Add pytest unit tests in each package test/ dir
[ ] Set up Docker (from RECOMMENDED_ADDITIONS.md #2)
[ ] Flash ESP32 + test real hardware

-------------------------------------------------------------
AUDIT GAP TARGETS:
-------------------------------------------------------------
Category C ROS2 (3/10) → build packages → target 7/10
Category E Testing (1/10) → add pytest → target 5/10
Category I Git (3/10) → add tags+release → target 7/10
Overall target: 70/100 (Pre-Release)

Reference: advika30_project_kit/audit/REPOSITORY_AUDIT.md

=============================================================