"""
ADVIKA 3.0 — Web Teleop Dashboard Server
Flask + Flask-SocketIO + ROS2 bridge.
Runs on: http://localhost:5000
"""

import os
import threading
import math
import json
import base64
from io import BytesIO

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import os

# ── ROS2 imports (optional — dashboard works without ROS for demo) ──────────
try:
    import rclpy
    from rclpy.node import Node
    from geometry_msgs.msg import Twist
    from sensor_msgs.msg import Image, Imu, LaserScan
    from nav_msgs.msg import Odometry
    import sensor_msgs.msg
    ROS2_AVAILABLE = True
except ImportError:
    ROS2_AVAILABLE = False
    print("[Dashboard] ROS2 not available — running in demo mode")


# ── Flask App ─────────────────────────────────────────────────────────────────
app = Flask(__name__, template_folder='static', static_folder='static')
app.config['SECRET_KEY'] = 'advika-secret-2026'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet',
                    ping_timeout=120000, ping_interval=25000)

# ── Shared State ───────────────────────────────────────────────────────────────
state = {
    'linear_x':  0.0,
    'angular_z': 0.0,
    'e_stop':    False,
    'auto_mode': False,
    'robot_x':   0.0,
    'robot_y':   0.0,
    'robot_yaw': 0.0,
    'battery':   100.0,
    'lidar_ranges': [3.0] * 360,
    'imu_ax': 0.0, 'imu_ay': 0.0, 'imu_az': 0.0,
    'imu_gx': 0.0, 'imu_gy': 0.0, 'imu_gz': 0.0,
    'fps_horizon': 0, 'fps_floor': 0,
}

state_lock = threading.Lock()


# ── Pages ─────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/state')
def get_state():
    with state_lock:
        return jsonify({
            'linear_x':  round(state['linear_x'], 3),
            'angular_z': round(state['angular_z'], 3),
            'e_stop':    state['e_stop'],
            'auto_mode': state['auto_mode'],
            'robot_x':   round(state['robot_x'], 3),
            'robot_y':   round(state['robot_y'], 3),
            'robot_yaw': round(state['robot_y'], 3),
            'battery':   round(state['battery'], 1),
            'fps_horizon': state['fps_horizon'],
            'fps_floor':   state['fps_floor'],
        })


@app.route('/api/lidar')
def get_lidar():
    with state_lock:
        return jsonify({'ranges': state['lidar_ranges']})


@app.route('/api/imu')
def get_imu():
    with state_lock:
        return jsonify({
            'accel': {'x': round(state['imu_ax'], 4),
                      'y': round(state['imu_ay'], 4),
                      'z': round(state['imu_az'], 4)},
            'gyro':  {'x': round(state['imu_gx'], 4),
                      'y': round(state['imu_gy'], 4),
                      'z': round(state['imu_gz'], 4)},
        })


# ── Telemetry Polling (pushes to web) ─────────────────────────────────────────
def telemetry_loop():
    while True:
        socketio.sleep(0.1)
        with state_lock:
            s = dict(state)
        socketio.emit('telemetry', {
            'robot_x':   round(s['robot_x'], 3),
            'robot_y':   round(s['robot_y'], 3),
            'robot_yaw': round(s['robot_yaw'], 3),
            'battery':   round(s['battery'], 1),
            'fps_h':     s['fps_horizon'],
            'fps_f':     s['fps_floor'],
            'e_stop':    s['e_stop'],
        }, namespace='/')


# ── WebSocket Events ──────────────────────────────────────────────────────────
@socketio.on('connect')
def on_connect():
    print(f"[Dashboard] Client connected: {request.sid}")


@socketio.on('disconnect')
def on_disconnect():
    print(f"[Dashboard] Client disconnected: {request.sid}")


@socketio.on('cmd_vel')
def on_cmd_vel(data):
    """Receive teleop command from web UI."""
    with state_lock:
        state['linear_x']  = max(-0.5, min(0.5, float(data.get('linear_x', 0.0))))
        state['angular_z'] = max(-1.0, min(1.0, float(data.get('angular_z', 0.0))))
        state['auto_mode'] = False
    emit('cmd_ack', {'ok': True})


@socketio.on('e_stop')
def on_e_stop():
    with state_lock:
        state['e_stop'] = True
        state['linear_x'] = 0.0
        state['angular_z'] = 0.0
    print("[Dashboard] E-STOP ACTIVATED")
    emit('cmd_ack', {'ok': True, 'e_stop': True})


@socketio.on('e_stop_reset')
def on_e_stop_reset():
    with state_lock:
        state['e_stop'] = False
    emit('cmd_ack', {'ok': True, 'e_stop': False})


