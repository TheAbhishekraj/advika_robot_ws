import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    slam_params  = os.path.join(
        get_package_share_directory('advika_description'),
        'config', 'slam_params.yaml')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),

        # SLAM Toolbox
        Node(package='slam_toolbox',
             executable='async_slam_toolbox_node',
             name='slam_toolbox',
             output='screen',
             parameters=[slam_params, {'use_sim_time': use_sim_time}]),

        # RViz2 for map visualization
        Node(package='rviz2',
             executable='rviz2',
             name='rviz2',
             output='screen'),
    ])
