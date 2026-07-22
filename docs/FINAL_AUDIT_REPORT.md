# Advika 3.0 Final Audit Report

Date: 2026-07-22  
Scope files:
- `/home/runner/work/advika_robot_ws/advika_robot_ws/firmware/esp32_motor_bridge/src/main.cpp`
- `/home/runner/work/advika_robot_ws/advika_robot_ws/firmware/esp32_motor_bridge/src/safety_interrupt.h`
- `/home/runner/work/advika_robot_ws/advika_robot_ws/mcp_servers/hardware_bridge.py`
- `/home/runner/work/advika_robot_ws/advika_robot_ws/mcp_servers/vision_bridge.py`
- `/home/runner/work/advika_robot_ws/advika_robot_ws/simulation/scripts/sim_mcp_bridge.py`
- `/home/runner/work/advika_robot_ws/advika_robot_ws/simulation/scripts/safety_monitor.py`
- `/home/runner/work/advika_robot_ws/advika_robot_ws/simulation/hitl/hitl_bridge.py`
- `/home/runner/work/advika_robot_ws/advika_robot_ws/scripts/test_peripherals.py`

---

## SAFETY CRITICAL CODE

- **E-Stop ISR response < 1ms**: **PASS**
  - Ref: `firmware/esp32_motor_bridge/src/main.cpp`, `firmware/esp32_motor_bridge/src/safety_interrupt.h`
  - `main.cpp` now initializes and checks `safety_interrupt.h` safety ISR path (`safety_init_interrupts`, `safety_is_active`).

- **Collision thresholds match specs (120mm ToF, 200mm LiDAR)**: **PASS**
  - Ref: `mcp_servers/hardware_bridge.py`, `simulation/scripts/safety_monitor.py`, `simulation/hitl/hitl_bridge.py`
  - Collision hard-stop now aligned to 120mm equivalent in simulation/HITL.

- **Motor clamps enforced before PWM generation**: **PASS**
  - Ref: `firmware/esp32_motor_bridge/src/main.cpp`
  - Clamp logic exists for command inputs and PWM outputs.

- **Recovery sequence halt → reverse → turn → re-scan**: **PASS**
  - Ref: `simulation/scripts/safety_monitor.py`
  - Recovery now includes explicit re-scan gate before safety clear.

- **No blocking operations in safety paths**: **PASS**
  - Ref: `firmware/esp32_motor_bridge/src/safety_interrupt.h`, `firmware/esp32_motor_bridge/src/main.cpp`
  - Removed micro-delay in ISR hard-stop path and avoided serial activity in immediate E-stop handling.

## MCP PROTOCOL COMPLIANCE

- **All hardware via MCP tools only**: **WARNING**
  - Ref: `scripts/test_peripherals.py`
  - Diagnostic script intentionally performs low-level direct checks (serial/I2C/camera). Keep as operator diagnostic tool.

- **JSON-RPC 2.0 format correct**: **PASS**
  - Ref: `firmware/esp32_motor_bridge/src/main.cpp`
  - `get_telemetry` now returns JSON-RPC `result` with request `id`.

- **Error handling for serial timeout**: **PASS**
  - Ref: `mcp_servers/hardware_bridge.py`
  - Timeout path returns explicit error object.

## ROS2 BEST PRACTICES

- **Node lifecycle management**: **WARNING**
  - Ref: `simulation/scripts/sim_mcp_bridge.py`, `simulation/scripts/safety_monitor.py`, `simulation/hitl/hitl_bridge.py`
  - Uses standard `Node` classes; lifecycle-node migration is still recommended.

- **QoS profiles appropriate for sensors**: **PASS**
  - Ref: simulation nodes

- **Topic namespaces (/advika/...)**: **PASS**
  - Ref: simulation and HITL nodes

- **use_sim_time respected**: **PASS**
  - Ref: `simulation/hitl/hitl_bridge.py`, `simulation/scripts/*.py`
  - `use_sim_time` declaration present for simulation/HITL paths.

## PYTHON CODE QUALITY

- **Type hints on all functions**: **WARNING**
  - Ref: audited Python files
  - Several functions remain partially annotated.

- **Docstrings with Args/Returns**: **WARNING**
  - Ref: audited Python files
  - Coverage is improved in some places but not complete project-wide.

- **No bare except clauses**: **PASS**
  - Ref: audited Python files

- **Resource cleanup (serial/cameras/I2C)**: **WARNING**
  - Ref: `mcp_servers/hardware_bridge.py`, `mcp_servers/vision_bridge.py`
  - Helper cleanup exists; explicit shutdown hooks can still be improved.

- **Logging not print**: **PASS**
  - Ref: `simulation/hitl/hitl_bridge.py`, `simulation/scripts/sim_mcp_bridge.py`
  - Operational print statements replaced with logger usage in these audited runtime files.

## C++ FIRMWARE (ESP32)

- **No dynamic allocation in ISR**: **PASS**
  - Ref: `firmware/esp32_motor_bridge/src/safety_interrupt.h`

- **volatile on shared ISR variables**: **PASS**
  - Ref: `firmware/esp32_motor_bridge/src/safety_interrupt.h`

- **PID tuning in reasonable ranges**: **WARNING**
  - Ref: `firmware/esp32_motor_bridge/src/main.cpp`
  - Runtime range guards for set_pid can be further tightened.

- **Encoder overflow handling**: **WARNING**
  - Ref: `firmware/esp32_motor_bridge/src/main.cpp`
  - Overflow-safe delta handling not yet explicitly implemented.

- **PWM frequency 20kHz**: **PASS**
  - Ref: `firmware/esp32_motor_bridge/src/main.cpp`

## SIMULATION FIDELITY

- **URDF masses match physical (2.5kg)**: **N/A**
  - Not part of this file-edit pass.

- **Sensor noise matches hardware**: **WARNING**
  - Ref: `simulation/scripts/sim_mcp_bridge.py`
  - Noise model remains synthetic and should be hardware-calibrated.

- **MCP bridge returns identical format**: **PASS**
  - Ref: `simulation/scripts/sim_mcp_bridge.py`, `mcp_servers/hardware_bridge.py`, `firmware/.../main.cpp`
  - Core MCP response structure aligned for tool compatibility.

## HITL SECURITY

- **WebSocket input validation**: **PASS**
  - Ref: `simulation/hitl/hitl_bridge.py`
  - Added numeric bounds checks and mode validation.

- **E-Stop cannot be overridden by AI**: **PASS**
  - Ref: `simulation/hitl/hitl_bridge.py`
  - Emergency lock now blocks mode downgrade unless reset token is provided.

- **Approval timeouts prevent blocking**: **PASS**
  - Ref: `simulation/hitl/hitl_bridge.py`
  - Added timed-out action expiration with auto-reject status.

---

## Remaining Recommendations (High Priority)

1. Add hardware-calibrated ToF/LiDAR noise model and validation datasets.
2. Add strict bounds and validation for `set_pid` values in firmware.
3. Add graceful shutdown hooks to close serial/camera handles on SIGTERM/SIGINT.
4. Move critical ROS2 nodes to lifecycle-managed nodes for controlled state transitions.
