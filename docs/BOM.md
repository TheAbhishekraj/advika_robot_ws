# ADVIKA 3.0 BILL OF MATERIALS (BOM)

**Version:** 1.0
**Date:** 2026-07-25
**Currency:** USD (estimate, prices may vary)

---

## PHASE 1: 3D PRINTED PARTS (DIY)

| Part | Qty | Material | Print Time | Status | Est. Cost |
|------|-----|----------|------------|--------|-----------|
| Chassis Base v3 | 1 | PETG | 2.5h | Design Needed | $3-5 |
| Wheel Hub Left | 1 | PETG | 45min | Design Needed | $1 |
| Wheel Hub Right | 1 | PETG | 45min | Design Needed | $1 |
| LiDAR Tower | 1 | PETG | 1.5h | Design Needed | $2 |
| Top Dome | 1 | PETG (translucent) | 2h | Design Needed | $3 |
| Motor Mounts | 2 | PETG | 30min each | Design Needed | $1 |
| Battery Tray | 1 | PETG | 1h | Design Needed | $1.50 |
| Camera Bracket | 1 | PETG | 45min | Design Needed | $1 |
| ToF Holder | 1 | PETG | 20min | Design Needed | $0.50 |
| Front Bumper | 1 | TPU 95A | 1h | Design Needed | $2 |
| Rear Bumper | 1 | TPU 95A | 1h | Design Needed | $2 |
| **SUBTOTAL** | | | **~12h** | | **~$18** |

**Print Settings:**
- PETG: 250°C nozzle, 80°C bed, 30-50% infill
- TPU 95A: 235°C nozzle, 60°C bed, 20% infill
- All parts: 0.2mm layer height, 4 perimeters

---

## PHASE 2: STRUCTURAL PARTS (Purchase)

| Part | Qty | Est. Cost | Link/Notes |
|------|-----|-----------|------------|
| JGA25-370 Motors | 2 | $28-35 | with 334 PPR encoders |
| 65mm Wheel Set | 2 | $12-18 | Compatible with JGA25 |
| M3 Brass Threaded Inserts | 20pcs | $5 | For chassis mounting |
| M3 × 8mm screws | 20pcs | $2 | For motor mounts |
| M3 × 12mm screws | 10pcs | $1 | For general assembly |
| M2.5 Standoffs | 4pcs | $2 | For RPi mounting |
| 6mm D-Shaft (100mm) | 1 | $3 | For wheel hub interface |
| **SUBTOTAL** | | **$53-66** | |

---

## PHASE 3: ELECTRONICS

### Compute
| Part | Qty | Est. Cost | Notes |
|------|-----|-----------|-------|
| Raspberry Pi 5 (8GB) | 1 | $80 | Essential |
| 32GB microSD Card | 1 | $10 | Class 10, A2 |
| USB-C Power Supply (5A) | 1 | $15 | For Pi 5 |

### Motor Controller
| Part | Qty | Est. Cost | Notes |
|------|-----|-----------|-------|
| ESP32-S3 DevKit C1 | 1 | $15 | Or M5Stack AtomS3 |
| USB-C Cable | 1 | $5 | |
| Logic Level Shifter | 2 | $3 | 3.3V ↔ 5V |

### Sensors
| Part | Qty | Est. Cost | Notes |
|------|-----|-----------|-------|
| LD06 LiDAR | 1 | $55-70 | 360° 12m range |
| VL53L5CX ToF Array | 1 | $35-45 | 8×8 array |
| BNO055 IMU | 1 | $15 | 9-axis |
| SSD1306 OLED 128×64 | 1 | $8 | I2C display |

### Cameras
| Part | Qty | Est. Cost | Notes |
|------|-----|-----------|-------|
| Raspberry Pi Camera Module 3 Wide | 2 | $50 | 120° FOV each |
| Camera Cables (150mm) | 2 | $5 | FPC extension |

### Power
| Part | Qty | Est. Cost | Notes |
|------|-----|-----------|-------|
| 3S 5000mAh LiPo Battery | 1 | $30 | With XT60 connector |
| 3S BMS Board | 1 | $10 | Battery protection |
| Step-Up Converter (5V/3A) | 1 | $8 | For electronics |
| XT60 Connectors | 2 | $3 | Power connections |
| JST-XH Balance Connector | 1 | $2 | For charger |

