# ADVIKA 3.0 — LEARNING MANUAL (I AM 5 YEARS OLD VERSION)
**Simple Step-by-Step Guide to Build Your Own Robot**

*Version: 1.0 | For: Beginners | Reading Level: 5 years old +*

---

## 🤖 WHAT IS ADVIKA?

Advika is a **smart robot** that can move around your house all by itself!

- It has **eyes** (cameras) — one looking forward, one looking down
- It has **ears** (LiDAR) — it shoots invisible light beams to see walls
- It has a **brain** (Raspberry Pi 5 computer) — it thinks like you!
- It has **feet** (wheels) — two big wheels that go forward/back
- It has a **voice** — it can speak using a speaker

You give Advika commands and it follows them!

---

## 📦 PART 1: BEFORE YOU START — WHAT YOU NEED

Imagine building with LEGO blocks — but bigger and cooler!

### The Shopping List

| Thing to Buy | How Many | What it Does |
|-------------|----------|-------------|
| Raspberry Pi 5 | 1 | Robot's brain — like a tiny computer |
| ESP32-S3 | 1 | Robot's helper — moves the motors |
| Motors (JGA25-370) | 2 | Robot's legs — make the wheels spin |
| LiDAR (YDLIDAR X4) | 1 | Robot's ears — sees walls |
| Camera (Pi Camera 3) | 2 | Robot's eyes — sees things |
| Battery (3S2P 18650) | 1 | Robot's food — gives it power |
| Wheels + Casters | Set | Robot's shoes — helps it roll |
| Many small screws | Lots! | Holds everything together |
| 3D printed parts | 23 pieces | Robot's body — plastic shapes |
| Wires + Cables | Many | Robot's nerves — connect everything |
| Buck Converter | 1 | Power teacher — gives right power to each part |

---

## 🔧 PART 2: SET UP YOUR COMPUTER (FOR SIMULATION)

Before building the real robot, you can make it work on your computer first!

### Step 2.1: Install Ubuntu (The Robot's Computer Language)

Ubuntu is like Windows — but for robots!

```
1. Download Ubuntu 24.04 LTS from: ubuntu.com/download/desktop
2. Put it on a USB stick (8GB minimum)
3. Turn on your computer, press F12 (or Del) to choose boot menu
4. Select "USB Drive" and press Enter
5. Click "Install Ubuntu" — choose "Erase disk and install"
6. Your name: advika
   Computer name: advika-pi
   Password: advika123
7. Wait 15 minutes for installation
8. Restart computer
```

✅ **Test:** You should see a desktop with "advika" in the corner.

### Step 2.2: Install Robot Software (ROS2 Jazzy)

ROS2 is like a language robots speak. It helps different robot parts talk to each other.

Open a terminal (press `Ctrl + Alt + T`) and type each line:

```bash
# Step 1: Update your computer
sudo apt update
sudo apt upgrade -y

# Step 2: Install robot software
sudo apt install -y curl gnupg lsb-release
curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo gpg --dearmor -o /usr/share/keyrings/ros.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros.gpg] http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
sudo apt update
sudo apt install -y ros-jazzy-desktop python3-colcon-rosdep python3-rosdep

# Step 3: Tell Ubuntu you like robots now!
source /opt/ros/jazzy/setup.bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc

# Step 4: Install Gazebo (robot playground)
sudo apt install -y gazebo

# Step 5: Install other tools
sudo apt install -y python3-pip git tree Terminator

# Step 6: Get the robot brain (code from internet)
cd ~
git clone https://github.com/TheAbhishekraj/advika_robot_ws.git
cd advika_robot_ws
./scripts/install_and_generate.sh   # Makes all the 3D parts

# Step 7: Build the robot code
cd ~/advika_robot_ws
colcon build
source install/setup.bash
```

✅ **Test:** Type `ros2 topic list` — you should see robot topics!

---

## 🏠 PART 3: RUN THE ROBOT IN THE COMPUTER (SIMULATION)

Now Advika exists inside your computer! You can make it move without breaking anything.

### Step 3.1: Start the Robot Playground

Open **4 terminal windows** (right-click terminal → "Open in Tab"):

