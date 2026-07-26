from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    dashboard_port = DeclareLaunchArgument(
        'dashboard_port', default_value='5000',
        description='Web dashboard port'
    )

    dashboard_node = Node(
        package='advika_dashboard',
        executable='dashboard',
        name='advika_dashboard',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'dashboard_port': LaunchConfiguration('dashboard_port'),
        }]
    )

    return LaunchDescription([
        dashboard_port,
        dashboard_node,
    ])