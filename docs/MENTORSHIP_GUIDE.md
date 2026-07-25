# ADVIKA 3.0 MENTORSHIP PROGRAM
## Project Completion Guide: Simulation → Design → Hardware

**Mentor Mode:** Active
**Current Phase:** SIMULATION & DESIGN
**Target:** Complete all simulation and CAD design work BEFORE touching hardware

---

## 🗺️ YOUR LEARNING PATH

```
Phase 1: SIMULATION MASTER      →  Phase 2: DESIGN FLUENCY    →  Phase 3: HARDWARE
[ Weeks 1-4 ]                  [ Weeks 5-8 ]                  [ Weeks 9+ ]
                               
• Get Gazebo running            • Design first component      • Order parts
• Validate URDF                 • Export STL correctly         • Assemble chassis
• Run 3BHK world                • Update URDF with meshes      • Flash ESP32
• Test Nav2                    • Design furniture set         • Integration testing
• Complete HITL dashboard       • Prepare manufacturing       • Field testing
```

---

## PHASE 1: SIMULATION MASTER (Weeks 1-4)

### Week 1: Get Everything Running

**Goal:** Launch Gazebo and see the robot move

#### Task 1.1: Environment Setup (Day 1-2)
```bash
# On your Linux VM or dual-boot (NOT Windows):
# 1. Install Ubuntu 24.04 LTS
# 2. Install ROS2 Jazzy: https://docs.ros.org/en/jazzy/Installation.html
# 3. Clone repository
cd ~
git clone https://github.com/TheAbhishekraj/advika_robot_ws.git
cd advika_robot_ws
source /opt/ros/jazzy/setup.bash

# Build the workspace
colcon build --symlink-install
source install/setup.bash
```

#### Task 1.2: Launch Playground World (Day 3-4)
```bash
# Terminal 1: Launch Gazebo
ros2 launch advika_sim sim_bringup.launch.py

# Expected: Gazebo window opens with Advika robot in arena
# If error: Check Gazebo Harmonic installation
```

#### Task 1.3: Drive the Robot (Day 5-7)
```bash
# Terminal 2: Send drive commands
ros2 topic pub /advika/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}" -1

# Robot should move forward
# Try: angular.z: 0.5 for rotation
```

**Deliverable:** Robot moves in Gazebo. Screenshot showing robot position changed.

---

### Week 2: URDF Deep Dive

**Goal:** Understand every part of the robot model

#### Task 2.1: Inspect URDF (Day 1-3)
```bash
# Visualize robot structure
ros2 run urdf_omy inspect src/advika_description/urdf/advika.urdf

# Or use launch file with robot_state_publisher
ros2 launch robot_state_publisher robot_state_publisher.launch.py \
  xacro: src/advika_description/urdf/advika.urdf
```

#### Task 2.2: Modify a Primitive (Day 4-5)
**Exercise:** Change the base_link color from blue to green
```xml
<!-- In advika.urdf, find and change: -->
<material name="blue">
  <color rgba="0.1 0.3 0.8 1.0"/>  <!-- Change to -->
  <color rgba="0.1 0.8 0.3 1.0"/>  <!-- Green -->
```

**Rebuild and verify** in Gazebo.

#### Task 2.3: Add a New Link (Day 6-7)
**Exercise:** Add a "front_bumper" link to the URDF
```xml
<!-- Add after display_link definition -->
<link name="front_bumper">
  <visual>
    <origin xyz="0.16 0 0.05" rpy="0 0 0"/>
    <geometry>
      <box size="0.02 0.20 0.08"/>
    </geometry>
    <material name="red"/>
  </visual>
</link>
```

**Deliverable:** URDF with 13 links (original 12 + 1 bumper). Screenshot.

---

### Week 3: 3BHK World Mastery

**Goal:** Navigate the full house in simulation

#### Task 3.1: Launch 3BHK World (Day 1-2)
```bash
# Modify sim_bringup.launch.py to use 3BHK world
# OR copy living_room.world and modify for 3BHK

# Let's use the existing 3BHK world
ros2 launch advika_sim sim_bringup.launch.py world:=3bhk_house
```

#### Task 3.2: Map the Environment (Day 3-5)
```bash
# Terminal 1: Launch Nav2 with SLAM
ros2 launch advika_sim sim_bringup.launch.py

# Terminal 2: Start SLAM Toolbox
ros2 run slam_toolbox async_slam_toolbox_node \
  --ros-args -p slam_params_file:=config/slam_params.yaml

# Terminal 3: Teleoperate and map
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

**Drive robot around entire house** to create map. Save map:
```bash
ros2 run nav2_map_server map_saver_cli -f ~/3bhk_map
```

#### Task 3.3: Autonomous Navigation (Day 6-7)
```bash
# Navigate to waypoints using Nav2
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: map}, pose: {position: {x: -1.5, y: 1.5}}}}"
```

**Deliverable:** 3BHK map saved. Robot navigates to 3 different waypoints autonomously.

---

### Week 4: HITL Dashboard

**Goal:** Get the human-in-the-loop web interface working

#### Task 4.1: Launch HITL Bridge (Day 1-3)
```bash
# Terminal 1: Launch simulation
ros2 launch advika_sim sim_bringup.launch.py

