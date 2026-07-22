#!/usr/bin/env python3
"""
Advika 3.0 -- Simulation Safety Monitor
Independent safety node that monitors sensor data and can override
motor commands to prevent collisions in simulation.
This mirrors the hardware safety_interrupt.h behavior.
"""

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Bool
import math


class SafetyMonitorNode(Node):
    """
    Safety monitor that:
    1. Monitors LiDAR scan for obstacles
    2. Overrides cmd_vel if collision imminent
    3. Publishes safety state for HITL
    4. Implements recovery procedures
    """

    def __init__(self):
        super().__init__('safety_monitor')

        # Parameters
        self.declare_parameter('scan_topic', '/advika/scan')
        self.declare_parameter('cmd_vel_topic', '/advika/cmd_vel')
        self.declare_parameter('safety_cmd_topic', '/advika/safety_cmd_vel')
        self.declare_parameter('collision_threshold_m', 0.15)
        self.declare_parameter('obstacle_threshold_m', 0.20)
        self.declare_parameter('recovery_reverse_m', 0.1)
        self.declare_parameter('recovery_turn_deg', 45.0)
        self.declare_parameter('use_sim_time', True)

        scan_topic = self.get_parameter('scan_topic').value
        cmd_vel_topic = self.get_parameter('cmd_vel_topic').value
        safety_cmd_topic = self.get_parameter('safety_cmd_topic').value
        self.collision_threshold = self.get_parameter('collision_threshold_m').value
        self.obstacle_threshold = self.get_parameter('obstacle_threshold_m').value
        self.recovery_reverse = self.get_parameter('recovery_reverse_m').value
        self.recovery_turn = math.radians(self.get_parameter('recovery_turn_deg').value)

        # State
        self.safety_active = False
        self.recovery_mode = False
        self.last_scan: LaserScan = None
        self.last_cmd_vel: Twist = None

        # QoS
        sensor_qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # Subscribers
        self.scan_sub = self.create_subscription(
            LaserScan, scan_topic, self._scan_callback, sensor_qos)
        self.cmd_vel_sub = self.create_subscription(
            Twist, cmd_vel_topic, self._cmd_vel_callback, 10)

        # Publishers
        self.safety_cmd_pub = self.create_publisher(Twist, safety_cmd_topic, 10)
        self.safety_state_pub = self.create_publisher(Bool, '/advika/safety_active', 10)

        # Timer for safety checks (100Hz)
        self.safety_timer = self.create_timer(0.01, self._safety_check)

        # Recovery timer
        self.recovery_timer = None
        self.recovery_phase = 0

        self.get_logger().info("Safety Monitor initialized")
        self.get_logger().info(f"Collision threshold: {self.collision_threshold}m")
        self.get_logger().info(f"Obstacle threshold: {self.obstacle_threshold}m")

    def _scan_callback(self, msg: LaserScan):
        self.last_scan = msg

    def _cmd_vel_callback(self, msg: Twist):
        self.last_cmd_vel = msg

    def _safety_check(self):
        if self.last_scan is None:
            return

        # Get minimum distance in front sector (-30 to +30 degrees)
        front_ranges = []
        for i, r in enumerate(self.last_scan.ranges):
            angle = self.last_scan.angle_min + i * self.last_scan.angle_increment
            if abs(angle) < math.radians(30):  # Front 60-degree cone
                if self.last_scan.range_min < r < self.last_scan.range_max:
                    front_ranges.append(r)

        if not front_ranges:
            return

        min_front = min(front_ranges)

        # Check for collision
        if min_front < self.collision_threshold and not self.safety_active:
            self._trigger_safety_stop(min_front)

        # Check for obstacle
        elif min_front < self.obstacle_threshold and not self.safety_active:
            self._trigger_obstacle_avoidance(min_front)

        # Publish safety state
        safety_msg = Bool()
        safety_msg.data = self.safety_active
        self.safety_state_pub.publish(safety_msg)

    def _trigger_safety_stop(self, distance: float):
        """Hard collision limit triggered - immediate stop."""
        self.safety_active = True
        self.get_logger().error(
            f"COLLISION ALERT: Object at {distance:.3f}m. "
            f"Hard limit is {self.collision_threshold}m. STOPPING!"
        )

        # Immediate stop
        stop_cmd = Twist()
        stop_cmd.linear.x = 0.0
        stop_cmd.angular.z = 0.0
        self.safety_cmd_pub.publish(stop_cmd)

        # Start recovery procedure
        self._start_recovery()

    def _trigger_obstacle_avoidance(self, distance: float):
        """Obstacle detected - slow down or stop."""
        self.get_logger().warn(
            f"OBSTACLE: Object at {distance:.3f}m. "
            f"Threshold is {self.obstacle_threshold}m."
        )

        # If moving forward, reduce speed proportionally
        if self.last_cmd_vel and self.last_cmd_vel.linear.x > 0:
            slowdown = Twist()
            slowdown.linear.x = self.last_cmd_vel.linear.x * (distance / self.obstacle_threshold)
            slowdown.angular.z = self.last_cmd_vel.angular.z
            self.safety_cmd_pub.publish(slowdown)

    def _start_recovery(self):
        """
        Obstacle Recovery Procedure:
        1. Halt motors (done)
        2. Reverse 100mm
        3. Turn 45 degrees away
        4. Re-scan
        """
        self.recovery_mode = True
        self.recovery_phase = 0
        self.get_logger().info("Starting obstacle recovery procedure...")

        # Phase 1: Reverse
        self._execute_recovery_phase(0)

    def _execute_recovery_phase(self, phase: int):
        """Execute a single phase of recovery."""
        cmd = Twist()

        if phase == 0:
            # Reverse
            cmd.linear.x = -0.1  # 0.1 m/s backward
            self.safety_cmd_pub.publish(cmd)
            self.get_logger().info("Recovery: Reversing...")

            # Schedule next phase after 1 second (100mm at 0.1 m/s)
            self.recovery_timer = self.create_timer(1.0, lambda: self._next_recovery_phase())

        elif phase == 1:
            # Turn 45 degrees
            cmd.angular.z = 0.5  # rad/s
            self.safety_cmd_pub.publish(cmd)
            self.get_logger().info("Recovery: Turning away...")

            # Schedule stop after 0.8 seconds (45 deg at 0.5 rad/s ~= 0.785 rad)
            self.recovery_timer = self.create_timer(0.8, lambda: self._next_recovery_phase())

        elif phase == 2:
            # Stop and clear safety
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            self.safety_cmd_pub.publish(cmd)
            self.safety_active = False
            self.recovery_mode = False
            self.get_logger().info("Recovery complete. Safety cleared.")

    def _next_recovery_phase(self):
        """Advance to next recovery phase."""
        if self.recovery_timer:
            self.recovery_timer.cancel()
            self.recovery_timer = None

        self.recovery_phase += 1
        if self.recovery_phase <= 2:
            self._execute_recovery_phase(self.recovery_phase)


def main(args=None):
    rclpy.init(args=args)
    node = SafetyMonitorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
