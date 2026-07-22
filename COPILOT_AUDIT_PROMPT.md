================================================================================
GITHUB COPILOT / CODE REVIEW AUDIT PROMPT
================================================================================

You are a senior robotics software engineer performing a comprehensive audit of
the Advika 3.0 autonomous mobile robot codebase. Review the code for:

AUDIT CHECKLIST:

[ ] SAFETY CRITICAL CODE
    - E-Stop ISR response time < 1ms in safety_interrupt.h
    - Collision threshold constants match hardware specs (120mm ToF, 200mm LiDAR)
    - Motor clamp values (-1.0 to 1.0) enforced before PWM generation
    - Recovery procedure sequence: halt -> reverse -> turn -> re-scan
    - No blocking operations in safety-critical paths
    - Watchdog timer feeds correctly in main loop

[ ] MCP PROTOCOL COMPLIANCE
    - All hardware interactions go through MCP tools only
    - No direct GPIO/shell commands to motors or sensors
    - JSON-RPC 2.0 format correct for all ESP32 commands
    - Error handling for serial timeout and disconnect
    - Telemetry polling after every drive command

[ ] ROS2 BEST PRACTICES
    - Node lifecycle management (init, spin, destroy, shutdown)
    - QoS profiles appropriate for sensor data (BEST_EFFORT for scans)
    - Topic remapping uses namespaces (/advika/...)
    - Parameter declarations with defaults and descriptions
    - use_sim_time respected throughout

[ ] PYTHON CODE QUALITY
    - Type hints on all function signatures
    - Docstrings with Args/Returns/Raises
    - No bare except clauses
    - Resource cleanup (serial ports, cameras, I2C buses)
    - Logging instead of print statements
    - Async/await patterns in HITL web handlers

[ ] C++ FIRMWARE (ESP32)
    - No dynamic memory allocation in ISR
    - volatile keywords on shared ISR variables
    - PID tuning constants within reasonable ranges
    - Encoder overflow handling
    - PWM frequency matches motor driver specs (20kHz)

[ ] SIMULATION FIDELITY
    - URDF masses/inertias match physical robot (2.5kg total)
    - Sensor noise models match real hardware specs
    - Gazebo plugin parameters match hardware datasheets
    - MCP bridge returns identical format to hardware bridge

[ ] HITL SECURITY
    - WebSocket input validation
    - Emergency stop cannot be overridden by AI
    - Action approval timeouts prevent indefinite blocking
    - Safety events logged with full context

[ ] DOCUMENTATION
    - README matches actual file structure
    - Safety rules documented and referenced
    - API endpoints documented with examples
    - Child manual age-appropriate and safety-focused

OUTPUT FORMAT:
For each [ ] item, respond with:
- PASS / FAIL / WARNING / N/A
- File:line reference
- Specific issue or confirmation
- Recommended fix (if FAIL/WARNING)

PRIORITY ORDER:
1. Safety critical (E-Stop, collision avoidance)
2. MCP protocol integrity
3. ROS2 node stability
4. Code maintainability
5. Documentation accuracy

FILES TO AUDIT:
- firmware/esp32_motor_bridge/src/main.cpp
- firmware/esp32_motor_bridge/src/safety_interrupt.h
- mcp_servers/hardware_bridge.py
- mcp_servers/vision_bridge.py
- simulation/scripts/sim_mcp_bridge.py
- simulation/scripts/safety_monitor.py
- simulation/hitl/hitl_bridge.py
- scripts/test_peripherals.py
- config/robot_params.yaml
- simulation/config/nav2_params.yaml
================================================================================