#!/usr/bin/env python3
"""
Advika 3.0 -- Hardware Diagnostic Pipeline
Comprehensive test suite for all robot peripherals.
Run this before first deployment or after hardware changes.
"""

import os
import sys
import time
import json
import serial
import struct
from datetime import datetime
from typing import Dict, List, Tuple

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

class TestResult:
    def __init__(self, name: str):
        self.name = name
        self.passed = False
        self.details = ""
        self.duration_ms = 0

    def __str__(self):
        status = f"{GREEN}PASS{RESET}" if self.passed else f"{RED}FAIL{RESET}"
        return f"  [{status}] {self.name} ({self.duration_ms:.0f}ms) - {self.details}"

class DiagnosticRunner:
    def __init__(self):
        self.results: List[TestResult] = []
        self.serial_port = os.getenv("SERIAL_PORT", "/dev/ttyUSB0")
        self.baud_rate = int(os.getenv("BAUD_RATE", "115200"))
        self.lidar_port = os.getenv("LIDAR_PORT", "/dev/ttyUSB1")
        self.esp32 = None

    def run_all(self):
        print(f"\n{BOLD}{BLUE}╔══════════════════════════════════════════════════════════════╗{RESET}")
        print(f"{BOLD}{BLUE}║         ADVIKA 3.0 HARDWARE DIAGNOSTIC PIPELINE              ║{RESET}")
        print(f"{BOLD}{BLUE}╚══════════════════════════════════════════════════════════════╝{RESET}\n")
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Serial Port: {self.serial_port} @ {self.baud_rate} baud")
        print(f"LiDAR Port: {self.lidar_port} @ 230400 baud\n")

        # Run all tests
        self._test_esp32_serial()
        self._test_motor_drive()
        self._test_encoder_feedback()
        self._test_lidar()
        self._test_tof_array()
        self._test_bms()
        self._test_cameras()
        self._test_tts()
        self._test_i2c_bus()

        # Print summary
        self._print_summary()

    def _test_esp32_serial(self):
        result = TestResult("ESP32 Serial Communication")
        start = time.time()

        try:
            self.esp32 = serial.Serial(self.serial_port, self.baud_rate, timeout=2.0)
            time.sleep(2)  # Wait for boot

            # Send ping command
            ping = {"jsonrpc": "2.0", "method": "get_telemetry", "id": 1}
            self.esp32.write((json.dumps(ping) + "\n").encode())

            # Wait for response
            resp_start = time.time()
            while time.time() - resp_start < 3.0:
                if self.esp32.in_waiting:
                    line = self.esp32.readline().decode().strip()
                    if line and ("result" in line or "telemetry" in line):
                        result.passed = True
                        result.details = f"Response received: {line[:60]}..."
                        break
                time.sleep(0.01)

            if not result.passed:
                result.details = "No valid response from ESP32"
        except Exception as e:
            result.details = f"Serial error: {str(e)}"

        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)

    def _test_motor_drive(self):
        result = TestResult("Motor Drive Command")
        start = time.time()

        if self.esp32 is None or not self.esp32.is_open:
            result.details = "ESP32 serial not available"
            result.duration_ms = (time.time() - start) * 1000
            self.results.append(result)
            print(result)
            return

        try:
            # Send a very brief forward command (100ms, low speed)
            cmd = {
                "jsonrpc": "2.0",
                "method": "drive",
                "params": {"linear_velocity": 0.1, "angular_velocity": 0.0, "duration_ms": 100},
                "id": 2
            }
            self.esp32.write((json.dumps(cmd) + "\n").encode())

            # Wait for acceptance
            resp_start = time.time()
            while time.time() - resp_start < 2.0:
                if self.esp32.in_waiting:
                    line = self.esp32.readline().decode().strip()
                    if "accepted" in line:
                        result.passed = True
                        result.details = "Drive command accepted by ESP32"
                        break
                time.sleep(0.01)

            if not result.passed:
                result.details = "Drive command not accepted"
        except Exception as e:
            result.details = f"Motor test error: {str(e)}"

        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)

    def _test_encoder_feedback(self):
        result = TestResult("Encoder Feedback")
        start = time.time()

        if self.esp32 is None or not self.esp32.is_open:
            result.details = "ESP32 serial not available"
            result.duration_ms = (time.time() - start) * 1000
            self.results.append(result)
            print(result)
            return

        try:
            # Reset encoders
            reset_cmd = {"jsonrpc": "2.0", "method": "reset_encoders", "id": 3}
            self.esp32.write((json.dumps(reset_cmd) + "\n").encode())
            time.sleep(0.5)

            # Read telemetry
            telem_cmd = {"jsonrpc": "2.0", "method": "get_telemetry", "id": 4}
            self.esp32.write((json.dumps(telem_cmd) + "\n").encode())

            resp_start = time.time()
            while time.time() - resp_start < 2.0:
                if self.esp32.in_waiting:
                    line = self.esp32.readline().decode().strip()
                    if "telemetry" in line:
                        data = json.loads(line)
                        params = data.get("params", {})
                        left_enc = params.get("left_encoder", "N/A")
                        right_enc = params.get("right_encoder", "N/A")
                        result.passed = True
                        result.details = f"L={left_enc}, R={right_enc}"
                        break
                time.sleep(0.01)

            if not result.passed:
                result.details = "No encoder data received"
        except Exception as e:
            result.details = f"Encoder test error: {str(e)}"

        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)

    def _test_lidar(self):
        result = TestResult("LD06 LiDAR")
        start = time.time()

        try:
            lidar = serial.Serial(self.lidar_port, 230400, timeout=1.0)
            time.sleep(0.5)

            # Try to read a packet
            packet_found = False
            read_start = time.time()
            while time.time() - read_start < 3.0:
                if lidar.in_waiting >= 2:
                    header = lidar.read(2)
                    if header == b'\x54\x2C':
                        data = lidar.read(45)
                        if len(data) == 45:
                            start_angle = struct.unpack('<H', data[40:42])[0] / 100.0
                            result.passed = True
                            result.details = f"Packet received, start angle: {start_angle:.1f}°"
                            packet_found = True
                            break
                    else:
                        lidar.read(1)
                time.sleep(0.01)

            lidar.close()

            if not packet_found:
                result.details = "No valid LiDAR packets received"
        except Exception as e:
            result.details = f"LiDAR error: {str(e)}"

        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)

    def _test_tof_array(self):
        result = TestResult("VL53L5CX ToF Array (8x8)")
        start = time.time()

        try:
            import smbus2
            bus = smbus2.SMBus(1)

            # Try to detect device at 0x52
            try:
                bus.read_byte(0x52)
                result.passed = True
                result.details = "VL53L5CX detected on I2C bus 1 (addr 0x52)"
            except OSError:
                result.details = "VL53L5CX not responding on I2C bus 1"

            bus.close()
        except ImportError:
            result.details = "smbus2 not installed"
        except Exception as e:
            result.details = f"ToF error: {str(e)}"

        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)

    def _test_bms(self):
        result = TestResult("Battery Management System")
        start = time.time()

        try:
            import smbus2
            bus = smbus2.SMBus(1)

            try:
                # Read voltage register (0x09)
                voltage_raw = bus.read_word_data(0x0B, 0x09)
                voltage = voltage_raw / 1000.0
                result.passed = True
                result.details = f"Battery voltage: {voltage:.2f}V"
            except OSError:
                result.details = "BMS not responding on I2C bus 1 (addr 0x0B)"

            bus.close()
        except ImportError:
            result.details = "smbus2 not installed"
        except Exception as e:
            result.details = f"BMS error: {str(e)}"

        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)

    def _test_cameras(self):
        result = TestResult("Dual Camera Rig")
        start = time.time()

        try:
            import cv2

            horizon_cam = os.getenv("HORIZON_CAM", "/dev/video0")
            floor_cam = os.getenv("FLOOR_CAM", "/dev/video2")

            caps_tested = 0
            caps_working = 0

            for cam_dev, name in [(horizon_cam, "horizon"), (floor_cam, "floor")]:
                cap = cv2.VideoCapture(cam_dev, cv2.CAP_V4L2)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret and frame is not None:
                        h, w = frame.shape[:2]
                        caps_working += 1
                        result.details += f"{name}: {w}x{h} | "
                    cap.release()
                caps_tested += 1

            if caps_working == caps_tested:
                result.passed = True
            else:
                result.details += f"({caps_working}/{caps_tested} cameras working)"
        except ImportError:
            result.details = "OpenCV not installed"
        except Exception as e:
            result.details = f"Camera error: {str(e)}"

        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)

    def _test_tts(self):
        result = TestResult("Text-to-Speech (eSpeak-ng)")
        start = time.time()

        try:
            import subprocess

            test_result = subprocess.run(
                ["espeak-ng", "-v", "en-us", "-s", "150", "Testing Advika TTS"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if test_result.returncode == 0:
                result.passed = True
                result.details = "eSpeak-ng executed successfully"
            else:
                result.details = f"eSpeak-ng error: {test_result.stderr}"
        except FileNotFoundError:
            result.details = "espeak-ng not found in PATH"
        except Exception as e:
            result.details = f"TTS error: {str(e)}"

        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)

    def _test_i2c_bus(self):
        result = TestResult("I2C Bus Scan")
        start = time.time()

        try:
            import smbus2
            bus = smbus2.SMBus(1)

            devices = []
            for addr in range(0x03, 0x78):
                try:
                    bus.read_byte(addr)
                    devices.append(f"0x{addr:02X}")
                except OSError:
                    pass

            bus.close()

            if devices:
                result.passed = True
                result.details = f"Found {len(devices)} devices: {', '.join(devices[:5])}"
                if len(devices) > 5:
                    result.details += f" ... and {len(devices) - 5} more"
            else:
                result.details = "No I2C devices detected"
        except ImportError:
            result.details = "smbus2 not installed"
        except Exception as e:
            result.details = f"I2C error: {str(e)}"

        result.duration_ms = (time.time() - start) * 1000
        self.results.append(result)
        print(result)

    def _print_summary(self):
        print(f"\n{BOLD}{BLUE}══════════════════════════════════════════════════════════════{RESET}")
        print(f"{BOLD}                        TEST SUMMARY                          {RESET}")
        print(f"{BOLD}{BLUE}══════════════════════════════════════════════════════════════{RESET}\n")

        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        total = len(self.results)

        for r in self.results:
            print(r)

        print(f"\n{BOLD}{BLUE}──────────────────────────────────────────────────────────────{RESET}")
        print(f"  Total Tests: {total}")
        print(f"  {GREEN}Passed: {passed}{RESET}")
        print(f"  {RED}Failed: {failed}{RESET}")

        if failed == 0:
            print(f"\n  {GREEN}{BOLD}All systems operational. Advika is ready to roll!{RESET}")
        elif failed <= 2:
            print(f"\n  {YELLOW}{BOLD}Minor issues detected. Check failed tests before deployment.{RESET}")
        else:
            print(f"\n  {RED}{BOLD}Multiple failures detected. Do NOT deploy until resolved.{RESET}")

        print(f"{BOLD}{BLUE}──────────────────────────────────────────────────────────────{RESET}\n")

        # Save report
        report = {
            "timestamp": datetime.now().isoformat(),
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "details": r.details,
                    "duration_ms": r.duration_ms
                } for r in self.results
            ],
            "summary": {"total": total, "passed": passed, "failed": failed}
        }

        report_path = "/var/log/advika/diagnostic_report.json"
        try:
            os.makedirs(os.path.dirname(report_path), exist_ok=True)
            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)
            print(f"Full report saved to: {report_path}\n")
        except Exception:
            local_report = os.path.expanduser("~/Documents/Robotics/advika_robot_ws/diagnostic_report.json")
            with open(local_report, "w") as f:
                json.dump(report, f, indent=2)
            print(f"Full report saved to: {local_report}\n")


if __name__ == "__main__":
    runner = DiagnosticRunner()
    runner.run_all()