**Window 1 — Start the robot world:**
```bash
cd ~/advika_robot_ws
source install/setup.bash
ros2 launch advika_sim sim_bringup.launch.py
```

**Window 2 — See what the robot sees:**
```bash
rviz2 -d src/advika_description/rviz/advika.rviz
```

**Window 3 — Make the robot move:**
```bash
ros2 topic pub /advika/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.3}, angular: {z: 0.0}}" -r 10
```
(The robot moves forward! Press Ctrl+C to stop.)

**Window 4 — Watch robot brain messages:**
```bash
ros2 topic echo /advika/scan
```
(You see the LiDAR distances! Numbers like "1.5" means wall is 1.5 meters away.)

### Step 3.2: Open the Web Dashboard

1. Open your browser (Chrome/Firefox)
2. Type in the address bar: `http://localhost:5000`
3. You see the robot control panel!
4. Use the joystick or keyboard to move the robot

✅ **Test:** The robot should appear in the Gazebo window. The dashboard should show the LiDAR scan!

---

## 🔨 PART 4: BUILD THE REAL ROBOT

Now the fun part — build Advika for real!

### Tools You Need
- Screwdriver (Phillips #1)
- Hex keys (1.5mm, 2mm, 2.5mm)
- Soldering iron (250°C) — for heat-set inserts
- Pliers — for holding small things
- Caliper — for measuring
- Multimeter — for checking electricity

### Step 4.1: Prepare the 3D Printed Parts

Your 3D printed parts arrive like puzzle pieces. They need finishing:

```
1. Remove all "support" material (the extra plastic underneath)
2. Clean the parts with isopropyl alcohol (70%)
3. Test-fit the M3 heat-set inserts:
   - Heat soldering iron to 250°C
   - Press insert into hole (it looks like a brass ring)
   - Wait 5 seconds, remove iron
   - Let cool 30 seconds
   - Screw in M3 screw to test — should turn smoothly
4. Sand any rough edges with 400-grit sandpaper
5. Check all 23 parts exist (see BOM)
```

### Step 4.2: Build the Base (The Robot's Feet)

The base plate is the bottom — everything goes on top of it.

```
1. Find the BASE PLATE (the big flat octagonal piece)
2. Press heat-set inserts into ALL the small holes (about 40 holes)
3. Install the MOTOR MOUNTS L and R on the left and right
   - Use M3 × 8mm screws to bolt them down
4. Slide JGA25-370 MOTORS into the motor mounts
5. Attach WHEEL HUBS onto the motor shafts (6mm D-shape)
   - Tighten the set-screw firmly
6. Press BALL CASTERS into the front and rear caster housings
7. Snap caster housings into the base plate recesses
8. Install BATTERY RETAINER at the rear
```

✅ **Test:** Push the robot — wheels and casters should roll smoothly.

### Step 4.3: Add the Mid Frame (The Robot's Body)

```
1. Stack the MID FRAME onto the BASE PLATE
2. Screw in M3 × 8mm at all 4 corners
3. Install standoffs for ESP32 (front)
4. Install standoffs for Raspberry Pi 5 (center)
```

### Step 4.4: Install Electronics (The Robot's Nerves)

**CAUTION: Electricity can hurt! Ask an adult for help with soldering.**

```
1. Install the DRV8833 motor driver on standoffs
   - Put thermal pad between driver and chassis
2. Connect motor wires (left = GPIO 4-8, right = GPIO 9-13 on ESP32)
3. Install ESP32-S3 on front standoffs
4. Connect ESP32 to DRV8833 with wires
5. Connect ESP32 to Raspberry Pi 5 with USB-C cable
6. Install I2C devices on shared bus:
   - ToF sensor bar (front)
   - BNO055 IMU (center of base plate)
   - SSD1306 OLED (top cover)
   - All share SDA (GPIO 1) and SCL (GPIO 2)
7. Install YDLIDAR X4 on top of mid frame (3 screws)
8. Install cameras:
   - Horizon camera: 15° upward tilt (front)
   - Floor camera: 45° downward tilt (underneath)
9. Install 5V buck converter and connect to battery
10. Connect 3.3V LDO to 5V output for I2C sensors
```

### Step 4.5: Install Bumpers (The Robot's Feelers)

```
1. Thread M4 shoulder bolts through bumper mounts
2. Attach compression springs onto bolts
3. Screw into chassis — springs give 10mm floating travel
4. Wire microswitches (2 per bumper) to ESP32 GPIO inputs
5. Press WS2812B LED rings into bumper channels
```

### Step 4.6: Close the Robot (Top Cover)

```
1. Place GASKET_TOP on the mid-frame perimeter lip
2. Gently lower TOP COVER onto mid frame
3. Press corner latches to snap closed
4. Secure with M3 × 8mm at 4 corners
5. Mount E-STOP button through rear hole
6. Install SDD1306 OLED into front cutout
```

---

## 🔌 PART 5: POWER UP AND TEST

### Step 5.1: Safety Check FIRST (Before any power!)

```
□ All wires connected correctly? (Double-check polarity!)
□ No bare wires touching? (Use electrical tape)
□ Battery voltage: 11.1V–12.6V? (Measure with multimeter)
□ E-Stop button works? (Press it — should cut motor power)
□ Solder joints solid? (No cold joints)
```

### Step 5.2: First Power On

```
1. Connect battery (XT60 — red to red!)
2. The LED ring should light up (rainbow pattern)
3. The OLED display should show "ADVIKA 3.0 READY"
4. If smoke appears — UNPLUG IMMEDIATELY and check wiring!
```

### Step 5.3: Test Each Part

| Test | How to Test | Success |
|------|------------|---------|
| Motors spin | `python3 test_motors.py` | Both wheels turn |
| LiDAR sees | `ros2 topic echo /advika/scan` | Numbers appear |
| Cameras see | `ros2 topic echo /advika/horizon_camera/image_raw` | Image data |
| IMU works | `ros2 topic echo /advika/imu/data` | Numbers changing |
| E-Stop works | Press E-Stop button | Motors stop immediately |
| Bumpers work | Press bumper by hand | Numbers change in terminal |

---

## 🎮 PART 6: DRIVE THE ROBOT

### Method 1: Web Dashboard (Easiest!)

1. Open browser to `http://<pi-ip>:5000`
2. Use joystick or keyboard:
   - `i` = Forward
   - `k` = Stop
   - `m` = Backward
   - `j` = Turn left
   - `l` = Turn right

### Method 2: Terminal

```bash
# Move forward
ros2 topic pub /advika/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2}, angular: {z: 0}}" -r 5

# Turn left
ros2 topic pub /advika/cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.0}, angular: {z: 0.5}}" -r 5
```

### Method 3: Keyboard Teleop

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

---

## 🔍 PART 7: MAKE THE ROBOT SMART (NAVIGATION)

### Step 7.1: Make a Map (SLAM)

```bash
# Drive the robot around to build a map
ros2 launch nav2_bringup slam.launch.py
# Use keyboard to drive around every room
# When done: Ctrl+C — map is saved!
```

### Step 7.2: Send Robot to a Goal

```bash
# Start navigation
ros2 launch nav2_bringup nav2.launch.py

# In another terminal, set a goal
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "{pose: {header: {frame_id: 'map'}, pose: {position: {x: 2.0, y: 1.0}}}}"
# Robot drives to (2.0, 1.0) on its own!
```

---

## 🆘 PART 8: WHEN THINGS GO WRONG

### Problem: Robot doesn't move
```
□ Is battery charged? (Should be 11.1V+)
□ Are motors connected? (Check XT60 connector)
□ Is ESP32 powered? (Blue LED on ESP32 should blink)
□ Does E-Stop work? (Press and hold reset)
□ Check: `ros2 topic echo /advika/cmd_vel` — does data appear?
```

### Problem: Robot spins in circles
```
□ Are motor wires swapped? (Left/right might be reversed)
□ Check: which wheel is spinning the wrong way?
□ Fix: swap the motor wire pairs in DRV8833
```

### Problem: LiDAR doesn't work
```
□ Is LiDAR getting power? (5V — measure with multimeter)
□ Is UART connected? (TX/RX not swapped)
□ Check: `ls /dev/serial/by-id/` — LiDAR appears?
□ Fix: `sudo chmod 666 /dev/ttyUSB0`
```

### Problem: Camera shows black/no image
```
□ Is camera cable installed correctly? (Gold contacts facing in)
□ Does `v4l2-ctl --list-devices` show camera?
□ Try: `ros2 launch advika_bringup cameras.launch.py`
```

### Problem: Can't connect to WiFi
```
□ Is Pi 5 WiFi turned on? (Check raspberrypi.local with Fing app)
□ Run: `nmtui` to connect to WiFi
□ Check SSH: `ssh advika@advika-pi.local`
```

### Problem: ROS topics not appearing
```
□ Did you source the workspace? (`source install/setup.bash`)
□ Is ROS domain set? (`export ROS_DOMAIN_ID=0`)
□ Check: `ros2 topic list` — should show advika topics
□ Try: restart with `colcon build && source install/setup.bash`
```

---

## 🎓 PART 9: HOW THE ROBOT WORKS (SIMPLE EXPLANATION)

### The Robot's Brain (Raspberry Pi 5)

The Pi 5 runs **ROS2 Jazzy** — it thinks for the robot!

```
1. Sensors (cameras, LiDAR, IMU) send data to Pi
2. Pi processes the data — "I see a wall 50cm ahead"
3. Pi decides what to do — "Stop! or Turn!"
4. Pi sends commands to ESP32 — "Go forward at speed 0.2"
```

### The Robot's Helper (ESP32-S3)

The ESP32 is like the robot's **reflexes** — it does fast things instantly.

```
1. Receives high-level commands from Pi ("go forward")
2. Sends precise PWM signals to motors
3. Reads encoder data ("wheel has turned 10 degrees")
4. Sends position data back to Pi
5. Has a safety ISR — E-Stop stops motors in < 1ms
```

### The Robot's Senses

| Sense | Device | How it Works |
|-------|--------|-------------|
| Vision (far) | Pi Camera 3 | Takes 640×480 photos 30× per second |
| Vision (near) | VL53L5CX ToF | Shoots infrared, measures time to return |
| Hearing | YDLIDAR X4 | Spins and shoots laser, measures reflection |
| Balance | BNO055 | Measures acceleration + magnetic heading |
| Touch | Microswitches | Detect when bumper hits something |

---

## 📋 QUICK REFERENCE CARDS

### Terminal Commands
```bash
# Start robot
source install/setup.bash
ros2 launch advika_sim sim_bringup.launch.py

# Check topics
ros2 topic list
ros2 topic echo /advika/scan

# Drive robot
ros2 run teleop_twist_keyboard teleop_twist_keyboard

# Navigate
ros2 launch nav2_bringup nav2.launch.py
```

### WiFi / SSH
```bash
# SSH into robot
ssh advika@advika-pi.local

# Copy files to robot
scp my_file.py advika@advika-pi.local:~/advika_robot_ws/

# Check robot IP
hostname -I
```

---

## ✅ YOUR CHECKLIST

Before declaring "Done!" — check each item:

- [ ] All 23 STL parts printed
- [ ] All fasteners installed (no loose screws)
- [ ] All electronics connected and working
- [ ] Battery charged (11.1V–12.6V)
- [ ] E-Stop tested and working
- [ ] Dashboard opens in browser
- [ ] Robot moves forward/backward
- [ ] Robot turns left/right
- [ ] LiDAR shows obstacle distances
- [ ] Cameras show live feed
- [ ] IMU shows orientation
- [ ] ToF shows floor distances
- [ ] LED ring animates
- [ ] Speaker makes sounds
- [ ] ROS2 topics are active
- [ ] Navigation works (robot goes to goal)
- [ ] Robot can map a room

---

**Congratulations!** You built Advika 3.0 — a real autonomous mobile robot! 🎉

```
    ╔═══════════════════════════╗
    ║   ADVIKA 3.0 COMPLETE!    ║
    ║   You are a robotics       ║
    ║   engineer now!             ║
    ╚═══════════════════════════╝
```

Questions? Open an issue at: https://github.com/TheAbhishekraj/advika_robot_ws/issues