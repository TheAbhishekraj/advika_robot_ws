#!/usr/bin/env python3
"""
Advika 3.0 — Simulation Phase Tester
Tests all 6 simulation phases (A-F) and saves structured output.

Usage:
    python3 scripts/simulation_test.py               # Run all checks
    python3 scripts/simulation_test.py --phase A     # Run single phase
    python3 scripts/simulation_test.py --save        # Save report to docs/reports/
"""
import os
import sys
import json
import time
import argparse
import subprocess
from datetime import datetime

WS = os.path.realpath(os.path.expanduser('~/Documents/Robotics/advika_robot_ws'))
ROS_SETUP = '/opt/ros/jazzy/setup.bash'
WS_SETUP  = os.path.join(WS, 'install', 'setup.bash')
REPORT_DIR = os.path.join(WS, 'docs', 'reports')

GREEN = '\033[92m'; YELLOW = '\033[93m'; RED = '\033[91m'
CYAN  = '\033[96m'; BOLD   = '\033[1m';  RESET = '\033[0m'

results = []

# ─── Helpers ──────────────────────────────────────────────────────
def run(cmd):
    r = subprocess.run(
        ['bash', '-c', f'source {ROS_SETUP} 2>/dev/null; source {WS_SETUP} 2>/dev/null; {cmd}'],
        capture_output=True, text=True, timeout=15
    )
    return r.stdout.strip(), r.stderr.strip(), r.returncode

def check(phase, name, fn):
    """Run one check and record result."""
    try:
        ok, detail = fn()
    except Exception as e:
        ok, detail = False, str(e)
    status = f"{GREEN}PASS{RESET}" if ok else f"{RED}FAIL{RESET}"
    print(f"  [{status}] {name}")
    if detail:
        print(f"         └─ {detail}")
    results.append({
        "phase": phase, "name": name,
        "passed": ok, "detail": detail,
        "timestamp": datetime.now().isoformat()
    })
    return ok

def section(title):
    print(f"\n{BOLD}{CYAN}{'─'*55}")
    print(f"  {title}")
    print(f"{'─'*55}{RESET}")

# ─── Phase A: Robot Spawning ──────────────────────────────────────
def phase_a():
    section("Phase A: Robot Spawning")

    def urdf_exists():
        p = os.path.join(WS, 'src', 'advika_description', 'urdf', 'advika.urdf')
        return os.path.exists(p), p

    def spawn_in_launch():
        out, _, _ = run(f"grep -r 'spawn\\|create' {WS}/src/advika_sim/launch/")
        return bool(out), out[:120] if out else "spawn node not found"

    def timer_delay():
        out, _, _ = run(f"grep 'period' {WS}/src/advika_sim/launch/sim_bringup.launch.py")
        return "5.0" in out, out.strip()

    def ws_built():
        return os.path.exists(WS_SETUP), WS_SETUP

    check("A", "URDF file exists",         urdf_exists)
    check("A", "spawn/create node in launch", spawn_in_launch)
    check("A", "5s TimerAction delay",     timer_delay)
    check("A", "Workspace built",          ws_built)

# ─── Phase B: 3BHK World ─────────────────────────────────────────
def phase_b():
    section("Phase B: 3BHK Indoor Environment")

    def world_exists():
        p = os.path.join(WS, 'src', 'advika_sim', 'worlds', '3bhk_house.world')
        return os.path.exists(p), p

    def walls_in_world():
        out, _, _ = run(f"grep -c 'wall_' {WS}/src/advika_sim/worlds/3bhk_house.world")
        count = int(out) if out.isdigit() else 0
        return count >= 4, f"{count} wall models found"

    def launch_uses_3bhk():
        out, _, _ = run(f"grep '3bhk' {WS}/src/advika_sim/launch/sim_bringup.launch.py")
        return bool(out), out.strip()[:100]

    check("B", "3bhk_house.world exists",  world_exists)
    check("B", "≥4 wall models in world",  walls_in_world)
    check("B", "Launch uses 3BHK world",   launch_uses_3bhk)

# ─── Phase C: Parameter Tuning ───────────────────────────────────
def phase_c():
    section("Phase C: Parameter Tuning")
    urdf = os.path.join(WS, 'src', 'advika_description', 'urdf', 'advika.urdf')
    nav2 = os.path.join(WS, 'simulation', 'config', 'nav2_params.yaml')

    def max_vel():
        out, _, _ = run(f"grep 'max_linear_velocity' {urdf}")
        return '0.5' in out, out.strip()

    def lidar_range():
        out, _, _ = run(f"grep 'max.*5.0\\|5.0.*max' {urdf}")
        return bool(out), out.strip()[:80] or "5.0m not found"

    def camera_res():
        out, _, _ = run(f"grep '<width>320' {urdf}")
        return bool(out), "320px camera" if out else "640px camera still set"

    def nav2_tuned():
        out, _, _ = run(f"grep 'max_iterations' {nav2}")
        return bool(out), out.strip()

    def friction_tuned():
        out, _, _ = run(f"grep 'mu1>0.8' {urdf}")
        return bool(out), "mu=0.8 tile friction" if out else "friction not tuned"

    check("C", "max_linear_velocity = 0.5", max_vel)
    check("C", "LiDAR range = 5.0m",        lidar_range)
    check("C", "Camera 320×240",            camera_res)
    check("C", "Nav2 max_iterations set",   nav2_tuned)
    check("C", "Wheel friction = 0.8",      friction_tuned)

