# ADVIKA 3.0 — BILL OF MATERIALS (BOM)

**Version:** 1.0 | **Date:** 2026-07-25

---

## 📦 PRINTED PARTS (In-House / Print Service)

| # | Part Name | Qty | Material | Est. Print Time | Filament (g) |
|---|-----------|-----|----------|-----------------|-------------|
| A | Base Plate | 1 | PETG | 4h | 120g |
| B | Mid Frame | 1 | PETG | 8h | 180g |
| C | Top Cover + LiDAR Dome | 1 | PETG (clear dome) | 5h | 100g |
| D | Motor Mount Bracket | 2 | PETG | 1h each | 30g each |
| E | Wheel Hub | 2 | PETG | 1.5h each | 40g each |
| F | Caster Housing | 2 | PETG | 0.5h each | 15g each |
| G | Camera Mount — Horizon | 1 | PETG | 0.5h | 10g |
| H | Camera Mount — Floor | 1 | PETG | 0.5h | 10g |
| I | Battery Retainer | 1 | PETG | 0.5h | 15g |
| J | Bumper Front/Rear | 2 | TPU 95A | 2h each | 50g each |
| K | ToF Sensor Mount | 1 | PETG | 0.5h | 8g |
| L | ESP32 Enclosure | 1 | PETG | 1h | 15g |
| M | IMU Mount | 1 | PETG | 0.5h | 8g |
| N | Gasket — Top Perimeter | 1 | TPU 95A | 0.5h | 10g |
| O | Gasket — Pi Pad | 1 | TPU 95A | 0.3h | 5g |
| P | Gasket — Motor Ring | 2 | TPU 95A | 0.2h each | 3g each |
| | **TOTAL PRINT** | **20** | | **~30h** | **~740g** |

### Filament Cost Estimate
| Filament | Amount | Cost (approx) |
|----------|--------|---------------|
| PETG (any color) | ~600g (1 roll) | ₹1,200 / $15 |
| TPU 95A | ~125g (partial roll) | ₹800 / $10 |
| Clear PETG (dome) | ~30g (partial roll) | ₹300 / $4 |
| **Filament Total** | | **₹2,300 / ~$29** |

---

## ⚡ ELECTRONIC COMPONENTS

| Component | Model | Qty | Price (INR) | Price (USD) | Supplier |
|-----------|-------|-----|-------------|-------------|----------|
| Compute Board | Raspberry Pi 5 (8GB) | 1 | ₹6,500 | $80 | raspberrypi.com / Robu.in |
| Motor Controller | ESP32-S3 DevKitC-1 | 1 | ₹1,200 | $15 | Robu.in / Amazon |
| H-Bridge Driver | DRV8833 Dual Motor Driver | 1 | ₹250 | $3 | Amazon / Robu.in |
| DC Motors | JGA25-370 (170RPM, 334PPR) | 2 | ₹1,200 | $15 ea. | Amazon / AliExpress |
| LiDAR | LD06 (360°, 12m, 10Hz) | 1 | ₹4,500 | $55 | AliExpress / Robu.in |
| ToF Sensor | VL53L5CX (8×8 array, 4m) | 2 | ₹1,500 | $18 ea. | Mouser / DigiKey |
| Cameras | Pi Camera Module 3 Wide | 2 | ₹1,600 | $20 ea. | raspberrypi.com |
| IMU | BNO055 9-DOF | 1 | ₹1,800 | $22 | Adafruit / Mouser |
| Battery | 3S2P 18650 Li-Ion (11.1V 5200mAh, BMS) | 1 | ₹2,400 | $30 | AliExpress / Amazon |
| OLED Display | SSD1306 128×64 I2C | 1 | ₹200 | $2.50 | Amazon |
| LED Ring | WS2812B 24-LED (80mm) | 2 | ₹400 | $5 ea. | AliExpress |
| Speaker | 4Ω 3W Mini Speaker (28mm) | 1 | ₹100 | $1.50 | Amazon |
| E-Stop | 16mm Latching Button (NC) | 1 | ₹150 | $2 | Amazon |
| Power Connector | XT60 Pair | 1 | ₹80 | $1 | Amazon |
| Balance Connector | JST-XH 4-pin | 1 | ₹30 | $0.50 | Amazon |
| Casters | 15mm Ball Caster | 2 | ₹200 | $2.50 ea. | Amazon |
| **Electronics Total** | | | **₹23,810** | **~$295** | |

---

## 🔩 FASTENERS & HARDWARE

| Item | Qty | Price (INR) | Price (USD) |
|------|-----|-------------|-------------|
| M3 Brass Heat-Set Threaded Insert (4.2mm OD, 3.5mm deep) | 40 | ₹400 | $5 |
| M3 × 8mm SHCS (Socket Head Cap Screw) | 20 | ₹100 | $1.50 |
| M3 × 12mm SHCS | 10 | ₹60 | $0.80 |
| M3 × 16mm SHCS | 5 | ₹40 | $0.50 |
| M2.5 × 6mm SHCS | 8 | ₹50 | $0.60 |
| M4 × 20mm Shoulder Bolt | 8 | ₹200 | $2.50 |
| M4 Compression Spring (10mm free length) | 8 | ₹150 | $2 |
| 10mm M2.5 Aluminum Standoff (M/F) | 8 | ₹120 | $1.50 |
| Zip ties (100mm) | 20 | ₹50 | $0.60 |
| Heat shrink tubing (assorted) | 1 set | ₹100 | $1.50 |
| **Fasteners Total** | | **₹1,270** | **~$16.50** |

---

## 💰 TOTAL COST SUMMARY

| Category | INR | USD |
|----------|-----|-----|
| 🖨️ Filament (PETG + TPU) | ₹2,300 | $29 |
| ⚡ Electronics | ₹23,810 | $295 |
| 🔩 Fasteners & Hardware | ₹1,270 | $16.50 |
| **GRAND TOTAL** | **₹27,380** | **~$340** |

> **Note:** Prices are approximate as of July 2026. Actual costs may vary by region and supplier. Bulk ordering (10+ of same fastener) reduces per-unit cost significantly.

---

## 📋 Ordering Checklist

- [ ] Raspberry Pi 5 (8GB)
- [ ] ESP32-S3 DevKitC-1
- [ ] DRV8833 Motor Driver
- [ ] JGA25-370 Motors ×2
- [ ] LD06 LiDAR
- [ ] VL53L5CX ToF Sensors ×2
- [ ] Pi Camera Module 3 Wide ×2
- [ ] BNO055 IMU
- [ ] 3S2P 18650 Battery Pack
- [ ] SSD1306 OLED Display
- [ ] WS2812B LED Rings ×2
- [ ] Mini Speaker
- [ ] E-Stop Button
- [ ] XT60 + JST-XH Connectors
- [ ] 15mm Ball Casters ×2
- [ ] M3 Heat-Set Inserts (pack of 50)
- [ ] M3 SHCS Assorted Kit
- [ ] M2.5 SHCS + Standoffs
- [ ] M4 Shoulder Bolts + Springs
- [ ] PETG Filament (1kg roll)
- [ ] TPU 95A Filament (500g roll)
- [ ] Clear PETG (250g or shared roll)