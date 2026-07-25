# ADVIKA 3.0 — MECHANICAL ASSEMBLY GUIDE

**Version:** 1.0 | **Date:** 2026-07-25

---

## 🔩 Required Tools

| Tool | Purpose |
|------|---------|
| Soldering iron (adjustable) | Heat-set insert installation @ 250°C |
| Hex key set (1.5mm, 2mm, 2.5mm) | M3 SHCS, M2.5 SHCS |
| Phillips #1 screwdriver | Pi 5 standoff screws |
| Needle-nose pliers | Connector seating, clip engagement |
| Digital caliper | Part verification, fit checking |
| Wire cutters / strippers | Cable management |
| Multimeter | Continuity checks, voltage verification |

---

## 🔧 Fastener Schedule

| Fastener | Qty | Where Used |
|----------|-----|------------|
| M3 × 6mm Brass Heat-Set Insert | ~40 | All PETG boss locations |
| M3 × 8mm SHCS | ~20 | Base-to-frame, motor brackets |
| M3 × 12mm SHCS | ~10 | Through-frame attachments |
| M3 × 16mm SHCS | ~5 | Long stack-ups (caster, LiDAR) |
| M2.5 × 6mm SHCS | 8 | Pi 5 standoffs, camera mounts |
| M4 × 20mm Shoulder Bolt + Spring | 8 | Bumper floating mount |
| 10mm M2.5 Aluminum Standoff | 8 | ESP32, Pi 5 elevation |

---

## 📋 Assembly Order (14 Steps)

> **GOLDEN RULE:** Battery → Motors → Electronics → Cables → Top Cover

### Step 1: Heat-Set Inserts
Press M3 brass heat-set inserts into ALL boss locations on base plate, mid frame, and top cover.
- Set soldering iron to **250°C**
- Apply gentle straight-down pressure
- Insert should sit flush ±0.5mm
- Total: ~40 inserts across 3 parts
- **Test with spare M3 screw after each insert cools**

### Step 2: Battery Installation
Slide 3S2P 18650 Li-Ion battery pack into base plate tray from the rear.
- Battery slides on C-channel rails
- Secure with battery retainer thumb screw
- Connect XT60 power connector (red = positive, verify with multimeter)
- Connect JST-XH balance connector

### Step 3: Motor Installation
Bolt motor mount brackets (L/R) to base plate motor pockets.
- Insert JGA25-370 motors into split-collar clamp
- Close collar, tighten M3 pinch bolt (1.5 N⋅m)
- Press wheel hub onto 6mm D-shaft
- Tighten M3 radial set screw
- Verify: wheel spins freely, no wobble

### Step 4: Caster Installation
Snap caster housings (F/R) into base plate recesses.
- Press-fit 15mm ball casters
- Confirm retention clip engages (audible click)
- Verify: ball rotates freely in all directions

### Step 5: Mid Frame Stacking
Stack mid frame onto base plate.
- Align 4× corner insert bosses
- Secure with M3 × 8mm SHCS into heat-set inserts (0.8 N⋅m)
- Verify: frame walls sit flush, no gaps

### Step 6: ESP32-S3 Mounting
Mount ESP32-S3 DevKitC-1 on front standoffs.
- 4× M2.5 standoffs (10mm height)
- USB-C port must face forward for programming access
- Leave 10mm clearance below for airflow

### Step 7: DRV8833 Driver Mounting
Mount DRV8833 dual H-bridge near ESP32.
- 15mm standoffs with thermal pad to chassis floor beneath
- Wire motor leads (verify polarity with multimeter)

### Step 8: Raspberry Pi 5 Mounting
Mount Pi 5 on center platform standoffs (25mm elevation).
- 4× M2.5 × 6mm SHCS through Pi mounting holes
- Place TPU vibration gasket (gasket_pi) beneath Pi
- Ensure 10mm clearance below for airflow
- SD card slot must align with top cover access slot

### Step 9: IMU Installation
Adhesive-mount BNO055 IMU on base plate locating pins.
- Center of base plate, vibration-isolated position
- Place TPU motor gaskets around motor mount faces
- Align 2× Ø2mm locating pins with IMU board holes
- Secure with M2 screws or adhesive

### Step 10: Camera Installation
- **Horizon Camera (15° up-tilt):** Mount camera_mount_front at front panel, bolt Pi Camera Module 3 Wide with TPU gasket
- **Floor Camera (45° down-tilt):** Mount camera_mount_floor on underside front
- Route FPC cables through mid frame cable channels

### Step 11: LiDAR Installation
Install YDLIDAR X4 / LD06 on mid frame top ring.
- 3× M3 on 60mm PCD
- Route 6-pin JST cable through center shaft
- LiDAR must be level (use spirit level)

### Step 12: Cable Management
Route all internal cabling through base plate and mid frame channels.
- Minimum bend radius: 10mm
- Leave 20mm service loops at all connectors
- Snap channel cover strips over open cable runs
- Label all connectors with heat-shrink labels

### Step 13: Bumper Installation
Install bumper_front and bumper_rear on M4 shoulder bolts with springs.
- 10mm floating travel (test compression)
- Confirm microswitch triggers at 5mm compression
- Press WS2812B LED rings into bumper channel
- Light-pipe diffuser faces outward

### Step 14: Top Cover & Final Assembly
Lower top cover onto mid frame.
- Place gasket_top on perimeter lip
- Engage 4× corner snap latches
- Confirm SD-card slot aligns with Pi 5 SD reader
- Confirm LiDAR dome sits centered over LiDAR ring
- Panel-mount 16mm E-Stop button through top cover rear hole
- Wire E-Stop NC contact in series with motor power

---

## ✅ Post-Assembly Verification

| Check | Test | Expected |
|-------|------|----------|
| Power on | Press E-Stop release, connect battery | LED ring illuminates |
| Motor test | `python3 scripts/test_peripherals.py` | Both wheels spin |
| LiDAR test | `ros2 topic echo /advika/scan --once` | Range data received |
| Camera test | `ros2 topic echo /advika/horizon_camera/image_raw --once` | Image data |
| IMU test | `ros2 topic echo /advika/imu/data --once` | Orientation data |
| E-Stop test | Press E-Stop button | Motors cut immediately |
| Bumper test | Press each bumper inward | Microswitch triggers |