**ELECTRONICS SUBTOTAL:** ~$309-362

---

## PHASE 4: CASES & ENCLOSURES

| Part | Qty | Est. Cost | Notes |
|------|-----|-----------|-------|
| ESP32 Enclosure | 1 | Print yourself | PETG |
| LiDAR Mount | 1 | Print yourself | PETG |
| Display Bezel | 1 | Print yourself | PETG |
| Cable Management Clips | 10 | Print yourself | PETG |

---

## PHASE 5: TOOLS (If Not Owned)

| Part | Est. Cost | Notes |
|------|-----------|-------|
| Calipers (digital) | $15-25 | Essential for verification |
| Screwdriver Set | $10 | M2, M2.5, M3, M4 |
| Soldering Iron | $20 | For connectors |
| Wire Strippers | $8 | |
| Multimeter | $20 | |
| Heat Shrink Tubing Set | $5 | |

**TOOLS SUBTOTAL:** ~$78-93 (if buying everything)

---

## GRAND TOTAL SUMMARY

| Category | Min Cost | Max Cost |
|----------|----------|----------|
| 3D Printed Parts | $18 | $18 |
| Structural Parts | $53 | $66 |
| Electronics | $309 | $362 |
| Cases/Enclosures | $0 | $0 (print yourself) |
| Tools | $78 | $93 |
| **GRAND TOTAL** | **$458** | **$539** |

---

## RECOMMENDED: STARTUP BUDGET (Simulation Validated)

Before buying everything, start with:

### Minimum Viable Robot ($180)
| Part | Cost |
|------|------|
| Raspberry Pi 5 (8GB) | $80 |
| ESP32-S3 DevKit | $15 |
| LD06 LiDAR | $60 |
| 3S Battery + BMS | $25 |
| **Total** | **$180** |

This lets you:
- Build robot chassis
- Test locomotion
- Run SLAM
- Validate sensors

### Full Build ($458-539)
Add cameras, ToF, IMU, display for complete functionality.

---

## SUPPLIER RECOMMENDATIONS

### Electronics
| Part | Supplier | Notes |
|------|----------|-------|
| Raspberry Pi | raspberrypi.com | Official |
| ESP32 | amazon.com or maker店 | |
| LD06 LiDAR | Amazon or Aliexpress | "YDLIDAR X4" or "LD06" |
| VL53L5CX | Adafruit or SparkFun | |
| Batteries | CNHL or CNB (Amazon) | 3S 5000mAh |

### 3D Printing
| Service | Notes |
|---------|-------|
| JLCPCB | $2-5 per part, 1-2 week delivery |
| Treatstock | Online quote tool |
| Local Library | Often free maker spaces |
| Buy Ender 3 V3 KE | ~$200, own printer |

### Hardware
| Item | Supplier |
|------|----------|
| Motors, Wheels | Amazon or Aliexpress |
| Fasteners | McMaster-Carr or local hardware store |
| Brass Inserts | Amazon (M3 brass heat set) |

---

## PURCHASE ORDER (Recommended)

### First Order (Chassis Build)
1. Raspberry Pi 5 8GB - $80
2. ESP32-S3 - $15
3. JGA25-370 Motors ×2 - $30
4. Wheels ×2 - $15
5. 3S Battery - $30
6. M3 screws/inserts - $10
7. Power supply - $15
**Subtotal: ~$195**

### Second Order (Sensors)
1. LD06 LiDAR - $60
2. VL53L5CX - $40
3. Cameras ×2 - $50
**Subtotal: ~$150**

### Third Order (Fine-Tuning)
1. BNO055 IMU - $15
2. SSD1306 Display - $8
3. Additional cables, connectors - $20
**Subtotal: ~$43**

---

## ✅ BEFORE PURCHASING

1. ✅ Complete simulation validation (Gazebo works)
2. ✅ Design and print all CAD parts
3. ✅ Test fit components physically
4. ✅ Verify budget available

---

*Remember: Complete simulation and design FIRST*
*BOM Date: 2026-07-25 - Check prices before ordering*