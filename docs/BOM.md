# ADVIKA 3.0 — BILL OF MATERIALS (BOM)
**Version:** 2.0 | **Date:** 2026-07-26 | **Currency:** INR (₹)

> All prices are estimates for Indian market. Source from Robu.in, Amazon.in, or AliExpress as noted.
> Last verified: July 2026. Prices fluctuate — check before ordering.

---

## 🖨️ 3D PRINTED PARTS (In-House or Print Service)

| # | Part Name | STL File | Qty | Material | Est. Print Time | Filament (g) | Est. Cost |
|---|-----------|----------|-----|----------|-----------------|---------------|-----------|
| A | Base Plate | advika30_base_plate.stl | 1 | PETG | 4h | 120g | ₹240 |
| B | Mid Frame | advika30_mid_frame.stl | 1 | PETG | 8h | 180g | ₹360 |
| C | Top Cover + LiDAR Dome | advika30_top_cover.stl | 1 | PETG + Clear dome | 5h | 100g | ₹200 |
| D | Motor Mount L | advika30_motor_mount_L.stl | 1 | PETG | 1h | 30g | ₹60 |
| E | Motor Mount R | advika30_motor_mount_R.stl | 1 | PETG | 1h | 30g | ₹60 |
| F | Wheel Hub L | advika30_wheel_hub_L.stl | 1 | PETG | 1.5h | 40g | ₹80 |
| G | Wheel Hub R | advika30_wheel_hub_R.stl | 1 | PETG | 1.5h | 40g | ₹80 |
| H | Caster Housing Front | advika30_caster_housing_F.stl | 1 | PETG | 0.5h | 15g | ₹30 |
| I | Caster Housing Rear | advika30_caster_housing_R.stl | 1 | PETG | 0.5h | 15g | ₹30 |
| J | Camera Mount — Horizon | advika30_camera_mount_front.stl | 1 | PETG | 0.5h | 10g | ₹20 |
| K | Camera Mount — Floor | advika30_camera_mount_floor.stl | 1 | PETG | 0.5h | 10g | ₹20 |
| L | Battery Retainer | advika30_battery_retainer.stl | 1 | PETG | 0.5h | 15g | ₹30 |
| M | Bumper Front | advika30_bumper_front.stl | 1 | TPU 95A | 2h | 50g | ₹150 |
| N | Bumper Rear | advika30_bumper_rear.stl | 1 | TPU 95A | 2h | 50g | ₹150 |
| O | ToF Sensor Bar | advika30_tof_bar.stl | 1 | PETG | 0.5h | 8g | ₹16 |
| P | ESP32 Enclosure | advika30_esp32_enclosure.stl | 1 | PETG | 1h | 15g | ₹30 |
| Q | IMU Mount | advika30_imu_mount.stl | 1 | PETG | 0.5h | 8g | ₹16 |
| R | Gasket — Top Perimeter | advika30_gasket_top.stl | 1 | TPU 95A | 0.5h | 10g | ₹30 |
| S | Gasket — Pi Pad | advika30_gasket_pi.stl | 1 | TPU 95A | 0.3h | 5g | ₹15 |
| T | Gasket — Motor Ring | advika30_gasket_motor.stl | 2 | TPU 95A | 0.2h×2 | 6g | ₹18 |
| U | LiDAR Disk | advika30_lidar_disk.stl | 1 | PETG | 0.3h | 8g | ₹16 |
| V | Display Board | advika30_display.stl | 1 | PETG | 0.3h | 5g | ₹10 |
| W | IMU Board | advika30_imu_board.stl | 1 | PETG | 0.3h | 5g | ₹10 |
| | **TOTAL PRINT** | | **23** | | **~32h** | **~750g** | **₹1,701** |

### Filament Cost Breakdown
| Filament | Amount | Price |
|----------|--------|-------|
| PETG (any color) | ~600g | ₹1,200 |
| TPU 95A | ~125g | ₹800 |
| Clear PETG | ~30g (partial roll) | ₹300 |
| **Total Filament** | | **₹2,300** |

---

## ⚡ ELECTRONIC COMPONENTS

