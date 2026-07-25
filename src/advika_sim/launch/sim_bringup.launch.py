import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, TimerAction, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Package paths
    advika_sim_dir = get_package_share_directory('advika_sim')
    advika_description_dir = get_package_share_directory('advika_description')
    
    # Arguments
    world_arg = DeclareLaunchArgument('world', default_value='living_room.world', description='World file name')
    auto_move_arg = DeclareLaunchArgument('auto_move', default_value='true', description='Move robot automatically in a circle')
    
    world_file = os.path.join(advika_sim_dir, 'worlds', 'living_room.world')
    
    # RViz config
    rviz_config = os.path.join(advika_sim_dir, 'config', 'advika_sim.rviz')
    if not os.path.exists(rviz_config):
        rviz_config = os.path.join(advika_description_dir, 'rviz', 'advika.rviz')
    
    # URDF / Xacro file resolution
    urdf_file = os.path.join(advika_description_dir, 'urdf', 'advika.urdf.xacro')
    if not os.path.exists(urdf_file):
        urdf_file = os.path.join(advika_description_dir, 'urdf', 'advika.urdf')

    # Load robot description
    try:
        import xacro
        doc = xacro.process_file(urdf_file)
        robot_description_content = doc.toxml()
    except Exception:
        with open(urdf_file, 'r') as f:
            robot_description_content = f.read()

    return LaunchDescription([
        world_arg,
        auto_move_arg,
        
        # Gazebo
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
            ]),
            launch_arguments=[('gz_args', f'-r -v 4 {world_file}')],
        ),
        
        # Robot State Publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description_content,
                'use_sim_time': True
            }]
        ),
        
        # Spawn robot after 5 seconds - spawn away from coffee table
        TimerAction(
            period=5.0,
            actions=[
                Node(
                    package='ros_gz_sim',
                    executable='create',
                    arguments=[
                        '-name', 'advika_robot',
                        '-topic', '/robot_description',
                        '-x', '-1.5', '-y', '-1.0', '-z', '0.5',
                    ],
                    output='screen'
                )
            ]
        ),
        
        # ROS-GZ Bridge
        TimerAction(
            period=6.0,
            actions=[
                Node(
                    package='ros_gz_bridge',
                    executable='parameter_bridge',
                    arguments=[
                        '/advika/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
                        '/advika/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
                        '/advika/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
                        '/advika/horizon_camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
                        '/advika/floor_camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
                        '/advika/imu/data@sensor_msgs/msg/Imu@gz.msgs.IMU',
                        '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock',
                    ],
                    output='screen'
                )
            ]
        ),
        
        # Auto-move command
        TimerAction(
            period=10.0,
            actions=[
                ExecuteProcess(
                    condition=IfCondition(LaunchConfiguration('auto_move')),
                    cmd=['ros2', 'topic', 'pub', '/advika/cmd_vel', 'geometry_msgs/msg/Twist', 
                         '"{linear: {x: 0.3}, angular: {z: 0.2}}"', '-r', '10'],
                    shell=True,
                    output='log'
                )
            ]
        ),
        
        # RViz
        TimerAction(
            period=7.0,
            actions=[
                Node(
                    package='rviz2',
                    executable='rviz2',
                    name='rviz2',
                    output='screen',
                    arguments=['-d', rviz_config] if os.path.exists(rviz_config) else []
                )
            ]
        ),
    ])
