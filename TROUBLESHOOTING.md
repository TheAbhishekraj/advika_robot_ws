# TROUBLESHOOTING — Advika 3.0

## Table of Contents
1. [Simulation Issues](#simulation-issues)
2. [Hardware / ESP32 Issues](#hardware--esp32-issues)
3. [ROS2 Issues](#ros2-issues)
4. [Sensor Issues](#sensor-issues)
5. [Navigation Issues](#navigation-issues)
6. [Safety System Issues](#safety-system-issues)

---

## Simulation Issues

### Gazebo doesn't open / hangs on launch
```
Symptom: gz sim freezes or no window appears
Fix:
  export GZ_SIM_RESOURCE_PATH=~/advika_robot_ws/simulation
  pkill -9 gz ; pkill -9 ign    # kill stale instances
  ros2 launch simulation/launch/sim_bringup.launch.py
```

### Robot fails to spawn in Gazebo
```
Symptom: "Entity not found" or robot not visible
Root cause: sim_bringup waits 3s for Gazebo — may need more on slow machines
Fix: In sim_bringup.launch.py increase TimerAction period from 3.0 to 6.0
```

### HITL dashboard not loading (http://localhost:8080)
```
Symptom: Browser shows "connection refused"
Fix:
  # Check if hitl_server started:
  ros2 node list | grep hitl
  # If missing, start manually:
  python3 simulation/hitl/hitl_bridge.py
```

### `launch.actions` import error in IDE
```
Symptom: IDE shows "Cannot find module launch.actions"
Root cause: These modules only exist in the ROS2 sourced Python path, not system Python.
Fix (IDE): Add /opt/ros/jazzy/lib/python3.12/site-packages to your Python path settings.
Fix (Runtime): source /opt/ros/jazzy/setup.bash   ← this is sufficient
```

---

## Hardware / ESP32 Issues

### ESP32 not detected (`/dev/ttyUSB0` missing)
```
Symptom: serial.SerialException: [Errno 2] No such file or directory
Fix:
  sudo adduser $USER dialout && newgrp dialout
  # Reconnect USB, then:
  ls /dev/ttyUSB*
```

### Firmware upload fails (PlatformIO)
```
Symptom: "Error: Timed out waiting for packet header"
Fix:
  # Hold BOOT button on ESP32 during upload start, release after "Connecting..."
  cd firmware/esp32_motor_bridge && pio run --target upload
```

### Motors not responding after firmware flash
```
Symptom: No motor movement but ESP32 connected
Fix: Check DRV8833 enable pin. Send test command:
  python3 -c "
  import serial, json
  s = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
  cmd = {'method': 'drive', 'params': {'linear': 0.1, 'angular': 0.0, 'duration_ms': 500}}
  s.write((json.dumps(cmd) + '\n').encode())
  print(s.readline())
  "
```

### Safety watchdog firing immediately
```
Symptom: Motors halt instantly after any command
Root cause: ToF reading < 120mm (object too close) or no serial data
Fix:
  python3 scripts/test_peripherals.py   # check all 9 sensors
  # Clear obstructions from ToF sensors, reboot ESP32
```

---

## ROS2 Issues

### `colcon build` fails — package not found
```
Symptom: "Package 'advika_sim' not found"
Fix:
  source /opt/ros/jazzy/setup.bash
  cd ~/advika_robot_ws
  colcon build --symlink-install
  source install/setup.bash
```

### `ros2 topic list` shows nothing
```
Symptom: Empty topic list even after launch
Fix:
  echo $ROS_DOMAIN_ID    # should be 42
  # If empty:
  export ROS_DOMAIN_ID=42
  # Add to ~/.bashrc permanently
```

### TF tree broken / RViz shows no robot
```
Symptom: RViz "No transform from [base_link] to [map]"
Fix:
  ros2 run tf2_tools view_frames   # generate frames.gv
  # Check robot_state_publisher is running:
  ros2 node list | grep robot_state
  # Re-launch if missing
```

### Nav2 not reaching goal
```
Symptom: Robot plans path but stops short
Fix: Check costmap inflation_radius in simulation/config/nav2_params.yaml
     Increase recovery_radius if robot gets stuck in local minima
```

---

## Sensor Issues

### LiDAR scan not publishing (`/advika/scan` silent)
```
Port: /dev/ttyUSB1, Baud: 230400 (LD06)
Fix:
  # Test raw data:
  python3 -c "import serial; s=serial.Serial('/dev/ttyUSB1',230400); [print(s.readline()) for _ in range(5)]"
  # If no data: check USB cable, try different port (/dev/ttyUSB0)
```

### ToF sensors reading 0 or max (4000mm)
```
Symptom: All 8x8 cells stuck at 0 or 4000
Fix:
  # Check I2C:
  i2cdetect -y 1   # should show 0x52
  # If not found: check SDA(GPIO8)/SCL(GPIO9) wiring on ESP32
```

### Cameras not streaming
```
Camera 1: /dev/video0 (horizon, 75°)
Camera 2: /dev/video2 (floor, 120°)
Fix:
  ls /dev/video*    # confirm device nodes exist
  sudo adduser $USER video
  python3 -c "import cv2; c=cv2.VideoCapture(0); print(c.read())"
```

---

## Navigation Issues

### SLAM map drifting
```
Symptom: Map shows walls duplicated or misaligned
Fix: Drive SLOWER during mapping (max 0.2 m/s)
     Ensure LiDAR scan rate is 10Hz: ros2 topic hz /advika/scan
     Increase map_update_interval in slam_params.yaml
```

### AMCL not converging (robot lost)
```
Fix:
  1. Use RViz "2D Pose Estimate" to set rough initial position
  2. Drive robot slowly to accumulate scan matches
  3. Increase max_particles from 2000 to 5000 in nav2_params.yaml
```

---

## Safety System Issues

### E-Stop not responding
```
CRITICAL — Check immediately:
1. Verify E-Stop button wired to GPIO 14 with pull-up
2. Check motor driver enable pin connected to ESP32 ISR output
3. Test: Press button, LED should turn RED, motors stop < 1ms
4. Check safety_interrupt.h — ISR must be IRAM_ATTR
```

### `/var/log/advika/decisions.jsonl` permission denied
```
Fix:
  sudo mkdir -p /var/log/advika
  sudo chown $USER:$USER /var/log/advika
```

---

*Last Updated: 2026-07-24 | Version: 0.1.0*