| Component | Model | Qty | Unit Price (₹) | Total (₹) | Supplier | Link |
|-----------|-------|-----|----------------|-----------|----------|------|
| Compute Board | Raspberry Pi 5 (8GB) | 1 | ₹6,500 | ₹6,500 | Robu.in | [Link](https://robu.in/product/raspberry-pi-5-8gb/) |
| MicroController | ESP32-S3 DevKitC-1 | 1 | ₹1,200 | ₹1,200 | Robu.in | [Link](https://robu.in/product/esp32-s3-devkitc-1/) |
| Motor Driver | DRV8833 Dual H-Bridge | 1 | ₹250 | ₹250 | Robu.in | [Link](https://robu.in/product/drv8833-motor-driver/) |
| DC Motors | JGA25-370 (170RPM, 6mm D-shaft) | 2 | ₹1,200 | ₹2,400 | Robu.in | [Link](https://robu.in/product/jga25-370-motor/) |
| LiDAR | YDLIDAR X4 (360°, 10Hz) | 1 | ₹4,500 | ₹4,500 | Robu.in | [Link](https://robu.in/product/ydlidar-x4/) |
| ToF Sensor | VL53L5CX (8×8 array, 4m) | 2 | ₹1,500 | ₹3,000 | Mouser | [Link](https://mou.sr/4dSfvR9) |
| Camera | Pi Camera Module 3 Wide | 2 | ₹1,600 | ₹3,200 | Robu.in | [Link](https://robu.in/product/pi-camera-module-3-wide/) |
| IMU | BNO055 9-DOF | 1 | ₹1,800 | ₹1,800 | Robu.in | [Link](https://robu.in/product/bno055-imu/) |
| Battery | 3S2P 18650 Li-Ion (11.1V 5200mAh + BMS) | 1 | ₹2,400 | ₹2,400 | Robu.in | [Link](https://robu.in/product/18650-3s2p-bms/) |
| OLED Display | SSD1306 128×64 I2C | 1 | ₹200 | ₹200 | Robu.in | [Link](https://robu.in/product/ssd1306-oled-128x64/) |
| LED Ring | WS2812B 24-LED (80mm) | 2 | ₹400 | ₹800 | Robu.in | [Link](https://robu.in/product/ws2812b-led-ring-24-led/) |
| Speaker | 4Ω 3W Mini Speaker (28mm) | 1 | ₹100 | ₹100 | Amazon.in | [Link](https://amzn.in/9x2k3) |
| E-Stop Button | 16mm Latching NC | 1 | ₹150 | ₹150 | Robu.in | [Link](https://robu.in/product/16mm-estop-button/) |
| Power Connector | XT60 Pair (male+female) | 1 | ₹80 | ₹80 | Robu.in | [Link](https://robu.in/product/xt60-connector-pair/) |
| Balance Connector | JST-XH 4-pin | 1 | ₹30 | ₹30 | Robu.in | [Link](https://robu.in/product/jst-xh-4-pin/) |
| Ball Casters | 15mm Ball Caster | 2 | ₹200 | ₹400 | Robu.in | [Link](https://robu.in/product/15mm-ball-caster/) |
| Buck Converter | MP1584 5V 3A | 1 | ₹80 | ₹80 | Robu.in | [Link](https://robu.in/product/mp1584-buck-converter/) |
| LDO Regulator | AMS1117-3.3V | 2 | ₹20 | ₹40 | Robu.in | [Link](https://robu.in/product/ams1117-3v3-ldo/) |
| **Electronics Total** | | | | **₹27,130** | | |

---

## 🔩 FASTENERS & HARDWARE

| Item | Specification | Qty | Unit Price (₹) | Total (₹) | Supplier |
|------|---------------|-----|----------------|-----------|----------|
| M3 Heat-Set Insert | OD 4.2mm, 3.5mm deep, brass | 50 | ₹8 | ₹400 | Robu.in |
| M3 × 8mm SHCS | Socket Head Cap Screw | 20 | ₹5 | ₹100 | Robu.in |
| M3 × 12mm SHCS | Socket Head Cap Screw | 10 | ₹6 | ₹60 | Robu.in |
| M3 × 16mm SHCS | Socket Head Cap Screw | 5 | ₹7 | ₹35 | Robu.in |
| M2.5 × 6mm SHCS | For Pi 5 + camera mounts | 8 | ₹6 | ₹48 | Robu.in |
| M4 × 20mm Shoulder Bolt | Bumper floating mount | 8 | ₹25 | ₹200 | Robu.in |
| M4 Compression Spring | 10mm free, Ø4mm | 8 | ₹18 | ₹144 | Robu.in |
| M2.5 Standoff (M/F) | 10mm Aluminum | 8 | ₹15 | ₹120 | Robu.in |
| M3 Washer | Flat washer | 20 | ₹1 | ₹20 | Robu.in |
| Cable Ties | 100mm × 2.5mm | 50 | ₹2 | ₹100 | Robu.in |
| Heat Shrink | Assorted 5cm pack | 1 | ₹100 | ₹100 | Robu.in |
| Double-Sided Tape | 3M VHB 10mm × 5m | 1 | ₹150 | ₹150 | Amazon.in |
| Thermal Pad | 50×50×1mm (for DRV8833) | 1 | ₹50 | ₹50 | Robu.in |
| **Fasteners Total** | | | | **₹1,527** | |

---

## 🔌 CABLES & WIRING

| Item | Specification | Qty | Unit Price (₹) | Total (₹) |
|------|---------------|-----|----------------|-----------|
| Dupont Wire | 26AWG various colors (10m) | 1 | ₹150 | ₹150 |
| USB-A to USB-C Cable | 30cm (Pi to ESP32) | 1 | ₹80 | ₹80 |
| USB-A Extension | 50cm (camera hub) | 1 | ₹60 | ₹60 |
| FPC Cable | 15-pin 0.5mm (cameras) | 2 | ₹50 | ₹100 |
| JST-PH 4-pin | Motor connector | 2 | ₹20 | ₹40 |
| JST-SR 4-pin | LiDAR connector | 1 | ₹20 | ₹20 |
| JST-XH 6-pin | ToF bar connector | 1 | ₹20 | ₹20 |
| Shrink Label Tube | 3:1 ratio (labelling) | 1 | ₹100 | ₹100 |
| **Cables Total** | | | | **₹570** |

---

## 📦 ENCLOSURE & MECHANICAL

| Item | Qty | Unit Price (₹) | Total (₹) |
|------|-----|----------------|-----------|
| 3M PE Foam Sheet | 3× sheets | ₹100 | ₹300 |
| Rubber Grommets (M12) | 4 | ₹15 | ₹60 |
| M3 Wing Nuts (optional) | 8 | ₹5 | ₹40 |
| Rubber Feet (silicon) | 4 | ₹10 | ₹40 |
| **Mechanical Total** | | | **₹440** |

---

## 💰 TOTAL COST SUMMARY

| Category | INR (₹) | Notes |
|----------|---------|-------|
| 🖨️ Filament (PETG + TPU) | ₹2,300 | 1 roll PETG + 0.5 roll TPU |
| ⚡ Electronics | ₹27,130 | See table above |
| 🔩 Fasteners & Hardware | ₹1,527 | |
| 🔌 Cables & Wiring | ₹570 | |
| 📦 Mechanical | ₹440 | |
| **GRAND TOTAL** | **₹31,967** | ~$385 USD |

> **Note:** Electronics are ~85% of total cost. Using AliExpress for cameras and ToF sensors can reduce electronics cost by ₹4,000–6,000.
> Battery price may vary by 20% depending on cell quality (Sony/Molicel vs generic).

---

## 📋 ORDERING CHECKLIST

### Must Order (Electronics)
- [ ] Raspberry Pi 5 8GB
- [ ] ESP32-S3 DevKitC-1
- [ ] DRV8833 Motor Driver
- [ ] JGA25-370 Motors ×2
- [ ] YDLIDAR X4
- [ ] VL53L5CX ×2
- [ ] Pi Camera Module 3 Wide ×2
- [ ] BNO055 IMU
- [ ] 3S2P 18650 Battery Pack with BMS
- [ ] SSD1306 OLED
- [ ] WS2812B LED Ring ×2
- [ ] MP1584 Buck Converter
- [ ] AMS1117-3.3V LDO ×2

### Must Order (Hardware)
- [ ] M3 Heat-Set Inserts ×50
- [ ] M3 SHCS assortment kit
- [ ] M2.5 SHCS ×8
- [ ] M4 Shoulder Bolts ×8 + Springs ×8
- [ ] 15mm Ball Casters ×2
- [ ] 10mm M2.5 Standoffs ×8
- [ ] XT60 connectors ×2
- [ ] JST connectors (assorted)
- [ ] PETG 1kg roll (your color choice)
- [ ] TPU 95A 500g roll

### Print Yourself (STLs included in repo)
- [ ] All 23 parts from `src/advika_cad/meshes/` or `meshes_freecad/`

---

## 🛒 INDIAN SUPPLIERS QUICK REFERENCE

| Supplier | Website | Strengths | Notes |
|----------|---------|-----------|-------|
| **Robu.in** | robu.in | ROS/robot parts, fast delivery | Primary source for motors, LiDAR, ESP32 |
| **RoboCart** | robocart.in | Budget electronics | Good for sensors |
| **Elementz** | elementz.in | I2C sensors, IMUs | Genuine parts |
| **Amazon.in** | amazon.in | Fast Prime delivery | Best for Pi 5, cameras |
| **AliExpress** | aliexpress.com | Budget cameras, ToF | 2-3 week delivery, use Bhub for shipping |
| **Mouser India** | mouser.in | Industrial quality | VL53L5CX, genuine parts |

---

## 💡 COST OPTIMIZATION TIPS

1. **LiDAR** — LD06 on AliExpress is ₹2,500 vs YDLIDAR X4 at ₹4,500 (lower resolution but functional)
2. **Cameras** — Use USB webcam modules instead of Pi Camera v3 for ₹400 each
3. **IMU** — MPU6050 (₹150) instead of BNO055 (₹1,800) for basic IMU
4. **Battery** — Build 3S2P pack yourself from 6× 18650 cells (₹1,200) vs pre-built (₹2,400)
5. **WiFi** — Pi 5 built-in WiFi is sufficient (no Ethernet module needed)