# ─── Phase D: ROS2 Topics ────────────────────────────────────────
def phase_d():
    section("Phase D: ROS2 Topic Verification (sim must be running)")

    required_topics = ['/advika/scan', '/advika/cmd_vel', '/advika/odom',
                       '/advika/imu/data', '/robot_description']

    try:
        out, _, _ = run("ros2 topic list")
        live_topics = out.split('\n') if out else []
    except Exception:
        live_topics = []

    for t in required_topics:
        check("D", f"Topic: {t}", lambda tp=t: (tp in live_topics, "active" if tp in live_topics else "NOT found — is sim running?"))

# ─── Phase E: SLAM Map Files ─────────────────────────────────────
def phase_e():
    section("Phase E: SLAM Map Files")

    candidates = [
        os.path.join(WS, 'maps', 'advika_3bhk_map.yaml'),
        os.path.expanduser('~/advika_3bhk_map.yaml'),
        os.path.join(WS, 'maps', 'real_room.yaml'),
    ]

    def map_yaml():
        for p in candidates:
            if os.path.exists(p):
                return True, p
        return False, "No map .yaml found — run: ros2 run nav2_map_server map_saver_cli -f ~/advika_3bhk_map"

    def map_pgm():
        for p in [c.replace('.yaml', '.pgm') for c in candidates]:
            if os.path.exists(p):
                size = os.path.getsize(p)
                return True, f"{p} ({size} bytes)"
        return False, "No .pgm found"

    check("E", "Map YAML exists",   map_yaml)
    check("E", "Map PGM exists",    map_pgm)
    check("E", "slam.launch.py exists", lambda: (
        os.path.exists(os.path.join(WS, 'src', 'advika_navigation', 'launch', 'slam.launch.py')),
        "slam.launch.py found"
    ))

# ─── Phase F: Nav2 Launch ────────────────────────────────────────
def phase_f():
    section("Phase F: Nav2 Configuration")

    def nav2_launch():
        p = os.path.join(WS, 'src', 'advika_navigation', 'launch', 'nav2.launch.py')
        return os.path.exists(p), p

    def params_file():
        p = os.path.join(WS, 'simulation', 'config', 'nav2_params.yaml')
        return os.path.exists(p), p

    def default_map():
        out, _, _ = run(f"grep 'map\\|3bhk' {WS}/src/advika_navigation/launch/nav2.launch.py")
        return bool(out), out.strip()[:100]

    check("F", "nav2.launch.py exists",     nav2_launch)
    check("F", "nav2_params.yaml exists",   params_file)
    check("F", "Map configured in launch",  default_map)

# ─── Report Save ─────────────────────────────────────────────────
def save_report(args):
    os.makedirs(REPORT_DIR, exist_ok=True)
    passed = sum(1 for r in results if r['passed'])
    failed = len(results) - passed

    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    json_path = os.path.join(REPORT_DIR, f'simulation_test_{ts}.json')
    md_path   = os.path.join(REPORT_DIR, f'simulation_test_{ts}.md')

    with open(json_path, 'w') as f:
        json.dump({"summary": {"total": len(results), "passed": passed, "failed": failed},
                   "results": results}, f, indent=2)

    lines = [f"# Advika 3.0 Simulation Test Report\n",
             f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n",
             f"**Result:** {passed}/{len(results)} passed\n\n",
             "| Phase | Test | Result | Detail |\n",
             "|-------|------|--------|--------|\n"]
    for r in results:
        icon = "✅" if r['passed'] else "❌"
        lines.append(f"| {r['phase']} | {r['name']} | {icon} | {r['detail'][:80]} |\n")

    with open(md_path, 'w') as f:
        f.writelines(lines)

    print(f"\n{GREEN}Reports saved:{RESET}")
    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_path}")
    return json_path, md_path

# ─── Main ─────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='Advika 3.0 Simulation Tester')
    parser.add_argument('--phase', choices=['A','B','C','D','E','F'], help='Run single phase')
    parser.add_argument('--save', action='store_true', default=True, help='Save report (default: True)')
    args = parser.parse_args()

    print(f"\n{BOLD}{CYAN}Advika 3.0 Simulation Test Suite{RESET}")
    print(f"Workspace: {WS}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    phase_map = {'A': phase_a, 'B': phase_b, 'C': phase_c,
                 'D': phase_d, 'E': phase_e, 'F': phase_f}

    if args.phase:
        phase_map[args.phase]()
    else:
        for fn in phase_map.values():
            fn()

    passed = sum(1 for r in results if r['passed'])
    total  = len(results)

    print(f"\n{BOLD}{'═'*55}")
    colour = GREEN if passed == total else (YELLOW if passed > total//2 else RED)
    print(f"  TOTAL: {colour}{passed}/{total} PASSED{RESET}")
    print(f"{'═'*55}{RESET}")

    if args.save:
        save_report(args)

    sys.exit(0 if passed == total else 1)

if __name__ == '__main__':
    main()