# Terminal 2: Start HITL bridge
ros2 run advika_sim hitl_bridge

# Open browser: http://localhost:8080
```

#### Task 4.2: Test Manual Control (Day 4-5)
- Use dashboard to drive robot manually
- Observe LiDAR visualization
- Check camera feeds

#### Task 4.3: Test Supervised Mode (Day 6-7)
**Exercise:** In supervised mode, approve and reject robot actions

**Deliverable:** Working HITL dashboard. Screenshot with all panels visible.

---

## PHASE 2: DESIGN FLUENCY (Weeks 5-8)

### Week 5: Fusion 360 Basics

**Goal:** Learn CAD fundamentals with a simple part

#### Task 5.1: Install & Setup (Day 1-2)
1. Download Fusion 360 (autodesk.com/fusion-360)
2. Create personal account (free for makers)
3. Create project: "Advika_Learning"

#### Task 5.2: First Sketch (Day 3-4)
**Exercise:** Draw a 50mm × 50mm square
- New sketch on XY plane
- Create rectangle tool
- Dimension all sides
- Constrain with equal lengths

#### Task 5.3: First Extrusion (Day 5-7)
**Exercise:** Extrude square to 10mm height
- Select rectangle sketch
- Extrude command (E key)
- Distance: 10mm
- Create first 3D print!

**Deliverable:** Print the 50×50×10mm block. Photo of printed part.

---

### Week 6: Wheel Hub Design

**Goal:** Design the first Advika component

#### Task 6.1: Analyze Requirements (Day 1)
From your audit report, wheel hub specs:
- Outer diameter: 65mm
- Bore diameter: 6mm (D-shaft)
- Hub height: 12mm
- 4× M3 screw holes on 50mm PCD

#### Task 6.2: Create Sketch (Day 2-3)
1. New sketch on XZ plane
2. Draw 65mm circle (outer boundary)
3. Draw 6mm circle (center bore)
4. Draw 4× M3 holes on 50mm diameter PCD
5. Add dimension annotations

#### Task 6.3: Extrude & Finish (Day 4-5)
1. Extrude outer circle 12mm
2. Extrude cut center bore
3. Extrude cut 4× M3 holes
4. Add chamfer to edges (0.5mm)

#### Task 6.4: Export & Print (Day 6-7)
```bash
# Export STL from Fusion 360
File → Export → STL → Binary, mm, High Quality

# Save to: src/advika_cad/meshes/Wheel_Hub_Left_v1.stl
# Print with PETG, 30% infill, 4 perimeters
```

**Deliverable:** Printed wheel hub. Photo showing it fitted to a motor shaft.

---

### Week 7: Chassis Base Design

**Goal:** Design the main structural component

#### Task 7.1: Requirements Analysis (Day 1)
From audit report:
- Dimensions: 300mm × 240mm × 5mm
- Motor mount holes (4× M3)
- Raspberry Pi 5 mounting (4× M2.5)
- ESP32 mounting (4× M2)
- Cable channels (6mm wide)
- Battery tray slot (140mm × 80mm)

#### Task 7.2: Create Base Sketch (Day 2-3)
1. Draw 300×240mm rectangle
2. Mark motor positions (±50mm from center, 20mm apart)
3. Mark Pi positions (60×50mm rectangle centered)
4. Mark ESP32 positions (40×30mm rectangle)
5. Draw battery tray slot (140×80mm)
6. Draw cable channels

#### Task 7.3: Add Mounting Holes (Day 4-5)
1. 4× motor mount holes: 3.2mm diameter (for M3 tap)
2. 4× Pi mounting holes: 2.5mm
3. 4× ESP32 holes: 2.0mm
4. All holes through entire 5mm base

#### Task 7.4: Export & Verify (Day 6-7)
```bash
# Export STL: Chassis_Base_v3.stl
# Print test: Use draft mode first to verify dimensions
# Check with caliper: 300mm, 240mm, 5mm
```

**Deliverable:** Printed chassis base. Photo showing all mounting holes aligned.

---

### Week 8: Complete Component Set

**Goal:** Design remaining robot components

#### Task 8.1: LiDAR Tower (Day 1-2)
- Height: 150mm
- Base: 70mm diameter
- Top: 60mm diameter (tapered)
- Cable channel internal

#### Task 8.2: Top Dome (Day 3-4)
- Diameter: 230mm
- Height: 80mm
- SSD1306 cutout: 60mm × 30mm
- Translucent PETG

#### Task 8.3: Finalize & Organize (Day 5-7)
```bash
# Directory structure should be:
src/advika_cad/meshes/
├── Chassis_Base_v3.stl
├── Wheel_Hub_Left_v1.stl
├── Wheel_Hub_Right_v1.stl
├── LiDAR_Tower_v2.stl
├── Top_Dome_v1.stl
└── ...

