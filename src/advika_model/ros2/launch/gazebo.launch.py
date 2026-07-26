import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, ExecuteProcess,
                             IncludeLaunchDescription, RegisterEventHandler)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
import xacro

def generate_launch_description():
    pkg      = get_package_share_directory('advika_description')
    gz_ros   = get_package_share_directory('gazebo_ros')
    urdf_file = os.path.join(pkg, 'urdf', 'advika_3_0.urdf')
    world_file = os.path.join(pkg, 'worlds', 'advika_world.world')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose      = LaunchConfiguration('x_pose',      default='0.0')
    y_pose      = LaunchConfiguration('y_pose',      default='0.0')

    robot_desc = open(urdf_file).read()

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('x_pose',      default_value='0.0'),
        DeclareLaunchArgument('y_pose',      default_value='0.0'),

        # Launch Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gz_ros, 'launch', 'gazebo.launch.py')),
            launch_arguments={'world': world_file}.items()),

        # Robot State Publisher
        Node(package='robot_state_publisher',
             executable='robot_state_publisher',
             output='screen',
             parameters=[{'use_sim_time': use_sim_time,
                          'robot_description': robot_desc}]),

        # Spawn robot in Gazebo
        Node(package='gazebo_ros',
             executable='spawn_entity.py',
             arguments=['--topic', 'robot_description',
                         '--entity', 'advika_3_0',
                         '-x', x_pose, '-y', y_pose, '-z', '0.05'],
             output='screen'),

        # Teleop keyboard
        Node(package='teleop_twist_keyboard',
             executable='teleop_twist_keyboard',
             name='teleop',
             output='screen',
             prefix='xterm -e'),
    ])
