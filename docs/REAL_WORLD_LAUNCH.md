# Advika 3.0 Real-World Launch Guide

This file provides a practical launch sequence for physical robot bring-up.

## 1) Pre-Launch Checks

1. Power on Raspberry Pi and ESP32 motor controller.
2. Verify E-Stop physical button operation.
3. Confirm connected devices:
   - ESP32 serial (`/dev/ttyUSB0` by default)
   - LD06 LiDAR (`/dev/ttyUSB1` by default)
   - Dual cameras (`/dev/video0`, `/dev/video2`)
4. Ensure required env vars are exported if device paths differ.

## 2) Flash Firmware (when needed)

```bash
cd /home/runner/work/advika_robot_ws/advika_robot_ws/firmware/esp32_motor_bridge
pio run --target upload
```

## 3) Run Hardware Diagnostics

```bash
cd /home/runner/work/advika_robot_ws/advika_robot_ws
python3 scripts/test_peripherals.py
```

Do not proceed until critical tests (ESP32, LiDAR, E-Stop, cameras) pass.

## 4) Start MCP Bridges

```bash
cd /home/runner/work/advika_robot_ws/advika_robot_ws
python3 mcp_servers/hardware_bridge.py
```

In a second terminal:

```bash
cd /home/runner/work/advika_robot_ws/advika_robot_ws
python3 mcp_servers/vision_bridge.py
```

## 5) Launch Robot Runtime

```bash
cd /home/runner/work/advika_robot_ws/advika_robot_ws
bash scripts/launch_robot.sh start
```

## 6) Optional HITL Supervision

```bash
cd /home/runner/work/advika_robot_ws/advika_robot_ws
python3 simulation/hitl/hitl_bridge.py --both
```

Open dashboard: `http://localhost:8080`

Set emergency reset token for secure emergency unlock:

```bash
export HITL_EMERGENCY_RESET_TOKEN='set-a-strong-token'
```

## 7) Safety Rules During Real Runs

1. Keep clear physical perimeter around the robot.
2. Keep E-Stop accessible at all times.
3. Start in supervised mode before any full-auto run.
4. Verify `/var/log/advika/decisions.jsonl` is being written.

## 8) Shutdown

```bash
cd /home/runner/work/advika_robot_ws/advika_robot_ws
bash scripts/launch_robot.sh stop
```

Then stop MCP and HITL processes.
