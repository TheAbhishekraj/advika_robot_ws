#!/usr/bin/env python3
"""
Advika 3.0 -- Phase 2: Simulation Teleop Only
Minimal launch: Gazebo + Robot + Teleop + Bridge + RViz
"""

import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, TimerAction, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    use_rviz = LaunchConfiguration('use_rviz', default='true')

    # FIXED PATHS
    advika_ws = os.path.realpath(os.path.expanduser('~/Documents/Robotics/advika_robot_ws'))
    urdf_path = os.path.join(advika_ws, 'src', 'advika_description', 'urdf', 'advika.urdf')
    world_path = os.path.join(advika_ws, 'simulation', 'gazebo_worlds')
    rviz_config = os.path.join(advika_ws, 'simulation', 'config', 'advika_sim.rviz')

    # Verify URDF exists
    if not os.path.exists(urdf_path):
        raise FileNotFoundError(f"URDF not found at: {urdf_path}")

    # Read URDF
    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    # Gazebo
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-v', '4', os.path.join(world_path, 'advika_playground.world')],
        output='screen',
        cwd=advika_ws
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': use_sim_time
        }]
    )

    # Joint State Publisher
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # Spawn Robot
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'advika',
            '-topic', 'robot_description',
            '-x', '0.0', '-y', '0.0', '-z', '0.1', '-Y', '0.0'
        ],
        output='screen'
    )

    # GZ-ROS Bridge
    gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/advika/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
            '/advika/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
            '/advika/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
            '/advika/horizon_camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            '/advika/horizon_camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
            '/advika/floor_camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
            '/advika/floor_camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo',
            '/advika/imu/data@sensor_msgs/msg/Imu@gz.msgs.IMU',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # RViz
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen',
        condition=IfCondition(use_rviz),
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # Teleop
    teleop = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_twist_keyboard',
        output='screen',
        prefix='xterm -e',
        remappings=[('/cmd_vel', '/advika/cmd_vel')]
    )

    # Event: spawn robot 3 seconds after Gazebo starts
    spawn_after_gazebo = RegisterEventHandler(
        OnProcessStart(
            target_action=gazebo,
            on_start=[TimerAction(period=3.0, actions=[spawn_robot])]
        )
    )

    # Event: start bridge 2 seconds after spawn
    bridge_after_spawn = RegisterEventHandler(
        OnProcessStart(
            target_action=spawn_robot,
            on_start=[TimerAction(period=2.0, actions=[gz_bridge])]
        )
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('use_rviz', default_value='true'),
        gazebo,
        robot_state_publisher,
        joint_state_publisher,
        spawn_after_gazebo,
        bridge_after_spawn,
        rviz,
        teleop,
    ])
