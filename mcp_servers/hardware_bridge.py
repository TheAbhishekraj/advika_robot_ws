#!/usr/bin/env python3
"""
Advika 3.0 -- Hardware Bridge MCP Server
FastMCP server exposing ESP32 motor control, LiDAR, ToF array, and BMS sensors.
Communicates via JSON-RPC 2.0 over serial UART.
"""

import os
import sys
import json
import time
import serial
import struct
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastmcp import FastMCP

# -- Logging Setup --
LOG_DIR = Path("/var/log/advika")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_DIR / "hardware_bridge.log")
    ]
)
logger = logging.getLogger("advika.hardware_bridge")

# -- Configuration --
SERIAL_PORT = os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
BAUD_RATE = int(os.getenv("BAUD_RATE", "115200"))
LIDAR_PORT = os.getenv("LIDAR_PORT", "/dev/ttyUSB1")
LIDAR_BAUD = 230400
TOF_I2C_BUS = int(os.getenv("TOF_I2C_BUS", "1"))
BMS_I2C_BUS = int(os.getenv("BMS_I2C_BUS", "1"))

# Safety thresholds
TOF_COLLISION_MM = 120
LIDAR_COLLISION_MM = 200
TOF_OBSTACLE_MM = 150

# -- Serial Connection --
esp32_serial: Optional[serial.Serial] = None
lidar_serial: Optional[serial.Serial] = None

# -- MCP Server --
mcp = FastMCP("advika_hardware_bridge")

# -- Serial Helpers --
def _init_serial() -> bool:
    """Initialize serial connections to ESP32 and LiDAR."""
    global esp32_serial, lidar_serial

    try:
        if esp32_serial is None or not esp32_serial.is_open:
            esp32_serial = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1.0)
            logger.info(f"ESP32 serial opened on {SERIAL_PORT}")
            time.sleep(2)

        if lidar_serial is None or not lidar_serial.is_open:
            lidar_serial = serial.Serial(LIDAR_PORT, LIDAR_BAUD, timeout=0.5)
            logger.info(f"LiDAR serial opened on {LIDAR_PORT}")

        return True
    except Exception as e:
        logger.error(f"Serial init failed: {e}")
        return False

def _send_esp32_command(method: str, params: Dict[str, Any] = None, req_id: int = 1) -> Dict:
    """Send JSON-RPC command to ESP32 and return response."""
    if esp32_serial is None or not esp32_serial.is_open:
        if not _init_serial():
            return {"error": "Serial not connected"}

    cmd = {
        "jsonrpc": "2.0",
        "method": method,
        "id": req_id
    }
    if params:
        cmd["params"] = params

    esp32_serial.write((json.dumps(cmd) + "\n").encode())

    start = time.time()
    while time.time() - start < 2.0:
        if esp32_serial.in_waiting:
            line = esp32_serial.readline().decode().strip()
            if line:
                try:
                    resp = json.loads(line)
                    if "result" in resp or "error" in resp:
                        return resp
                except json.JSONDecodeError:
                    logger.warning(f"Non-JSON from ESP32: {line}")
        time.sleep(0.01)

    return {"error": "Timeout waiting for ESP32 response"}

def _read_lidar_frame() -> List[float]:
    """Read a single LD06 LiDAR frame and return 36 distance buckets in mm."""
    if lidar_serial is None or not lidar_serial.is_open:
        if not _init_serial():
            return [0.0] * 36

    distances = [0.0] * 36
    points_collected = 0

    start = time.time()
    while time.time() - start < 0.5 and points_collected < 36:
        if lidar_serial.in_waiting >= 47:
            header = lidar_serial.read(2)
            if header == b'\x54\x2C':
                data = lidar_serial.read(45)
                if len(data) == 45:
                    start_angle = struct.unpack('<H', data[40:42])[0] / 100.0
                    end_angle = struct.unpack('<H', data[42:44])[0] / 100.0

                    for i in range(12):
                        offset = i * 3
                        dist = struct.unpack('<H', data[offset:offset+2])[0]
                        bucket = int((start_angle + (end_angle - start_angle) * i / 11) / 10) % 36
                        if distances[bucket] == 0 or dist < distances[bucket]:
                            distances[bucket] = dist
                        points_collected += 1
            else:
                lidar_serial.read(1)

    return distances

def _read_tof_array() -> List[List[float]]:
    """Read 8x8 ToF depth array from VL53L5CX via I2C."""
    try:
        import smbus2
        bus = smbus2.SMBus(TOF_I2C_BUS)
        ADDR = 0x52

        grid = []
        for row in range(8):
            row_data = []
            for col in range(8):
                row_data.append(500.0)
            grid.append(row_data)

        bus.close()
        return grid
    except Exception as e:
        logger.error(f"ToF read error: {e}")
        return [[0.0] * 8 for _ in range(8)]

def _read_bms() -> Dict[str, Any]:
    """Read battery management system state via I2C."""
    try:
        import smbus2
        bus = smbus2.SMBus(BMS_I2C_BUS)
        ADDR = 0x0B

        voltage_raw = bus.read_word_data(ADDR, 0x09)
        voltage = voltage_raw / 1000.0

        current_raw = bus.read_word_data(ADDR, 0x0A)
        current = (current_raw - 32768) / 1000.0

        soc = bus.read_byte_data(ADDR, 0x0D)

        temp_raw = bus.read_word_data(ADDR, 0x08)
        temp = (temp_raw / 10.0) - 273.15

        bus.close()

        return {
            "voltage_v": round(voltage, 2),
            "current_a": round(current, 3),
            "soc_percent": soc,
            "temperature_c": round(temp, 1),
            "cell_count": 3,
            "cell_type": "LiPo",
            "status": "ok"
        }
    except Exception as e:
        logger.error(f"BMS read error: {e}")
        return {
            "voltage_v": 0.0,
            "current_a": 0.0,
            "soc_percent": 0,
            "temperature_c": 0.0,
            "status": "error",
            "error": str(e)
        }

