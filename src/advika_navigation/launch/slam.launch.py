#!/usr/bin/env python3
"""
slam.launch.py — SLAM Toolbox mapping launch
Phase 3: ros2 launch advika_navigation slam.launch.py
"""
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    ws_root = os.path.realpath(os.path.expanduser('~/Documents/Robotics/advika_robot_ws'))
    slam_params = os.path.join(ws_root, 'simulation', 'config', 'slam_params.yaml')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time', default_value='true',
            description='Use simulation (Gazebo) clock if true'),

        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                slam_params,
                {'use_sim_time': use_sim_time},
            ],
        ),
    ])
