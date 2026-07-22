#!/usr/bin/env python3
"""
Advika 3.0 -- Scenario Runner
Automated simulation testing framework for regression testing,
benchmarking, and CI/CD integration.

Scenarios are JSON-defined test cases that verify:
- Navigation accuracy
- Collision avoidance
- Object detection
- Recovery procedures
- HITL approval workflows
"""

import os
import sys
import json
import time
import math
import argparse
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import Bool
import numpy as np


class TestResult(Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"
    TIMEOUT = "TIMEOUT"


@dataclass
class ScenarioStep:
    """Single step in a test scenario."""
    action: str  # "drive", "wait", "check_distance", "check_position", "approve", "estop"
    params: Dict[str, Any]
    timeout_sec: float = 10.0
    description: str = ""


@dataclass
class Scenario:
    """Complete test scenario definition."""
    name: str
    description: str
    setup: Dict[str, Any]  # Initial pose, obstacles, etc.
    steps: List[ScenarioStep]
    expected_result: str
    tags: List[str]


@dataclass
class ScenarioResult:
    """Results from running a scenario."""
    scenario_name: str
    start_time: str
    end_time: str
    duration_sec: float
    result: str
    steps_passed: int
    steps_failed: int
    steps_total: int
    details: List[Dict[str, Any]]
    logs: List[str]


class ScenarioRunnerNode(Node):
    """ROS2 node that executes test scenarios in simulation."""

    def __init__(self):
        super().__init__('scenario_runner')

        # Subscribers
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )
        self.scan_sub = self.create_subscription(
            LaserScan, '/advika/scan', self._scan_callback, sensor_qos)
        self.odom_sub = self.create_subscription(
            Odometry, '/advika/odom', self._odom_callback, 10)
        self.safety_sub = self.create_subscription(
            Bool, '/advika/safety_active', self._safety_callback, 10)

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/advika/cmd_vel', 10)
        self.goal_pub = self.create_publisher(PoseStamped, '/goal_pose', 10)

        # State
        self.current_odom: Optional[Odometry] = None
        self.current_scan: Optional[LaserScan] = None
        self.safety_active = False
        self._step_results: List[Dict] = []
        self._logs: List[str] = []

        self.get_logger().info("Scenario Runner initialized")

    def _scan_callback(self, msg: LaserScan):
        self.current_scan = msg

    def _odom_callback(self, msg: Odometry):
        self.current_odom = msg

    def _safety_callback(self, msg: Bool):
        self.safety_active = msg.data

    def log(self, message: str):
        """Log a message."""
        self._logs.append(f"[{datetime.now().isoformat()}] {message}")
        self.get_logger().info(message)

    def _wait_for_odom(self, timeout_sec: float = 5.0) -> bool:
        """Wait for odometry data."""
        start = time.time()
        while self.current_odom is None and (time.time() - start) < timeout_sec:
            rclpy.spin_once(self, timeout_sec=0.1)
        return self.current_odom is not None

    def _get_position(self) -> Optional[Dict[str, float]]:
        """Get current position."""
        if self.current_odom is None:
            return None
        pose = self.current_odom.pose.pose
        return {
            "x": pose.position.x,
            "y": pose.position.y,
            "z": pose.position.z
        }

    def _get_min_lidar_distance(self) -> float:
        """Get minimum LiDAR distance in front sector."""
        if self.current_scan is None or not self.current_scan.ranges:
            return float('inf')

        front_ranges = []
        for i, r in enumerate(self.current_scan.ranges):
            angle = self.current_scan.angle_min + i * self.current_scan.angle_increment
            if abs(angle) < math.radians(30):
                if self.current_scan.range_min < r < self.current_scan.range_max:
                    front_ranges.append(r)

        return min(front_ranges) if front_ranges else float('inf')

    def _drive(self, linear: float, angular: float, duration_sec: float):
        """Send drive command for specified duration."""
        cmd = Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular

        start = time.time()
        rate = self.create_rate(20)

        while (time.time() - start) < duration_sec and rclpy.ok():
            self.cmd_vel_pub.publish(cmd)
            rclpy.spin_once(self, timeout_sec=0.05)

        # Stop
        stop_cmd = Twist()
        self.cmd_vel_pub.publish(stop_cmd)

    def _execute_step(self, step: ScenarioStep, step_num: int) -> TestResult:
        """Execute a single scenario step."""
        self.log(f"Step {step_num}: {step.description or step.action}")

        start_time = time.time()
        result = TestResult.FAIL
        details = {}

        try:
            if step.action == "drive":
                linear = step.params.get("linear_velocity", 0.0)
                angular = step.params.get("angular_velocity", 0.0)
                duration = step.params.get("duration_ms", 1000) / 1000.0
                self._drive(linear, angular, duration)
                result = TestResult.PASS
                details = {"linear": linear, "angular": angular, "duration": duration}

            elif step.action == "wait":
                duration = step.params.get("duration_sec", 1.0)
                time.sleep(duration)
                result = TestResult.PASS
                details = {"waited_sec": duration}

            elif step.action == "check_distance":
                min_dist = self._get_min_lidar_distance()
                expected_min = step.params.get("min_distance_m", 0.0)
                expected_max = step.params.get("max_distance_m", float('inf'))

                if expected_min <= min_dist <= expected_max:
                    result = TestResult.PASS
                else:
                    result = TestResult.FAIL
                details = {"measured_m": min_dist, "expected_min": expected_min, "expected_max": expected_max}

            elif step.action == "check_position":
                pos = self._get_position()
                if pos is None:
                    result = TestResult.FAIL
                    details = {"error": "No odometry available"}
                else:
                    target_x = step.params.get("x")
                    target_y = step.params.get("y")
                    tolerance = step.params.get("tolerance_m", 0.5)

                    if target_x is not None and target_y is not None:
                        dist = math.sqrt((pos["x"] - target_x)**2 + (pos["y"] - target_y)**2)
                        if dist <= tolerance:
                            result = TestResult.PASS
                        else:
                            result = TestResult.FAIL
                        details = {"distance_to_target": dist, "tolerance": tolerance, "position": pos}
                    else:
                        result = TestResult.PASS
                        details = {"position": pos}

            elif step.action == "check_safety":
                expected_active = step.params.get("safety_active", False)
                if self.safety_active == expected_active:
                    result = TestResult.PASS
                else:
                    result = TestResult.FAIL
                details = {"safety_active": self.safety_active, "expected": expected_active}

            elif step.action == "estop":
                # Publish zero velocity
                stop_cmd = Twist()
                self.cmd_vel_pub.publish(stop_cmd)
                result = TestResult.PASS
                details = {"action": "emergency_stop"}

            else:
                result = TestResult.SKIP
                details = {"error": f"Unknown action: {step.action}"}

        except Exception as e:
            result = TestResult.FAIL
            details = {"error": str(e)}
            self.log(f"Step {step_num} error: {e}")

        elapsed = time.time() - start_time

        step_result = {
            "step_num": step_num,
            "action": step.action,
            "result": result.value,
            "elapsed_sec": round(elapsed, 2),
            "details": details
        }
        self._step_results.append(step_result)

        self.log(f"Step {step_num} result: {result.value}")
        return result

    def run_scenario(self, scenario: Scenario) -> ScenarioResult:
        """Run a complete scenario."""
        self.log(f"=" * 60)
        self.log(f"Running scenario: {scenario.name}")
        self.log(f"Description: {scenario.description}")
        self.log(f"Expected result: {scenario.expected_result}")
        self.log(f"=" * 60)

        start_time = time.time()
        start_iso = datetime.utcnow().isoformat() + "Z"

        # Wait for sensors
        self.log("Waiting for sensor data...")
        if not self._wait_for_odom(timeout_sec=10.0):
            self.log("ERROR: Failed to receive odometry data")
            return ScenarioResult(
                scenario_name=scenario.name,
                start_time=start_iso,
                end_time=datetime.utcnow().isoformat() + "Z",
                duration_sec=0.0,
                result=TestResult.FAIL.value,
                steps_passed=0,
                steps_failed=0,
                steps_total=0,
                details=[{"error": "No odometry data"}],
                logs=self._logs
            )

        # Execute steps
        passed = 0
        failed = 0

        for i, step in enumerate(scenario.steps):
            step_result = self._execute_step(step, i + 1)

            if step_result == TestResult.PASS:
                passed += 1
            elif step_result == TestResult.FAIL:
                failed += 1
                # Stop on first failure unless continue_on_fail is set
                if not step.params.get("continue_on_fail", False):
                    self.log("Stopping scenario due to failure")
                    break

        end_time = time.time()
        duration = end_time - start_time

        overall_result = TestResult.PASS if failed == 0 else TestResult.FAIL

        result = ScenarioResult(
            scenario_name=scenario.name,
            start_time=start_iso,
            end_time=datetime.utcnow().isoformat() + "Z",
            duration_sec=round(duration, 2),
            result=overall_result.value,
            steps_passed=passed,
            steps_failed=failed,
            steps_total=len(scenario.steps),
            details=self._step_results,
            logs=self._logs
        )

        self.log(f"Scenario complete: {overall_result.value}")
        self.log(f"Steps: {passed} passed, {failed} failed, {len(scenario.steps)} total")
        self.log(f"Duration: {duration:.2f}s")

        return result


