#!/usr/bin/env python3
"""
Advika 3.0 -- HITL (Human-in-the-Loop) Bridge
WebSocket-based real-time interface for human oversight of AI agent decisions.
Features: live video feed, sensor telemetry, manual override, approval queues,
          safety alerts, and mission control dashboard.

HITL Modes:
  - FULL_AUTO: Agent makes all decisions, human monitors only
  - SUPERVISED: Agent proposes actions, human must approve each step
  - MANUAL: Human controls everything, AI provides suggestions
  - EMERGENCY: All AI control suspended, human takes full control
"""

import os
import sys
import json
import time
import asyncio
import threading
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Callable, Any
from enum import Enum
from collections import deque

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan, Image, Imu
from nav_msgs.msg import Odometry
from cv_bridge import CvBridge
import numpy as np

# Web framework
try:
    from fastapi import FastAPI, WebSocket, WebSocketDisconnect
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    from starlette.requests import Request
    import uvicorn
    WEB_AVAILABLE = True
except ImportError:
    WEB_AVAILABLE = False
    print("WARNING: FastAPI/uvicorn not installed. HITL web interface disabled.")

# ==================== ENUMS ====================
class HITLMode(Enum):
    FULL_AUTO = "full_auto"
    SUPERVISED = "supervised"
    MANUAL = "manual"
    EMERGENCY = "emergency"

class ActionStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXECUTED = "executed"
    TIMEOUT = "timeout"
    SAFETY_BLOCKED = "safety_blocked"

class SafetyLevel(Enum):
    NORMAL = "normal"
    CAUTION = "caution"
    WARNING = "warning"
    CRITICAL = "critical"

# ==================== DATA CLASSES ====================
@dataclass
class PendingAction:
    action_id: str
    timestamp: str
    goal: str
    proposed_action: str
    parameters: Dict[str, Any]
    tof_min_mm: int
    lidar_min_mm: int
    status: str = "pending"
    human_decision: Optional[str] = None
    decision_timestamp: Optional[str] = None
    timeout_sec: float = 10.0

@dataclass
class SafetyEvent:
    timestamp: str
    level: str
    message: str
    sensor_data: Dict[str, Any]
    action_taken: str

@dataclass
class TelemetrySnapshot:
    timestamp: str
    pose: Dict[str, float]
    velocity: Dict[str, float]
    lidar_min_m: float
    tof_min_m: float
    battery_voltage: float
    mode: str
    pending_actions: int
    safety_level: str

