#!/usr/bin/env python3
"""
nav2.launch.py — Nav2 autonomous navigation launch
Phase 4: ros2 launch advika_navigation nav2.launch.py map:=my_first_map.yaml
"""
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    map_file = LaunchConfiguration('map')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    ws_root = os.path.realpath(os.path.expanduser('~/Documents/Robotics/advika_robot_ws'))
    nav2_params = os.path.join(ws_root, 'simulation', 'config', 'nav2_params.yaml')

    nav2_bringup_dir = get_package_share_directory('nav2_bringup')

    return LaunchDescription([
        DeclareLaunchArgument(
            'map',
            default_value=os.path.join(ws_root, 'maps', 'my_first_map.yaml'),
            description='Full path to map yaml file to load'),
        DeclareLaunchArgument(
            'use_sim_time', default_value='true',
            description='Use simulation (Gazebo) clock if true'),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(nav2_bringup_dir, 'launch', 'bringup_launch.py')
            ),
            launch_arguments={
                'map': map_file,
                'use_sim_time': use_sim_time,
                'params_file': nav2_params,
            }.items(),
        ),
    ])
