# CHANGELOG — Advika 3.0

All notable changes to this project will follow [Semantic Versioning](https://semver.org/).

---

## [Unreleased] — v0.2.0

### Added
- `src/` ROS2 workspace with all 8 packages scaffolded:
  - `advika_bringup` — top-level launch configuration
  - `advika_description` — URDF robot model
  - `advika_hardware` — ESP32 bridge + sensor nodes
  - `advika_navigation` — Nav2 + SLAM configuration
  - `advika_sensors` — LD06, ToF, IMU, camera drivers
  - `advika_sim` — Gazebo simulation + HITL dashboard
  - `advika_viz` — RViz configs
  - `advika_msgs` — custom message definitions
- `TROUBLESHOOTING.md` — comprehensive debug guide (6 categories)
- `CHANGELOG.md` — this file
- `docs/LED_STATUS.md` — LED patterns reference
- `logbook/`, `checkpoints/`, `pdca/`, `photos/` directories
- `.github/workflows/ci.yml` — GitHub Actions CI (build + lint)
- `.pre-commit-config.yaml` — black + flake8 pre-commit hooks

### Fixed
- `simulation/launch/sim_bringup.launch.py` — workspace path now uses `os.path.realpath` to support symlinks

### Changed
- LiDAR confirmed as **LD06** (230400 baud) — documentation aligned

---

## [0.1.0] — 2026-07-23 — Initial Upload

### Added
- Complete Gazebo Harmonic simulation stack (`sim_bringup.launch.py`)
- URDF robot model (`simulation/urdf/advika.urdf`)
- Gazebo world (`simulation/gazebo_worlds/advika_playground.world`)
- Nav2 params (`simulation/config/nav2_params.yaml`)
- SLAM Toolbox params (`simulation/config/slam_params.yaml`)
- HITL dashboard (`simulation/hitl/`)
- MCP servers (`mcp_servers/hardware_bridge.py`, `vision_bridge.py`)
- ESP32 firmware (`firmware/esp32_motor_bridge/`)
- Hardware diagnostics (`scripts/test_peripherals.py`)
- Launch orchestration (`scripts/launch_robot.sh`)
- Robot params (`config/robot_params.yaml`)
- AI agent spec (`CLAUDE.md`)
- Child manual (`manuals/i_am_5/` — 6 chapters)
- Hardware docs (`docs/CAD_README.md`, `docs/Wiring_README.md`)

---

*Format: [Keep a Changelog](https://keepachangelog.com/)*