@socketio.on('auto_mode')
def on_auto_mode(data):
    with state_lock:
        state['auto_mode'] = bool(data.get('enabled', False))
    emit('cmd_ack', {'ok': True})


@socketio.on('camera_frame')
def on_camera_frame(data):
    """Receive JPEG frame from ROS bridge, broadcast to all clients."""
    if data.get('camera') in ('horizon', 'floor'):
        socketio.emit('camera_frame', data, include_self=False)


@socketio.on('nav_goal')
def on_nav_goal(data):
    """Receive a 2D navigation goal (x, y)."""
    goal = {
        'x': float(data.get('x', 0)),
        'y': float(data.get('y', 0)),
        'theta': float(data.get('theta', 0)),
    }
    print(f"[Dashboard] Navigation goal: {goal}")
    emit('cmd_ack', {'ok': True})


# ── ROS2 Bridge Node (runs in background thread) ───────────────────────────────
class DashboardNode(Node if ROS2_AVAILABLE else object):
    last_odom_time = 0

    def __init__(self):
        if not ROS2_AVAILABLE:
            return
        super().__init__('advika_dashboard_bridge')
        self.cmd_pub = self.create_publisher(Twist, '/advika/cmd_vel', 10)
        self.create_subscription(Odometry, '/advika/odom', self.on_odom, 10)
        self.create_subscription(LaserScan, '/advika/scan', self.on_lidar, 10)
        self.create_subscription(Imu, '/advika/imu/data', self.on_imu, 10)

        self.get_logger().info('Dashboard ROS2 bridge started')

        # Timer: publish cmd_vel from state
        self.create_timer(0.05, self.pub_cmd)

        # Start spin in background
        self._spin_thread = threading.Thread(target=lambda: rclpy.spin(self), daemon=True)
        self._spin_thread.start()

    def pub_cmd(self):
        if not ROS2_AVAILABLE:
            return
        with state_lock:
            if state['e_stop']:
                return
            if state['auto_mode']:
                return  # autonomous stack handles it
            v = Twist()
            v.linear.x  = state['linear_x']
            v.angular.z = state['angular_z']
            self.cmd_pub.publish(v)

    def on_odom(self, msg):
        with state_lock:
            state['robot_x']   = msg.pose.pose.position.x
            state['robot_y']   = msg.pose.pose.position.y
            q = msg.pose.pose.orientation
            state['robot_yaw'] = math.atan2(2*(q.w*q.z + q.x*q.y), 1 - 2*(q.y*q.y + q.z*q.z))

    def on_lidar(self, msg):
        with state_lock:
            state['lidar_ranges'] = list(msg.ranges)

    def on_imu(self, msg):
        with state_lock:
            state['imu_ax'] = msg.linear_acceleration.x
            state['imu_ay'] = msg.linear_acceleration.y
            state['imu_az'] = msg.linear_acceleration.z
            state['imu_gx'] = msg.angular_velocity.x
            state['imu_gy'] = msg.angular_velocity.y
            state['imu_gz'] = msg.angular_velocity.z


# ── Demo Mode (no ROS2) ───────────────────────────────────────────────────────
def demo_loop():
    """Animate simulated robot when ROS2 is not available."""
    t = 0
    while True:
        socketio.sleep(0.1)
        t += 0.05
        with state_lock:
            if not state['auto_mode'] or state['e_stop']:
                continue
            # Simulate robot moving in a circle
            state['robot_x']   = 1.5 * math.cos(t * 0.2)
            state['robot_y']   = 1.5 * math.sin(t * 0.2)
            state['robot_yaw'] = t * 0.2
            state['battery']   = max(20, 100 - t * 0.01)
            # Simulate LiDAR scan (circle with some variation)
            state['lidar_ranges'] = [
                2.5 + 0.5 * math.sin(math.radians(i) * 3 + t) for i in range(360)
            ]


# ── Entry Point ────────────────────────────────────────────────────────────────
def main(args=None):
    print("=" * 50)
    print("ADVIKA 3.0 — Web Teleop Dashboard")
    print("  URL:  http://localhost:5000")
    print("  ROS2: " + ("connected" if ROS2_AVAILABLE else "demo mode"))
    print("=" * 50)

    if ROS2_AVAILABLE:
        rclpy.init(args=args)
        node = DashboardNode()

    # Start background threads
    socketio.start_background_task(telemetry_loop)
    if not ROS2_AVAILABLE:
        socketio.start_background_task(demo_loop)

    try:
        socketio.run(app, host='0.0.0.0', port=5000,
                     debug=False, log_output=False, use_reloader=False)
    finally:
        if ROS2_AVAILABLE:
            rclpy.shutdown()


if __name__ == '__main__':
    main()