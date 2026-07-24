#!/usr/bin/env python3
"""
Advika 3.0 -- Simulation Bringup Launch File
ROS2 Jazzy + Gazebo Harmonic launch configuration
Launches: Gazebo, robot state publisher, RViz, navigation stack, and HITL bridge
"""

import os
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess,
    TimerAction, RegisterEventHandler
)
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit, OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    world_file = LaunchConfiguration('world_file', default='advika_playground.world')
    use_rviz = LaunchConfiguration('use_rviz', default='true')
    use_nav2 = LaunchConfiguration('use_nav2', default='false')
    use_hitl = LaunchConfiguration('use_hitl', default='false')
    hitl_port = LaunchConfiguration('hitl_port', default='8080')

    # Paths
    advika_ws = os.path.realpath(os.path.expanduser('~/Documents/Robotics/advika_robot_ws'))
    urdf_path = os.path.join(advika_ws, 'src', 'advika_description', 'urdf', 'advika.urdf')
    world_path = os.path.join(advika_ws, 'simulation', 'gazebo_worlds')
    rviz_config = os.path.join(advika_ws, 'simulation', 'config', 'advika_sim.rviz')

    # ==================== GAZEBO ====================
    gazebo = ExecuteProcess(
        cmd=[
            'gz', 'sim',
            '-r',
            '-v', '4',
            PathJoinSubstitution([world_path, world_file])
        ],
        output='screen',
        cwd=advika_ws
    )

    # ==================== ROBOT STATE PUBLISHER ====================
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'robot_description': open(urdf_path).read(),
            'use_sim_time': use_sim_time
        }]
    )

    # ==================== JOINT STATE PUBLISHER ====================
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # ==================== SPAWN ROBOT IN GAZEBO ====================
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-name', 'advika',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.1',
            '-Y', '0.0'
        ],
        output='screen'
    )

    # ==================== GZ-ROS BRIDGE ====================
    gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/advika/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/advika/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/advika/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/advika/horizon_camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/advika/floor_camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/advika/imu/data@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ],
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # ==================== RVIZ ====================
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen',
        condition=IfCondition(use_rviz),
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # ==================== TELEOP KEYBOARD ====================
    teleop = Node(
        package='teleop_twist_keyboard',
        executable='teleop_twist_keyboard',
        name='teleop_twist_keyboard',
        output='screen',
        prefix='xterm -e',
        remappings=[('/cmd_vel', '/advika/cmd_vel')]
    )

    # ==================== EVENT HANDLERS ====================
    spawn_after_gazebo = RegisterEventHandler(
        OnProcessStart(
            target_action=gazebo,
            on_start=[
                TimerAction(
                    period=3.0,
                    actions=[spawn_robot]
                )
            ]
        )
    )

    bridge_after_spawn = RegisterEventHandler(
        OnProcessStart(
            target_action=spawn_robot,
            on_start=[
                TimerAction(
                    period=2.0,
                    actions=[gz_bridge]
                )
            ]
        )
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true',
                              description='Use simulation time'),
        DeclareLaunchArgument('world_file', default_value='advika_playground.world',
                              description='Gazebo world file'),
        DeclareLaunchArgument('use_rviz', default_value='true',
                              description='Launch RViz'),
        DeclareLaunchArgument('use_nav2', default_value='false',
                              description='Launch Navigation2'),
        DeclareLaunchArgument('use_hitl', default_value='false',
                              description='Launch HITL web interface'),
        DeclareLaunchArgument('hitl_port', default_value='8080',
                              description='HITL web server port'),

        gazebo,
        robot_state_publisher,
        joint_state_publisher,
        spawn_after_gazebo,
        bridge_after_spawn,
        rviz,
        teleop,
    ])
