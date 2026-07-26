#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# ADVIKA 3.0 — FULL SYSTEM LAUNCH (4-QUADRANT)
# ═══════════════════════════════════════════════════════════════════
# Opens: Gazebo Sim | RViz2 | Web Dashboard | Terminal
# Requires: ROS2 Jazzy, Gazebo Harmonic, terminator (or tmux)
#
# Usage:
#   bash src/advika_sim/scripts/launch_full_system.sh [world_name]
#
# Defaults to: 3bhk_house.world
# ═══════════════════════════════════════════════════════════════════

set -e

WORLD_NAME="${1:-3bhk_house.world}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WS_DIR="$(dirname "$SCRIPT_DIR")"         # advika_robot_ws root
PKG_ADVIKA_SIM="$(find "$WS_DIR/src" -type d -name advika_sim 2>/dev/null | head -1)"
PKG_ADVIKA_DESC="$(find "$WS_DIR/src" -type d -name advika_description 2>/dev/null | head -1)"
PKG_ADVIKA_DASH="$(find "$WS_DIR/src" -type d -name advika_dashboard 2>/dev/null | head -1)"

WORLD_PATH="$PKG_ADVIKA_SIM/worlds/$WORLD_NAME"
if [ ! -f "$WORLD_PATH" ]; then
  echo "ERROR: World not found: $WORLD_PATH"
  echo "Available worlds:"
  find "$PKG_ADVIKA_SIM/worlds" -name "*.world" 2>/dev/null | while read w; do
    echo "  - $(basename $w)"
  done
  exit 1
fi

echo "=============================================="
echo "ADVIKA 3.0 — FULL SYSTEM LAUNCH"
echo "  World:    $WORLD_NAME"
echo "  Gazebo:   $(which gz 2>/dev/null || echo 'not found')"
echo "  ROS2:     ${ROS_DISTRO:-unknown}"
echo "=============================================="

# Source ROS2
if [ -f /opt/ros/jazzy/setup.bash ]; then
  source /opt/ros/jazzy/setup.bash
elif [ -f /opt/ros/humble/setup.bash ]; then
  source /opt/ros/humble/setup.bash
fi

# Source workspace
if [ -f "$WS_DIR/install/setup.bash" ]; then
  source "$WS_DIR/install/setup.bash"
fi

# ── Check terminator or fall back to tmux ────────────────────────────────────
OPEN_TERMINAL=""
if command -v terminator &>/dev/null; then
  OPEN_TERMINAL="terminator"
elif command -v gnome-terminal &>/dev/null; then
  OPEN_TERMINAL="gnome-terminal"
elif command -v konsole &>/dev/null; then
  OPEN_TERMINAL="konsole"
elif command -v xfce4-terminal &>/dev/null; then
  OPEN_TERMINAL="xfce4-terminal"
fi

# ── Launch ────────────────────────────────────────────────────────────────────
echo ""
echo "Launching 4-quadrant layout..."

# Quadrant 1 — Gazebo Sim (top-left, large)
if command -v gz &>/dev/null; then
  gz sim -r -v 4 "$WORLD_PATH" &
  echo "  [1] Gazebo started (PID $!)"
elif command -v gazebo &>/dev/null; then
  echo "  WARNING: Using classic gazebo (not Gazebo Harmonic)"
  # No-pretty fallback for classic
fi

sleep 1

# Quadrant 2 — RViz2 (top-right)
rviz2 --empty-validation &
echo "  [2] RViz2 started (PID $!)"

# Quadrant 3 — Web Dashboard (bottom-left)
if [ -n "$PKG_ADVIKA_DASH" ] && [ -f "$PKG_ADVIKA_DASH/advika_dashboard/dashboard.py" ]; then
  (cd "$PKG_ADVIKA_DASH" && python3 advika_dashboard/dashboard.py) &
  echo "  [3] Dashboard started (PID $!) — open http://localhost:5000"
else
  echo "  [3] Dashboard: package not found, skipping"
fi

# Quadrant 4 — Terminal (bottom-right) — give it a command that keeps it open
if [ -n "$OPEN_TERMINAL" ]; then
  $OPEN_TERMINAL --tab -t "ADVIKA Shell" \
    --working-directory="$WS_DIR" \
    -e "bash -c 'echo ADVIKA 3.0 Ready; echo Source your workspace: source install/setup.bash; echo Commands: ros2 topic list | grep advika; exec bash'" &
  echo "  [4] Terminal started (PID $!)"
else
  echo "  [4] Terminal: terminator/tmux not found — run 'bash' manually"
fi

echo ""
echo "=============================================="
echo "All windows launched!"
echo "  Dashboard: http://localhost:5000"
echo "  RViz:      rviz2 (manual open)"
echo "  Gazebo:    gz sim"
echo ""
echo "Press Ctrl+C in THIS terminal to stop everything."
echo "=============================================="

# Wait for any process to exit, then kill all children
wait