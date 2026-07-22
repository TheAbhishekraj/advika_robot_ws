#!/usr/bin/env python3
"""
Advika 3.0 -- Simulation MCP Bridge
Bridges Gazebo simulation topics to the same MCP protocol used by real hardware.
This allows the AI agent to control the simulated robot using identical MCP tools.
"""

import os
import sys
import json
import time
import asyncio
import threading
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Image
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge
import numpy as np

logger = logging.getLogger("advika.sim_mcp_bridge")
if not logger.handlers:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

# Try to import FastMCP for standalone MCP server mode
try:
    from fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    logger.warning("FastMCP not available. Running in ROS2-only bridge mode.")


@dataclass
class SimSensorState:
    """Current state of all simulated sensors."""
    lidar_distances_mm: List[float]
    tof_grid_mm: List[List[float]]
    odom_position: Dict[str, float]
    odom_velocity: Dict[str, float]
    camera_frame_b64: Optional[str] = None
    timestamp: str = ""


class SimMCPBridgeNode(Node):
    """
    ROS2 node that:
    1. Subscribes to all simulation topics
    2. Publishes cmd_vel for motor commands
    3. Exposes MCP-compatible tools (via FastMCP or ROS2 services)
    4. Maintains identical API to real hardware MCP servers
    """

    def __init__(self):
        super().__init__('sim_mcp_bridge')

        self.declare_parameter('cmd_vel_topic', '/advika/cmd_vel')
        self.declare_parameter('scan_topic', '/advika/scan')
        self.declare_parameter('camera_topic', '/advika/horizon_camera/image_raw')
        self.declare_parameter('odom_topic', '/advika/odom')
        self.declare_parameter('use_sim_time', True)

        cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        scan_topic = self.get_parameter('scan_topic').value
        camera_topic = self.get_parameter('camera_topic').value
        odom_topic = self.get_parameter('odom_topic').value

        self.bridge = CvBridge()
        self.sensor_state = SimSensorState(
            lidar_distances_mm=[0.0] * 36,
            tof_grid_mm=[[500.0] * 8 for _ in range(8)],
            odom_position={"x": 0.0, "y": 0.0, "z": 0.0, "yaw": 0.0},
            odom_velocity={"linear_x": 0.0, "angular_z": 0.0},
            timestamp=datetime.utcnow().isoformat() + "Z"
        )

        # QoS
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Subscribers
        self.scan_sub = self.create_subscription(
            LaserScan, scan_topic, self._scan_callback, sensor_qos)
        self.camera_sub = self.create_subscription(
            Image, camera_topic, self._camera_callback, sensor_qos)
        self.odom_sub = self.create_subscription(
            Odometry, odom_topic, self._odom_callback, 10)

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, cmd_vel_topic, 10)

        # State lock
        self._state_lock = threading.Lock()

        self.get_logger().info("Simulation MCP Bridge initialized")
        self.get_logger().info(f"Subscribed to: {scan_topic}, {camera_topic}, {odom_topic}")
        self.get_logger().info(f"Publishing to: {cmd_vel_topic}")

    def _scan_callback(self, msg: LaserScan):
        """Convert 360-point LiDAR to 36 buckets matching real LD06."""
        if not msg.ranges:
            return

        # Downsample 360 points to 36 buckets (10-degree resolution)
        buckets = []
        points_per_bucket = len(msg.ranges) // 36

        for i in range(36):
            start_idx = i * points_per_bucket
            end_idx = start_idx + points_per_bucket
            bucket_ranges = [
                r for r in msg.ranges[start_idx:end_idx]
                if msg.range_min < r < msg.range_max
            ]
            if bucket_ranges:
                buckets.append(min(bucket_ranges) * 1000.0)  # Convert to mm
            else:
                buckets.append(12000.0)  # Max range in mm

        with self._state_lock:
            self.sensor_state.lidar_distances_mm = buckets
            self.sensor_state.timestamp = datetime.utcnow().isoformat() + "Z"

    def _camera_callback(self, msg: Image):
        """Store latest camera frame."""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            # In simulation mode, we don't encode to base64 unless requested
            # Store the numpy array for on-demand encoding
            self._last_cv_image = cv_image
        except Exception as e:
            self.get_logger().error(f"Camera callback error: {e}")

    def _odom_callback(self, msg: Odometry):
        """Update odometry state."""
        import math

        q = msg.pose.pose.orientation
        # Convert quaternion to yaw
        siny = 2.0 * (q.w * q.z + q.x * q.y)
        cosy = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
        yaw = math.atan2(siny, cosy)

        with self._state_lock:
            self.sensor_state.odom_position = {
                "x": round(msg.pose.pose.position.x, 3),
                "y": round(msg.pose.pose.position.y, 3),
                "z": round(msg.pose.pose.position.z, 3),
                "yaw": round(yaw, 3)
            }
            self.sensor_state.odom_velocity = {
                "linear_x": round(msg.twist.twist.linear.x, 3),
                "angular_z": round(msg.twist.twist.angular.z, 3)
            }

    # ==================== MCP-COMPATIBLE METHODS ====================

    def mcp_esp32_drive(self, linear_velocity: float, angular_velocity: float, 
                        duration_ms: int) -> Dict[str, Any]:
        """
        MCP-compatible drive command.
        Identical API to real hardware bridge.
        """
        # Clamp values (same as hardware)
        linear_velocity = max(-1.0, min(1.0, linear_velocity))
        angular_velocity = max(-1.0, min(1.0, angular_velocity))
        duration_ms = max(0, min(2000, duration_ms))

        # Publish cmd_vel
        cmd = Twist()
        cmd.linear.x = linear_velocity
        cmd.angular.z = angular_velocity
        self.cmd_vel_pub.publish(cmd)

        # In simulation, we don't have a real ESP32 to confirm
        # So we simulate the response
        self.get_logger().info(
            f"SIM Drive: linear={linear_velocity}, angular={angular_velocity}, "
            f"duration={duration_ms}ms"
        )

        # If duration specified, schedule stop
        if duration_ms > 0:
            def stop_after_duration():
                time.sleep(duration_ms / 1000.0)
                stop_cmd = Twist()
                stop_cmd.linear.x = 0.0
                stop_cmd.angular.z = 0.0
                self.cmd_vel_pub.publish(stop_cmd)

            timer = threading.Thread(target=stop_after_duration, daemon=True)
            timer.start()

        return {
            "status": "success",
            "command": {
                "linear_velocity": linear_velocity,
                "angular_velocity": angular_velocity,
                "duration_ms": duration_ms
            },
            "simulated": True,
            "note": "Running in Gazebo simulation"
        }

    def mcp_get_spatial_telemetry(self) -> Dict[str, Any]:
        """
        MCP-compatible telemetry query.
        Returns identical format to real hardware bridge.
        """
        with self._state_lock:
            lidar_min = min(self.sensor_state.lidar_distances_mm) if any(self.sensor_state.lidar_distances_mm) else 9999
            tof_min = min(min(row) for row in self.sensor_state.tof_grid_mm)

            # Simulate ToF from LiDAR front buckets (indices 15-21 = front ~70 degrees)
            front_buckets = self.sensor_state.lidar_distances_mm[15:22]
            if front_buckets:
                front_min = min(front_buckets)
                # Populate ToF grid with simulated values
                for row in range(8):
                    for col in range(8):
                        # Simulate varying distances across the 8x8 grid
                        noise = np.random.normal(0, 20)
                        self.sensor_state.tof_grid_mm[row][col] = max(20, front_min + noise)

            collision_risk = tof_min < 120 or lidar_min < 200
            obstacle_detected = tof_min < 150

            return {
                "lidar": {
                    "distances_mm": self.sensor_state.lidar_distances_mm,
                    "min_distance_mm": int(lidar_min),
                    "buckets": 36,
                    "angular_resolution_deg": 10
                },
                "tof": {
                    "grid_mm": self.sensor_state.tof_grid_mm,
                    "min_distance_mm": int(tof_min),
                    "resolution": "8x8",
                    "fov_deg": 63
                },
                "bms": {
                    "voltage_v": 11.4,
                    "current_a": 0.5,
                    "soc_percent": 85,
                    "temperature_c": 32.0,
                    "cell_count": 3,
                    "cell_type": "LiPo",
                    "status": "ok"
                },
                "safety": {
                    "collision_risk": collision_risk,
                    "obstacle_detected": obstacle_detected,
                    "tof_collision_threshold_mm": 120,
                    "lidar_collision_threshold_mm": 200,
                    "tof_obstacle_threshold_mm": 150
                },
                "odometry": self.sensor_state.odom_position,
                "velocity": self.sensor_state.odom_velocity,
                "timestamp": self.sensor_state.timestamp,
                "simulated": True
            }

    def mcp_stop_motors(self) -> Dict[str, Any]:
        """Emergency stop - identical to hardware API."""
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)

        self.get_logger().warn("SIM Emergency STOP triggered")
        return {"status": "stopped", "simulated": True}

    def mcp_speak_message(self, message: str) -> Dict[str, Any]:
        """TTS - simulated (prints to log instead of speaking)."""
        message = message[:200]
        self.get_logger().info(f"[SIM TTS] {message}")
        return {"status": "spoken", "message": message, "simulated": True}

    def mcp_capture_stitched_frame(self, annotate: bool = True, 
                                    detect_objects: bool = True) -> Dict[str, Any]:
        """Capture camera frame - simulated."""
        if not hasattr(self, '_last_cv_image') or self._last_cv_image is None:
            return {
                "status": "error",
                "error": "No camera frame available",
                "simulated": True
            }

        import base64
        import cv2

        frame = self._last_cv_image.copy()

        # Add simulation watermark
        cv2.putText(frame, "SIMULATION MODE", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        frame_b64 = base64.b64encode(buffer).decode('utf-8')

        return {
            "status": "success",
            "frame_base64": frame_b64,
            "frame_dimensions": {
                "width": frame.shape[1],
                "height": frame.shape[0]
            },
            "detections": [],
            "detection_count": 0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "simulated": True
        }

    def mcp_get_motor_telemetry(self) -> Dict[str, Any]:
        """Motor telemetry - simulated from odometry."""
        with self._state_lock:
            return {
                "status": "success",
                "motors": {
                    "left_encoder": int(self.sensor_state.odom_position["x"] * 1000),
                    "right_encoder": int(self.sensor_state.odom_position["y"] * 1000),
                    "left_velocity": self.sensor_state.odom_velocity["linear_x"],
                    "right_velocity": self.sensor_state.odom_velocity["angular_z"],
                    "left_pwm": int(self.sensor_state.odom_velocity["linear_x"] * 255),
                    "right_pwm": int(self.sensor_state.odom_velocity["angular_z"] * 255),
                    "estop_active": False,
                    "motors_enabled": True,
                    "uptime_ms": int(time.time() * 1000)
                },
                "simulated": True
            }


# ==================== STANDALONE MCP SERVER ====================
if MCP_AVAILABLE:
    mcp = FastMCP("advika_sim_mcp_bridge")
    _ros_node: Optional[SimMCPBridgeNode] = None

    @mcp.tool()
    def mcp_esp32_drive(linear_velocity: float, angular_velocity: float, 
                        duration_ms: int) -> Dict[str, Any]:
        if _ros_node:
            return _ros_node.mcp_esp32_drive(linear_velocity, angular_velocity, duration_ms)
        return {"error": "ROS node not initialized"}

    @mcp.tool()
    def mcp_get_spatial_telemetry() -> Dict[str, Any]:
        if _ros_node:
            return _ros_node.mcp_get_spatial_telemetry()
        return {"error": "ROS node not initialized"}

    @mcp.tool()
    def mcp_stop_motors() -> Dict[str, Any]:
        if _ros_node:
            return _ros_node.mcp_stop_motors()
        return {"error": "ROS node not initialized"}

    @mcp.tool()
    def mcp_speak_message(message: str) -> Dict[str, Any]:
        if _ros_node:
            return _ros_node.mcp_speak_message(message)
        return {"error": "ROS node not initialized"}

    @mcp.tool()
    def mcp_capture_stitched_frame(annotate: bool = True, 
                                    detect_objects: bool = True) -> Dict[str, Any]:
        if _ros_node:
            return _ros_node.mcp_capture_stitched_frame(annotate, detect_objects)
        return {"error": "ROS node not initialized"}

    @mcp.tool()
    def mcp_get_motor_telemetry() -> Dict[str, Any]:
        if _ros_node:
            return _ros_node.mcp_get_motor_telemetry()
        return {"error": "ROS node not initialized"}


def main(args=None):
    rclpy.init(args=args)
    global _ros_node

    node = SimMCPBridgeNode()
    _ros_node = node

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
