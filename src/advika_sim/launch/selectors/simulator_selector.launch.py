import os
import sys
import yaml
from launch import LaunchDescription
from launch.actions import ExecuteProcess, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

CONFIG_FILE = os.path.expanduser("~/.advika_config/selector_config.yaml")

def get_user_selection(prompt, options):
    """Interactive user selection with arrow keys simulation"""
    print("\n" + "="*60)
    print(prompt)
    print("="*60)
    for i, (key, value) in enumerate(options.items(), 1):
        print(f"  [{i}] {value}")
    print("  [0] Exit")
    print("-"*60)
    
    while True:
        try:
            choice = input("Enter your choice (number): ").strip()
            if choice == "0":
                print("Exiting...")
                sys.exit(0)
            choice_int = int(choice)
            if 1 <= choice_int <= len(options):
                return list(options.keys())[choice_int-1]
            else:
                print(f"Invalid choice. Please enter 1-{len(options)} or 0 to exit.")
        except ValueError:
            print("Please enter a valid number.")

def load_config():
    """Load saved configuration"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return yaml.safe_load(f)
    return {}

def save_config(config):
    """Save configuration"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f)

def launch_setup(context, *args, **kwargs):
    """Main launch function"""
    
    # World options
    world_options = {
        "3bhk_house": "3BHK House (Indoor Home)",
        "warehouse": "Warehouse (Large Open Space)",
        "office": "Office (Cubicle Environment)",
        "living_room": "Living Room (Pre-built)",
        "advika_playground": "Playground (Test Arena)"
    }
    
    # Model options
    model_options = {
        "advika": "Advika 3.0 (Standard)",
        "advika_heavy": "Advika Heavy (30% more payload)",
        "advika_light": "Advika Light (No floor camera)",
        "advika_seds": "Advika SEDS (Omnidirectional)"
    }
    
    # Load saved config
    config = load_config()
    
    # Get user selections
    selected_world = get_user_selection("🌍 SELECT WORLD:", world_options)
    selected_model = get_user_selection("🤖 SELECT ROBOT MODEL:", model_options)
    
    # Save selection
    config['last_world'] = selected_world
    config['last_model'] = selected_model
    save_config(config)
    
    # Build paths
    world_path = os.path.join(
        get_package_share_directory('advika_sim'),
        'worlds', selected_world, f"{selected_world}.world"
    )
    
    print("\n" + "="*60)
    print(f"🚀 LAUNCHING SIMULATION")
    print("="*60)
    print(f"World: {world_options[selected_world]}")
    print(f"Model: {model_options[selected_model]}")
    print(f"World Path: {world_path}")
    print("="*60 + "\n")
    
    # Launch Gazebo
    gz_cmd = [
        'gz', 'sim', '-r', '-v', '4', world_path
    ]
    
    rsp_cmd = None
    spawn_cmd = None

    if selected_model == "advika_seds":
        model_path = os.path.join(get_package_share_directory('advika_sim'), 'models', 'NUS_SEDS_OGV', 'model.sdf')
        print(f"SDF Path: {model_path}")
        spawn_cmd = [
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-name', 'advika_robot',
            '-file', model_path,
            '-x', '0', '-y', '0', '-z', '0.5'
        ]
    else:
        urdf_path = os.path.join(
            get_package_share_directory('advika_description'),
            'urdf', 'alternative' if selected_model != "advika" else '',
            f"{selected_model}.urdf"
        )
        print(f"URDF Path: {urdf_path}")
        rsp_cmd = [
            'ros2', 'run', 'robot_state_publisher', 'robot_state_publisher',
            '--ros-args', '-p', f'robot_description:={open(urdf_path).read()}'
        ]
        spawn_cmd = [
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-name', 'advika_robot',
            '-topic', '/robot_description',
            '-x', '0', '-y', '0', '-z', '0.5'
        ]
    
    # Launch ROS-GZ Bridge
    bridge_cmd = [
        'ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
        '/advika/cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist',
        '/advika/odom@nav_msgs/msg/Odometry@gz.msgs.Odometry',
        '/advika/scan@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
        '/advika/horizon_camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
        '/advika/floor_camera/image_raw@sensor_msgs/msg/Image@gz.msgs.Image',
        '/advika/imu/data@sensor_msgs/msg/Imu@gz.msgs.IMU',
        '/clock@rosgraph_msgs/msg/Clock@gz.msgs.Clock'
    ]
    
    # Launch RViz
    rviz_config = os.path.join(
        get_package_share_directory('advika_sim'),
        'config', 'advika_sim.rviz'
    )
    rviz_cmd = ['rviz2', '-d', rviz_config]
    
    cmds = [ExecuteProcess(cmd=gz_cmd, output='screen', name='gz_server')]
    if rsp_cmd:
        cmds.append(ExecuteProcess(cmd=rsp_cmd, output='screen', name='robot_state_publisher'))
    cmds.append(ExecuteProcess(cmd=spawn_cmd, output='screen', name='spawn_robot'))
    cmds.append(ExecuteProcess(cmd=bridge_cmd, output='screen', name='ros_gz_bridge'))
    cmds.append(ExecuteProcess(cmd=rviz_cmd, output='screen', name='rviz2'))

    return cmds

def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function=launch_setup)
    ])
