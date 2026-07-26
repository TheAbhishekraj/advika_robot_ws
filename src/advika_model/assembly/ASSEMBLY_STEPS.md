# ADVIKA 3.0 â Assembly Instructions

## Tools Required
- M2, M2.5, M3, M4 hex drivers
- Soldering iron (for threaded inserts)
- Drill + 8mm drill bit (if bore needs widening)
- Wire crimper + heat shrink
- Multimeter

## Pre-Assembly Checklist
- [ ] All parts printed successfully
- [ ] 8mm axle fits through wheel hub bore
- [ ] M3 threaded inserts installed in chassis (x20)
- [ ] Motor shafts match D-flat in wheel hubs
- [ ] ESP32 fits in enclosure with lid clearance

## Step-by-Step Assembly

### STEP 1 â Chassis Base (Z=0 to 3mm)
1. Place `advika_chassis` flat on workbench
2. Install 20x M3 heat-set inserts at mounting points
3. Attach `advika_bumper_front` at X=+105mm with M3x6 x4
4. Attach `advika_bumper_rear` at X=-105mm with M3x6 x4

### STEP 2 â Wheel Drivetrain
1. Mount `advika_motor_mount_L` at Y=+60mm with M3x10 x4
2. Mount `advika_motor_mount_R` at Y=-60mm with M3x10 x4
3. Insert `advika_axle_shaft` (D8x170mm steel) through both mounts
4. Install DC motors into motor mounts, align shaft with D-flat
5. Slide `advika_wheel_hub_L` onto axle at Y=75-85mm
6. Secure with M4 set screw x1
7. Slide `advika_wheel_hub_R` onto axle at Y=-75 to -85mm
8. Secure with M4 set screw x1
9. **Test:** Spin wheels by hand â should rotate freely

### STEP 3 â Electronics Deck
1. Mount `advika_imu_mount` at centre (0,0) with M2x5 x4
2. Install MPU6050 board, connect I2C wires
3. Mount `advika_esp32_enclosure` at X=-70,Y=-40mm with M2.5x6 x4
4. Install ESP32 board, route USB-C cable along rear edge

### STEP 4 â Power
1. Slide LiPo battery into `advika_battery_tray` from rear
2. Secure with velcro strap
3. **CRITICAL:** Verify JST connector polarity before connecting

### STEP 5 â Sensor Tower
1. Mount `advika_lidar_tower` at centre with M3x12 x4
2. Press-fit `advika_top_dome` onto tower top at Z=83mm
3. Mount RPLiDAR A1 inside dome with M3 x3

### STEP 6 â Cameras
1. Mount `advika_camera_horizon` at X=+80mm with M2x5 x2
2. Mount `advika_camera_floor` at X=+90mm tilted 30° downward

### STEP 7 â Final Checks
- [ ] All bolts tightened
- [ ] Wheels spin freely on axle
- [ ] No cable pinching under chassis
- [ ] IMU level (use spirit level)
- [ ] ESP32 powers on via USB
- [ ] LiDAR spins freely inside dome

### STEP 8 â Software
1. Flash ESP32 with MicroROS firmware
2. Upload URDF to ROS2 workspace
3. Run: `ros2 launch advika_description gazebo.launch.py`
4. Test teleoperation: `ros2 run teleop_twist_keyboard teleop_twist_keyboard`

*Photos folder: `C:\Users\HP\Advika_3.0\photos\`*
*Videos folder: `C:\Users\HP\Advika_3.0\videos\`*