# ==================== BUILT-IN SCENARIOS ====================

def get_builtin_scenarios() -> List[Scenario]:
    """Return built-in test scenarios."""

    scenarios = []

    # Scenario 1: Basic Forward Drive
    scenarios.append(Scenario(
        name="basic_forward_drive",
        description="Drive forward 1 meter and verify position change",
        setup={"initial_pose": {"x": 0, "y": -4, "yaw": 0}},
        steps=[
            ScenarioStep(
                action="wait",
                params={"duration_sec": 2.0},
                description="Wait for simulation to stabilize"
            ),
            ScenarioStep(
                action="check_position",
                params={"tolerance_m": 0.1},
                description="Record initial position"
            ),
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.3, "angular_velocity": 0.0, "duration_ms": 3000},
                timeout_sec=5.0,
                description="Drive forward for 3 seconds at 0.3 m/s"
            ),
            ScenarioStep(
                action="wait",
                params={"duration_sec": 1.0},
                description="Wait for stop"
            ),
            ScenarioStep(
                action="check_position",
                params={"x": 0.0, "y": -3.0, "tolerance_m": 0.5},
                description="Verify position moved forward ~0.9m"
            )
        ],
        expected_result="Robot moves forward approximately 0.9 meters",
        tags=["basic", "drive", "smoke_test"]
    ))

    # Scenario 2: Collision Avoidance
    scenarios.append(Scenario(
        name="collision_avoidance",
        description="Drive toward wall and verify safety stop triggers",
        setup={"initial_pose": {"x": 0, "y": -4, "yaw": 0}, "obstacles": ["wall_north"]},
        steps=[
            ScenarioStep(
                action="wait",
                params={"duration_sec": 2.0},
                description="Wait for stabilization"
            ),
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.3, "angular_velocity": 0.0, "duration_ms": 10000},
                timeout_sec=12.0,
                description="Drive toward wall"
            ),
            ScenarioStep(
                action="wait",
                params={"duration_sec": 2.0},
                description="Wait for safety response"
            ),
            ScenarioStep(
                action="check_safety",
                params={"safety_active": True},
                description="Verify safety system triggered"
            ),
            ScenarioStep(
                action="check_distance",
                params={"min_distance_m": 0.12, "max_distance_m": 0.20},
                description="Verify stopped before collision"
            )
        ],
        expected_result="Safety monitor stops robot before wall collision",
        tags=["safety", "collision", "critical"]
    ))

    # Scenario 3: Rotation Test
    scenarios.append(Scenario(
        name="rotation_test",
        description="Rotate 360 degrees and verify orientation",
        setup={"initial_pose": {"x": 0, "y": 0, "yaw": 0}},
        steps=[
            ScenarioStep(
                action="wait",
                params={"duration_sec": 1.0},
                description="Stabilize"
            ),
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.0, "angular_velocity": 0.5, "duration_ms": 6300},
                timeout_sec=8.0,
                description="Rotate at 0.5 rad/s for ~2*pi radians"
            ),
            ScenarioStep(
                action="wait",
                params={"duration_sec": 1.0},
                description="Wait for stop"
            ),
            ScenarioStep(
                action="check_position",
                params={"x": 0.0, "y": 0.0, "tolerance_m": 0.2},
                description="Verify position unchanged (rotation only)"
            )
        ],
        expected_result="Robot rotates in place without significant translation",
        tags=["basic", "rotation", "odometry"]
    ))

    # Scenario 4: Obstacle Recovery
    scenarios.append(Scenario(
        name="obstacle_recovery",
        description="Test obstacle recovery procedure",
        setup={"initial_pose": {"x": 0, "y": -3, "yaw": 0}},
        steps=[
            ScenarioStep(
                action="wait",
                params={"duration_sec": 2.0},
                description="Stabilize"
            ),
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.3, "angular_velocity": 0.0, "duration_ms": 5000},
                timeout_sec=7.0,
                description="Drive toward obstacle"
            ),
            ScenarioStep(
                action="wait",
                params={"duration_sec": 4.0},
                description="Wait for recovery procedure"
            ),
            ScenarioStep(
                action="check_safety",
                params={"safety_active": False},
                description="Verify safety cleared after recovery"
            ),
            ScenarioStep(
                action="check_distance",
                params={"min_distance_m": 0.20},
                description="Verify safe distance maintained"
            )
        ],
        expected_result="Robot triggers safety, executes recovery, and clears",
        tags=["safety", "recovery", "critical"]
    ))

    # Scenario 5: Square Pattern
    scenarios.append(Scenario(
        name="square_pattern",
        description="Drive in a square pattern (1m sides)",
        setup={"initial_pose": {"x": 0, "y": 0, "yaw": 0}},
        steps=[
            ScenarioStep(
                action="wait",
                params={"duration_sec": 1.0},
                description="Stabilize"
            ),
            # Side 1: Forward 1m
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.3, "angular_velocity": 0.0, "duration_ms": 3300},
                description="Forward 1m"
            ),
            # Turn 90 degrees
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.0, "angular_velocity": 0.5, "duration_ms": 1570},
                description="Turn 90 degrees right"
            ),
            # Side 2
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.3, "angular_velocity": 0.0, "duration_ms": 3300},
                description="Forward 1m"
            ),
            # Turn 90
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.0, "angular_velocity": 0.5, "duration_ms": 1570},
                description="Turn 90 degrees right"
            ),
            # Side 3
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.3, "angular_velocity": 0.0, "duration_ms": 3300},
                description="Forward 1m"
            ),
            # Turn 90
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.0, "angular_velocity": 0.5, "duration_ms": 1570},
                description="Turn 90 degrees right"
            ),
            # Side 4
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.3, "angular_velocity": 0.0, "duration_ms": 3300},
                description="Forward 1m"
            ),
            # Turn 90 (back to start orientation)
            ScenarioStep(
                action="drive",
                params={"linear_velocity": 0.0, "angular_velocity": 0.5, "duration_ms": 1570},
                description="Turn 90 degrees right"
            ),
            ScenarioStep(
                action="wait",
                params={"duration_sec": 1.0},
                description="Settle"
            ),
            ScenarioStep(
                action="check_position",
                params={"x": 0.0, "y": 0.0, "tolerance_m": 0.3},
                description="Verify returned near start"
            )
        ],
        expected_result="Robot drives square and returns near starting position",
        tags=["navigation", "odometry", "pattern"]
    ))

    return scenarios