# ==================== HITL MANAGER ====================
class HITLManager:
    """Central HITL state manager - thread-safe singleton."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.mode = HITLMode.SUPERVISED
        self.pending_actions: deque = deque(maxlen=50)
        self.safety_events: deque = deque(maxlen=100)
        self.telemetry_history: deque = deque(maxlen=1000)
        self.connected_clients: set = set()
        self._callbacks: Dict[str, List[Callable]] = {
            'mode_change': [],
            'action_approved': [],
            'action_rejected': [],
            'safety_alert': [],
            'emergency_stop': []
        }
        self._lock = threading.Lock()
        self._initialized = True
        self.emergency_stop_active = False
        self.approval_timeout_sec = 10.0
        self.auto_approve_below_risk = False
        self.risk_threshold_mm = 300

    def register_callback(self, event: str, callback: Callable):
        """Register a callback for HITL events."""
        if event in self._callbacks:
            self._callbacks[event].append(callback)

    def _notify(self, event: str, data: Any = None):
        """Notify all registered callbacks."""
        for callback in self._callbacks.get(event, []):
            try:
                callback(data)
            except Exception as e:
                print(f"HITL callback error: {e}")

    def set_mode(self, mode: HITLMode):
        """Change HITL operating mode."""
        with self._lock:
            old_mode = self.mode
            self.mode = mode

            if mode == HITLMode.EMERGENCY:
                self.emergency_stop_active = True
                self._notify('emergency_stop', {"reason": "mode_change", "from": old_mode.value})
            else:
                self.emergency_stop_active = False

            self._notify('mode_change', {"from": old_mode.value, "to": mode.value})

    def request_action_approval(self, goal: str, action: str, params: Dict,
                                 tof_min: int, lidar_min: int) -> Optional[str]:
        """
        Request human approval for an AI-proposed action.
        Returns action_id if queued, None if auto-approved/rejected.
        """
        with self._lock:
            # Emergency mode: block everything
            if self.mode == HITLMode.EMERGENCY:
                return None

            # Full auto mode: approve immediately
            if self.mode == HITLMode.FULL_AUTO:
                return "auto_approved"

            # Manual mode: reject (human controls)
            if self.mode == HITLMode.MANUAL:
                return None

            # Auto-approve low-risk actions
            if self.auto_approve_below_risk:
                if tof_min > self.risk_threshold_mm and lidar_min > self.risk_threshold_mm:
                    return "auto_approved_low_risk"

            # Queue for human approval (SUPERVISED mode)
            action_id = f"act_{int(time.time() * 1000)}_{len(self.pending_actions)}"
            pending = PendingAction(
                action_id=action_id,
                timestamp=datetime.utcnow().isoformat() + "Z",
                goal=goal,
                proposed_action=action,
                parameters=params,
                tof_min_mm=tof_min,
                lidar_min_mm=lidar_min,
                timeout_sec=self.approval_timeout_sec
            )
            self.pending_actions.append(pending)

            # Notify connected clients
            asyncio.create_task(self._broadcast_action_request(pending))

            return action_id

    def approve_action(self, action_id: str, approved_by: str = "human") -> bool:
        """Human approves a pending action."""
        with self._lock:
            for action in self.pending_actions:
                if action.action_id == action_id and action.status == "pending":
                    action.status = "approved"
                    action.human_decision = approved_by
                    action.decision_timestamp = datetime.utcnow().isoformat() + "Z"
                    self._notify('action_approved', asdict(action))
                    asyncio.create_task(self._broadcast_action_update(action))
                    return True
            return False

    def reject_action(self, action_id: str, reason: str = "human_rejected") -> bool:
        """Human rejects a pending action."""
        with self._lock:
            for action in self.pending_actions:
                if action.action_id == action_id and action.status == "pending":
                    action.status = "rejected"
                    action.human_decision = reason
                    action.decision_timestamp = datetime.utcnow().isoformat() + "Z"
                    self._notify('action_rejected', asdict(action))
                    asyncio.create_task(self._broadcast_action_update(action))
                    return True
            return False

    def add_safety_event(self, level: SafetyLevel, message: str, sensor_data: Dict, action_taken: str):
        """Record a safety event."""
        event = SafetyEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            level=level.value,
            message=message,
            sensor_data=sensor_data,
            action_taken=action_taken
        )
        with self._lock:
            self.safety_events.append(event)

        self._notify('safety_alert', asdict(event))
        asyncio.create_task(self._broadcast_safety_event(event))

    def add_telemetry(self, snapshot: TelemetrySnapshot):
        """Add telemetry snapshot to history."""
        with self._lock:
            self.telemetry_history.append(snapshot)

    async def _broadcast_action_request(self, action: PendingAction):
        """Broadcast action request to all connected WebSocket clients."""
        message = {
            "type": "action_request",
            "data": asdict(action)
        }
        await self._broadcast(message)

    async def _broadcast_action_update(self, action: PendingAction):
        """Broadcast action status update."""
        message = {
            "type": "action_update",
            "data": asdict(action)
        }
        await self._broadcast(message)

    async def _broadcast_safety_event(self, event: SafetyEvent):
        """Broadcast safety event."""
        message = {
            "type": "safety_alert",
            "data": asdict(event)
        }
        await self._broadcast(message)

    async def _broadcast_telemetry(self, snapshot: TelemetrySnapshot):
        """Broadcast telemetry snapshot."""
        message = {
            "type": "telemetry",
            "data": asdict(snapshot)
        }
        await self._broadcast(message)

    async def _broadcast(self, message: Dict):
        """Send message to all connected WebSocket clients."""
        if not self.connected_clients:
            return

        disconnected = set()
        for client in self.connected_clients:
            try:
                await client.send_json(message)
            except Exception:
                disconnected.add(client)

        self.connected_clients -= disconnected

    def get_pending_actions(self) -> List[Dict]:
        """Get all pending actions."""
        with self._lock:
            return [asdict(a) for a in self.pending_actions if a.status == "pending"]

    def get_safety_events(self, limit: int = 50) -> List[Dict]:
        """Get recent safety events."""
        with self._lock:
            return [asdict(e) for e in list(self.safety_events)[-limit:]]

    def get_telemetry_history(self, limit: int = 100) -> List[Dict]:
        """Get recent telemetry."""
        with self._lock:
            return [asdict(t) for t in list(self.telemetry_history)[-limit:]]


# ==================== ROS2 NODE ====================
class HITLBridgeNode(Node):
    """ROS2 node that bridges simulation topics to HITL manager."""

    def __init__(self):
        super().__init__('hitl_bridge')

        self.hitl = HITLManager()
        self.bridge = CvBridge()
        self.current_scan: Optional[LaserScan] = None
        self.current_odom: Optional[Odometry] = None
        self.current_image: Optional[np.ndarray] = None

        # QoS profiles
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Subscribers
        self.scan_sub = self.create_subscription(
            LaserScan, '/advika/scan', self._scan_callback, sensor_qos)
        self.odom_sub = self.create_subscription(
            Odometry, '/advika/odom', self._odom_callback, 10)
        self.image_sub = self.create_subscription(
            Image, '/advika/horizon_camera/image_raw', self._image_callback, sensor_qos)
        self.imu_sub = self.create_subscription(
            Imu, '/advika/imu/data', self._imu_callback, sensor_qos)

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, '/advika/cmd_vel', 10)
        self.safety_cmd_pub = self.create_publisher(Twist, '/advika/safety_cmd_vel', 10)

        # Timer for telemetry publishing
        self.telemetry_timer = self.create_timer(0.1, self._publish_telemetry)

        # Register HITL callbacks
        self.hitl.register_callback('action_approved', self._on_action_approved)
        self.hitl.register_callback('action_rejected', self._on_action_rejected)
        self.hitl.register_callback('emergency_stop', self._on_emergency_stop)
        self.hitl.register_callback('safety_alert', self._on_safety_alert)

        self.get_logger().info("HITL Bridge Node initialized")

    def _scan_callback(self, msg: LaserScan):
        self.current_scan = msg

        # Safety check
        if msg.ranges:
            min_range = min(r for r in msg.ranges if r > msg.range_min)
            if min_range < 0.15:
                self.hitl.add_safety_event(
                    SafetyLevel.CRITICAL,
                    f"Collision imminent! Object at {min_range:.2f}m",
                    {"lidar_min_m": min_range, "sector": "front"},
                    "emergency_stop_triggered"
                )
                self._publish_emergency_stop()
            elif min_range < 0.20:
                self.hitl.add_safety_event(
                    SafetyLevel.WARNING,
                    f"Obstacle detected at {min_range:.2f}m",
                    {"lidar_min_m": min_range},
                    "slow_down"
                )

    def _odom_callback(self, msg: Odometry):
        self.current_odom = msg

    def _image_callback(self, msg: Image):
        try:
            self.current_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f"Image conversion error: {e}")

    def _imu_callback(self, msg: Imu):
        pass  # IMU data available if needed

    def _publish_telemetry(self):
        if self.current_odom is None:
            return

        pose = self.current_odom.pose.pose
        twist = self.current_odom.twist.twist

        lidar_min = 999.0
        if self.current_scan and self.current_scan.ranges:
            valid = [r for r in self.current_scan.ranges 
                     if self.current_scan.range_min < r < self.current_scan.range_max]
            if valid:
                lidar_min = min(valid)

        snapshot = TelemetrySnapshot(
            timestamp=datetime.utcnow().isoformat() + "Z",
            pose={
                "x": pose.position.x,
                "y": pose.position.y,
                "z": pose.position.z,
                "qx": pose.orientation.x,
                "qy": pose.orientation.y,
                "qz": pose.orientation.z,
                "qw": pose.orientation.w
            },
            velocity={
                "linear_x": twist.linear.x,
                "angular_z": twist.angular.z
            },
            lidar_min_m=round(lidar_min, 3),
            tof_min_m=round(lidar_min * 0.95, 3),  # Simulated ToF
            battery_voltage=11.4,  # Simulated
            mode=self.hitl.mode.value,
            pending_actions=len(self.hitl.get_pending_actions()),
            safety_level=SafetyLevel.NORMAL.value if lidar_min > 0.3 else 
                        SafetyLevel.WARNING.value if lidar_min > 0.15 else SafetyLevel.CRITICAL.value
        )

        self.hitl.add_telemetry(snapshot)

        # Async broadcast
        try:
            loop = asyncio.get_event_loop()
            loop.create_task(self.hitl._broadcast_telemetry(snapshot))
        except RuntimeError:
            pass

    def _on_action_approved(self, action_data: Dict):
        self.get_logger().info(f"Action approved: {action_data['proposed_action']}")
        # Execute the approved action
        self._execute_action(action_data)

    def _on_action_rejected(self, action_data: Dict):
        self.get_logger().warn(f"Action rejected: {action_data['proposed_action']}")

    def _on_emergency_stop(self, data: Dict):
        self.get_logger().error(f"EMERGENCY STOP: {data}")
        self._publish_emergency_stop()

    def _on_safety_alert(self, event_data: Dict):
        self.get_logger().warn(f"Safety alert: {event_data['message']}")

    def _publish_emergency_stop(self):
        stop_cmd = Twist()
        stop_cmd.linear.x = 0.0
        stop_cmd.angular.z = 0.0
        self.safety_cmd_pub.publish(stop_cmd)
        self.cmd_vel_pub.publish(stop_cmd)

    def _execute_action(self, action_data: Dict):
        """Execute an approved action by publishing cmd_vel."""
        params = action_data.get('parameters', {})
        cmd = Twist()

        if action_data['proposed_action'] == 'drive':
            cmd.linear.x = params.get('linear_velocity', 0.0)
            cmd.angular.z = params.get('angular_velocity', 0.0)
        elif action_data['proposed_action'] == 'stop':
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0

        self.cmd_vel_pub.publish(cmd)

    def manual_drive(self, linear: float, angular: float):
        """Manual drive command from human operator."""
        if self.hitl.mode == HITLMode.EMERGENCY:
            self.get_logger().warn("Cannot drive in EMERGENCY mode")
            return

        cmd = Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        self.cmd_vel_pub.publish(cmd)


# ==================== WEB INTERFACE ====================
if WEB_AVAILABLE:
    app = FastAPI(title="Advika HITL Control Center")
    hitl_manager = HITLManager()
    ros_node: Optional[HITLBridgeNode] = None

    # Static files and templates
    static_dir = os.path.join(os.path.dirname(__file__), 'web_interface', 'static')
    templates_dir = os.path.join(os.path.dirname(__file__), 'web_interface', 'templates')

    if os.path.exists(static_dir):
        app.mount("/static", StaticFiles(directory=static_dir), name="static")
    templates = Jinja2Templates(directory=templates_dir if os.path.exists(templates_dir) else ".")

    @app.get("/", response_class=HTMLResponse)
    async def dashboard(request: Request):
        """Main HITL dashboard."""
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "mode": hitl_manager.mode.value,
            "pending_count": len(hitl_manager.get_pending_actions())
        })

    @app.get("/api/status")
    async def api_status():
        """Get current HITL status."""
        return JSONResponse({
            "mode": hitl_manager.mode.value,
            "emergency_stop": hitl_manager.emergency_stop_active,
            "pending_actions": len(hitl_manager.get_pending_actions()),
            "connected_clients": len(hitl_manager.connected_clients),
            "safety_events_count": len(hitl_manager.safety_events),
            "telemetry_points": len(hitl_manager.telemetry_history)
        })

    @app.get("/api/pending_actions")
    async def api_pending_actions():
        """Get all pending actions requiring approval."""
        return JSONResponse({"actions": hitl_manager.get_pending_actions()})

    @app.post("/api/approve/{action_id}")
    async def api_approve_action(action_id: str):
        """Approve a pending action."""
        success = hitl_manager.approve_action(action_id, "web_operator")
        return JSONResponse({"success": success, "action_id": action_id})

    @app.post("/api/reject/{action_id}")
    async def api_reject_action(action_id: str, reason: str = "operator_rejected"):
        """Reject a pending action."""
        success = hitl_manager.reject_action(action_id, reason)
        return JSONResponse({"success": success, "action_id": action_id})

    @app.post("/api/mode/{mode}")
    async def api_set_mode(mode: str):
        """Set HITL operating mode."""
        try:
            new_mode = HITLMode(mode)
            hitl_manager.set_mode(new_mode)
            return JSONResponse({"success": True, "mode": mode})
        except ValueError:
            return JSONResponse({"success": False, "error": f"Invalid mode: {mode}"}, 400)

    @app.post("/api/emergency_stop")
    async def api_emergency_stop():
        """Trigger emergency stop."""
        hitl_manager.set_mode(HITLMode.EMERGENCY)
        return JSONResponse({"success": True, "message": "Emergency stop activated"})

    @app.post("/api/manual_drive")
    async def api_manual_drive(linear: float = 0.0, angular: float = 0.0):
        """Send manual drive command."""
        if ros_node:
            ros_node.manual_drive(linear, angular)
            return JSONResponse({"success": True})
        return JSONResponse({"success": False, "error": "ROS node not available"}, 503)

    @app.get("/api/telemetry")
    async def api_telemetry(limit: int = 100):
        """Get telemetry history."""
        return JSONResponse({"telemetry": hitl_manager.get_telemetry_history(limit)})

    @app.get("/api/safety_events")
    async def api_safety_events(limit: int = 50):
        """Get safety events."""
        return JSONResponse({"events": hitl_manager.get_safety_events(limit)})

    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """WebSocket for real-time updates."""
        await websocket.accept()
        hitl_manager.connected_clients.add(websocket)

        try:
            # Send initial state
            await websocket.send_json({
                "type": "connected",
                "data": {
                    "mode": hitl_manager.mode.value,
                    "pending_actions": hitl_manager.get_pending_actions()
                }
            })

            while True:
                # Receive commands from client
                data = await websocket.receive_json()

                if data.get("type") == "approve":
                    hitl_manager.approve_action(data.get("action_id"), "websocket_operator")
                elif data.get("type") == "reject":
                    hitl_manager.reject_action(data.get("action_id"), data.get("reason", "rejected"))
                elif data.get("type") == "mode_change":
                    try:
                        hitl_manager.set_mode(HITLMode(data.get("mode")))
                    except ValueError:
                        await websocket.send_json({"type": "error", "message": "Invalid mode"})
                elif data.get("type") == "manual_drive":
                    if ros_node:
                        ros_node.manual_drive(
                            data.get("linear", 0.0),
                            data.get("angular", 0.0)
                        )
                elif data.get("type") == "emergency_stop":
                    hitl_manager.set_mode(HITLMode.EMERGENCY)

        except WebSocketDisconnect:
            hitl_manager.connected_clients.discard(websocket)
        except Exception as e:
            print(f"WebSocket error: {e}")
            hitl_manager.connected_clients.discard(websocket)


# ==================== MAIN ====================
def main_ros(args=None):
    """ROS2 node entry point."""
    rclpy.init(args=args)
    global ros_node
    ros_node = HITLBridgeNode()

    try:
        rclpy.spin(ros_node)
    except KeyboardInterrupt:
        pass
    finally:
        ros_node.destroy_node()
        rclpy.shutdown()


def main_web():
    """Web server entry point."""
    if not WEB_AVAILABLE:
        print("FastAPI not available. Install with: pip install fastapi uvicorn")
        return

    port = int(os.getenv("HITL_PORT", "8080"))
    print(f"Starting HITL web server on http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ros", action="store_true", help="Run ROS2 node")
    parser.add_argument("--web", action="store_true", help="Run web server")
    parser.add_argument("--both", action="store_true", help="Run both")
    args = parser.parse_args()

    if args.ros:
        main_ros()
    elif args.web:
        main_web()
    elif args.both:
        # Run both in separate threads
        ros_thread = threading.Thread(target=main_ros)
        ros_thread.daemon = True
        ros_thread.start()
        main_web()
    else:
        print("Usage: python3 hitl_bridge.py [--ros|--web|--both]")