src/advika_cad/step/
├── Chassis_Assembly_v3.step
└── Full_Robot_v1.step
```

**Deliverable:** All STL files exported. README updated with BOM.

---

## PHASE 3: HARDWARE PREPARATION (Week 9+)

### Week 9: Manufacturing Prep

**Goal:** Prepare for 3D printing and parts ordering

#### Task 9.1: Create Bill of Materials (Day 1-2)
From your audit report, create `docs/BOM.md`:

| Part | Quantity | Material | Print Time | Status |
|------|----------|----------|------------|--------|
| Chassis Base | 1 | PETG | 2.5h | Ready |
| Wheel Hub | 2 | PETG | 45m each | Ready |
| ... | | | | |

#### Task 9.2: Find Print Service (Day 3-4)
Options:
- Local library maker space
- JLCPCB 3D printing
- Treatstock service
- Buy own Ender 3 V3 KE (~$200)

#### Task 9.3: Order Hardware Parts (Day 5-7)
Based on README hardware list:
- Raspberry Pi 5 (8GB)
- ESP32-S3 DevKit
- JGA25-370 Motors ×2
- LD06 LiDAR
- VL53L5CX ToF
- Pi Cameras ×2
- 3S LiPo Battery

**Deliverable:** BOM with costs. Ordered parts list.

---

## 📊 WEEKLY CHECKLIST

```
Before Week 2:
[ ] Gazebo running with Advika robot
[ ] Robot responds to cmd_vel
[ ] Screenshot: Robot in playground

Before Week 3:
[ ] Understand URDF structure
[ ] Modified base_link color successfully
[ ] Added front_bumper link

Before Week 4:
[ ] 3BHK world launches
[ ] Mapped at least 50% of house
[ ] Robot navigates autonomously

Before Week 5:
[ ] HITL dashboard working
[ ] Manual control functional
[ ] Screenshot: Dashboard with all panels

Before Week 6:
[ ] Fusion 360 installed
[ ] First simple part printed
[ ] Photo of 50×50×10mm block

Before Week 7:
[ ] Wheel hub designed and printed
[ ] Photo of hub on motor shaft

Before Week 8:
[ ] Chassis base designed and printed
[ ] Dimensions verified with caliper

Before Week 9:
[ ] All robot STL files exported
[ ] STEP files for assembly
[ ] Updated repository structure
```

---

## 🎯 GRADUATION CRITERIA

You are ready for **HARDWARE PHASE** when:

1. ✅ Simulation runs at 60+ FPS in Gazebo
2. ✅ Robot navigates 3BHK autonomously (no collisions)
3. ✅ HITL dashboard controls robot successfully
4. ✅ All robot components designed in Fusion 360
5. ✅ STL files printed and verified dimensionally
6. ✅ BOM with costs completed
7. ✅ Hardware parts list finalized

---

## 🚨 COMMON MENTOR ADVICE

### "My Gazebo is slow on Windows"
> Windows is NOT supported for Gazebo. Use Ubuntu 24.04 VM (VirtualBox) or dual-boot. Minimum 8GB RAM, 4 cores for acceptable performance.

### "My 3D prints are warping"
> PETG needs: 250°C nozzle, 80°C bed, enclosure to prevent drafts, slow cooling. Start with small parts first.

### "URDF mesh not showing in Gazebo"
> Check: (1) File exists in `meshes/` folder, (2) Path uses `package://advika_cad/meshes/`, (3) Built with `colcon build`

### "Fusion 360 is confusing"
> Start with tutorials on YouTube: "Fusion 360 for absolute beginners". Practice with simple boxes before complex parts.

### "Robot not moving in Gazebo"
> Check: (1) ESP32 plugin loaded, (2) cmd_vel topic correct, (3) Physics not paused (Spacebar in Gazebo)

---

## 📚 REFERENCE MATERIALS

| Topic | Resource |
|-------|----------|
| ROS2 Jazzy | docs.ros.org/en/jazzy/ |
| Gazebo Harmonic | gazebosim.org/docs/harmonic |
| Fusion 360 | youtube.com/@AutodeskFusion360 |
| URDF Tutorial | docs.ros.org/en/jazzy/Tutorials/URDF/ |
| Nav2 |navigation.ros.org/ |

---

## 💬 GET HELP

When stuck:
1. Check `simulation/docs/SIMULATION_GUIDE.md`
2. Check `docs/FUSION360_WORKFLOW.md`
3. Run diagnostics: `python3 scripts/test_peripherals.py`
4. Ask in repository Issues

**Remember:** Complete ALL simulation work before buying hardware. Save money and frustration by validating in simulation first.

---

*Mentorship Program Active*
*Your mentor believes in you!*
*Complete simulation → Complete design → Conquer hardware*