def load_scenario_from_file(filepath: str) -> Optional[Scenario]:
    """Load a scenario from JSON file."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        steps = [ScenarioStep(**s) for s in data.get("steps", [])]
        return Scenario(
            name=data["name"],
            description=data.get("description", ""),
            setup=data.get("setup", {}),
            steps=steps,
            expected_result=data.get("expected_result", ""),
            tags=data.get("tags", [])
        )
    except Exception as e:
        print(f"Failed to load scenario from {filepath}: {e}")
        return None


def save_results(results: List[ScenarioResult], output_dir: str = "/tmp/advika_scenarios"):
    """Save scenario results to JSON file."""
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"scenario_results_{timestamp}.json"
    filepath = os.path.join(output_dir, filename)

    output = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_scenarios": len(results),
        "passed": sum(1 for r in results if r.result == TestResult.PASS.value),
        "failed": sum(1 for r in results if r.result == TestResult.FAIL.value),
        "results": [asdict(r) for r in results]
    }

    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {filepath}")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Advika 3.0 Scenario Runner")
    parser.add_argument("--scenario", "-s", help="Run specific scenario by name")
    parser.add_argument("--file", "-f", help="Load scenario from JSON file")
    parser.add_argument("--list", "-l", action="store_true", help="List available scenarios")
    parser.add_argument("--all", "-a", action="store_true", help="Run all built-in scenarios")
    parser.add_argument("--output", "-o", default="/tmp/advika_scenarios", help="Output directory")
    parser.add_argument("--tags", "-t", help="Filter by tags (comma-separated)")
    args = parser.parse_args()

    # Get scenarios
    scenarios = get_builtin_scenarios()

    if args.list:
        print("\nAvailable Scenarios:")
        print("-" * 60)
        for s in scenarios:
            print(f"  {s.name:30s} | {', '.join(s.tags)}")
            print(f"    {s.description}")
        print()
        return

    # Filter by tags
    if args.tags:
        tags = [t.strip() for t in args.tags.split(",")]
        scenarios = [s for s in scenarios if any(t in s.tags for t in tags)]

    # Select scenarios to run
    if args.scenario:
        scenarios = [s for s in scenarios if s.name == args.scenario]
        if not scenarios:
            print(f"Scenario '{args.scenario}' not found")
            return
    elif args.file:
        scenario = load_scenario_from_file(args.file)
        if scenario:
            scenarios = [scenario]
        else:
            return
    elif not args.all:
        print("Use --scenario NAME, --file PATH, --all, or --list")
        return

    # Run scenarios
    rclpy.init()
    node = ScenarioRunnerNode()

    results = []
    try:
        for scenario in scenarios:
            result = node.run_scenario(scenario)
            results.append(result)

            # Reset state between scenarios
            node._step_results = []
            node._logs = []
            time.sleep(2)
    finally:
        node.destroy_node()
        rclpy.shutdown()

    # Print summary
    print("\n" + "=" * 60)
    print("SCENARIO TEST SUMMARY")
    print("=" * 60)
    for r in results:
        status = "PASS" if r.result == TestResult.PASS.value else "FAIL"
        print(f"  [{status}] {r.scenario_name:30s} | {r.duration_sec:.1f}s | "
              f"{r.steps_passed}/{r.steps_total} steps")

    passed = sum(1 for r in results if r.result == TestResult.PASS.value)
    print(f"\n  Total: {passed}/{len(results)} passed")

    # Save results
    save_results(results, args.output)


if __name__ == "__main__":
    main()
