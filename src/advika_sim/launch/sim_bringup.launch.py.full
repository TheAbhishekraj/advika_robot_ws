#!/usr/bin/env python3
"""
sim_bringup.launch.py — advika_sim package launch entry point
Delegates to the workspace-level simulation/launch/sim_bringup.launch.py
"""
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    ws_root = os.path.realpath(os.path.expanduser('~/advika_robot_ws'))
    sim_launch = os.path.join(ws_root, 'simulation', 'launch', 'sim_bringup.launch.py')

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(sim_launch)
        ),
    ])
