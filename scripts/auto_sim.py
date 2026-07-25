#!/usr/bin/env python3
"""
Advika 3.0 - Auto Simulation Launcher
Automatically starts Gazebo 3BHK world, RViz, bridges, and teleop

Usage:
    python3 scripts/auto_sim.py             # Full launch
    python3 scripts/auto_sim.py --no-rviz  # Without RViz
    python3 scripts/auto_sim.py --teleop   # With teleop window
"""
import os
import sys
import time
import subprocess
import argparse
import signal
import shlex

WS = os.path.realpath(os.path.expanduser('~/Documents/Robotics/advika_robot_ws'))
ROS_SETUP = '/opt/ros/jazzy/setup.bash'
WS_SETUP = os.path.join(WS, 'install', 'setup.bash')

# ─── Colours ──────────────────────────────────────────────────────
GREEN = '\033[92m'; YELLOW = '\033[93m'; RED = '\033[91m'; RESET = '\033[0m'

def banner():
    print(f"""
{GREEN}
 █████╗ ██████╗ ██╗   ██╗██╗██╗  ██╗ █████╗     ██████╗     ██████╗
██╔══██╗██╔══██╗██║   ██║██║██║ ██╔╝██╔══██╗    ╚════██╗   ██╔═████╗
███████║██║  ██║██║   ██║██║█████╔╝ ███████║     █████╔╝   ██║██╔██║
██╔══██║██║  ██║╚██╗ ██╔╝██║██╔═██╗ ██╔══██║     ╚═══██╗   ████╔╝██║
██║  ██║██████╔╝ ╚████╔╝ ██║██║  ██╗██║  ██║    ██████╔╝██╗╚██████╔╝
╚═╝  ╚═╝╚═════╝   ╚═══╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚═╝ ╚═════╝
    3BHK Auto-Simulation Launcher
{RESET}""")

def check_env():
    print(f"{YELLOW}[CHECK]{RESET} Verifying workspace...")
    if not os.path.exists(WS_SETUP):
        print(f"{RED}[ERROR]{RESET} Workspace not built! Run: colcon build --symlink-install")
        sys.exit(1)
    world = os.path.join(WS, 'src', 'advika_sim', 'worlds', '3bhk_house.world')
    if not os.path.exists(world):
        print(f"{RED}[ERROR]{RESET} 3BHK world not found at {world}")
        sys.exit(1)
    print(f"{GREEN}[OK]{RESET} Workspace ready.")

def run(cmd, wait=False, delay=0):
    source_cmd = f'source {ROS_SETUP} && source {WS_SETUP} && {cmd}'
    proc = subprocess.Popen(['bash', '-c', source_cmd], 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if delay:
        time.sleep(delay)
    if wait:
        proc.wait()
    return proc

def main():
    parser = argparse.ArgumentParser(description='Advika 3.0 Auto Launcher')
    parser.add_argument('--no-rviz', action='store_true', help='Skip RViz')
    parser.add_argument('--teleop', action='store_true', help='Launch teleop (separate terminal)')
    args = parser.parse_args()

    banner()
    check_env()

    print(f"\n{YELLOW}[1/4]{RESET} Launching 3BHK Gazebo world...")
    use_rviz = 'false' if args.no_rviz else 'true'
    launch_proc = run(
        f'ros2 launch advika_sim sim_bringup.launch.py use_rviz:={use_rviz}',
        wait=False
    )

    print(f"{YELLOW}[2/4]{RESET} Waiting 8s for Gazebo to fully load (robot spawns in 5s)...")
    time.sleep(8)

    print(f"{YELLOW}[3/4]{RESET} Verifying topics are alive...")
    result = subprocess.run(
        ['bash', '-c', f'source {ROS_SETUP} && source {WS_SETUP} && ros2 topic list'],
        capture_output=True, text=True
    )
    topics = result.stdout.strip().split('\n')
    expected = ['/advika/scan', '/advika/cmd_vel', '/advika/odom']
    for t in expected:
        if t in topics:
            print(f"  {GREEN}✓{RESET} {t}")
        else:
            print(f"  {RED}✗ MISSING: {t}{RESET}")

    if args.teleop:
        print(f"\n{YELLOW}[4/4]{RESET} Launching teleop...")
        teleop_cmd = (f'source {ROS_SETUP} && source {WS_SETUP} && '
                      f'ros2 run teleop_twist_keyboard teleop_twist_keyboard '
                      f'--ros-args -r cmd_vel:=/advika/cmd_vel')
        subprocess.Popen(['bash', '-c', teleop_cmd])
        print(f"{GREEN}[DONE]{RESET} Teleop active — use WASD keys to drive!")
    else:
        print(f"\n{GREEN}[4/4]{RESET} Teleop (run in new terminal if needed):")
        print(f"  source install/setup.bash")
        print(f"  ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r cmd_vel:=/advika/cmd_vel")

    print(f"\n{GREEN}╔══════════════════════════════════════════════╗")
    print(f"║   Advika 3.0 is LIVE in the 3BHK world!     ║")
    print(f"║   Press Ctrl+C to stop all processes.        ║")
    print(f"╚══════════════════════════════════════════════╝{RESET}")

    def shutdown(sig, frame):
        print(f"\n{YELLOW}[STOP]{RESET} Shutting down simulation...")
        launch_proc.terminate()
        launch_proc.wait()
        print(f"{GREEN}[DONE]{RESET} Simulation stopped cleanly.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    launch_proc.wait()

if __name__ == '__main__':
    main()