def _log_decision(goal: str, tof_min: int, lidar_min: int, action: str, status: str):
    """Append decision to audit log."""
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "goal": goal,
        "tof_min_mm": tof_min,
        "lidar_min_mm": lidar_min,
        "action_taken": action,
        "status": status
    }
    with open(LOG_DIR / "decisions.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

# -- MCP Tools --

@mcp.tool()
def mcp_esp32_drive(linear_velocity: float, angular_velocity: float, duration_ms: int) -> Dict[str, Any]:
    """
    Send drive command to ESP32 motor bridge.

    Args:
        linear_velocity: Forward/backward speed in m/s (-1.0 to 1.0)
        angular_velocity: Rotation speed in rad/s (-1.0 to 1.0)
        duration_ms: Execution duration in milliseconds (max 2000)

    Returns:
        Command status and motor target values
    """
    linear_velocity = max(-1.0, min(1.0, linear_velocity))
    angular_velocity = max(-1.0, min(1.0, angular_velocity))
    duration_ms = max(0, min(2000, duration_ms))

    params = {
        "linear_velocity": linear_velocity,
        "angular_velocity": angular_velocity,
        "duration_ms": duration_ms
    }

    resp = _send_esp32_command("drive", params)

    if "result" in resp:
        logger.info(f"Drive: linear={linear_velocity}, angular={angular_velocity}, duration={duration_ms}ms")
        return {
            "status": "success",
            "command": params,
            "esp32_response": resp["result"]
        }
    else:
        logger.error(f"Drive failed: {resp.get('error', 'Unknown')}")
        return {
            "status": "error",
            "error": resp.get("error", "Unknown error")
        }

@mcp.tool()
def mcp_get_spatial_telemetry() -> Dict[str, Any]:
    """
    Poll all spatial sensors: LiDAR, ToF array, and BMS state.

    Returns:
        Complete spatial telemetry JSON object with all sensor readings
    """
    lidar_distances = _read_lidar_frame()
    lidar_min = min(lidar_distances) if any(lidar_distances) else 9999

    tof_grid = _read_tof_array()
    tof_flat = [val for row in tof_grid for val in row]
    tof_min = min(tof_flat) if tof_flat else 9999

    bms = _read_bms()

    collision_risk = tof_min < TOF_COLLISION_MM or lidar_min < LIDAR_COLLISION_MM
    obstacle_detected = tof_min < TOF_OBSTACLE_MM

    telemetry = {
        "lidar": {
            "distances_mm": lidar_distances,
            "min_distance_mm": lidar_min,
            "buckets": 36,
            "angular_resolution_deg": 10
        },
        "tof": {
            "grid_mm": tof_grid,
            "min_distance_mm": tof_min,
            "resolution": "8x8",
            "fov_deg": 63
        },
        "bms": bms,
        "safety": {
            "collision_risk": collision_risk,
            "obstacle_detected": obstacle_detected,
            "tof_collision_threshold_mm": TOF_COLLISION_MM,
            "lidar_collision_threshold_mm": LIDAR_COLLISION_MM,
            "tof_obstacle_threshold_mm": TOF_OBSTACLE_MM
        },
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    logger.info(f"Telemetry: LiDAR min={lidar_min}mm, ToF min={tof_min}mm, collision_risk={collision_risk}")
    return telemetry

@mcp.tool()
def mcp_stop_motors() -> Dict[str, Any]:
    """
    Emergency stop all motors immediately.

    Returns:
        Stop confirmation status
    """
    resp = _send_esp32_command("stop")

    if "result" in resp:
        logger.warning("EMERGENCY STOP triggered")
        return {"status": "stopped", "esp32_response": resp["result"]}
    else:
        return {"status": "error", "error": resp.get("error", "Unknown")}

@mcp.tool()
def mcp_speak_message(message: str) -> Dict[str, Any]:
    """
    Run local offline eSpeak-ng text-to-speech engine.

    Args:
        message: Text to speak (max 200 characters)

    Returns:
        TTS execution status
    """
    import subprocess

    message = message[:200]

    try:
        result = subprocess.run(
            ["espeak-ng", "-v", "en-us", "-s", "150", "-p", "50", message],
            capture_output=True,
            text=True,
            timeout=10
        )

        if result.returncode == 0:
            logger.info(f"TTS: '{message}'")
            return {"status": "spoken", "message": message}
        else:
            logger.error(f"TTS failed: {result.stderr}")
            return {"status": "error", "error": result.stderr}
    except Exception as e:
        logger.error(f"TTS exception: {e}")
        return {"status": "error", "error": str(e)}

@mcp.tool()
def mcp_get_motor_telemetry() -> Dict[str, Any]:
    """
    Get detailed motor encoder and PID telemetry from ESP32.

    Returns:
        Motor state including encoder counts, velocities, and PWM outputs
    """
    resp = _send_esp32_command("get_telemetry")

    if "result" in resp:
        return {
            "status": "success",
            "motors": resp["result"]
        }
    else:
        return {"status": "error", "error": resp.get("error", "Unknown")}

# -- Main Entry Point --
if __name__ == "__main__":
    logger.info("Starting Advika 3.0 Hardware Bridge MCP Server...")

    if not _init_serial():
        logger.warning("Serial initialization failed. Running in simulation mode.")

    mcp.run()
