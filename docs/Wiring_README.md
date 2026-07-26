# ADVIKA 3.0 — COMPLETE WIRING DIAGRAM

**Version:** 1.0 | **Date:** 2026-07-26

---

## Overview

This document contains the complete electrical wiring for Advika 3.0.
The companion SVG file (`wiring_diagram.svg`) provides a full-color,
labelled schematic for printing and reference.

---

## Power Distribution

```
┌─────────────────────────────────────────────────────────────────┐
│                    3S2P 18650 Li-Ion Battery                   │
│                       11.1V  /  5200mAh                          │
│                     XT60 connector (red = +)                    │
└────────────────────────────┬──────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              │                              │
              ▼                              ▼
    ┌─────────────────┐           ┌─────────────────┐
    │  BMS (I2C 0x0B)  │           │  DRV8833 Motor  │
    │  Over-current   │           │    Driver       │
    │  Over-voltage   │           │   (Left/Right)  │
    │  Short-circuit  │           └───────┬─────────┘
    └──────┬──────────┘                   │
           │                              │ PWM + DIR
           ▼                              ▼
┌──────────────────────────────────────────────────────────┐
│              5V BUCK CONVERTER (LM2596 / MP1584)         │
│                        5V / 3A max                         │
└──┬─────┬──────┬──────┬──────┬──────┬──────┬──────┬─────────┘
   │     │      │      │      │      │      │      │
   ▼     ▼      ▼      ▼      ▼      ▼      ▼      ▼
  Pi5  ESP32  LiDAR  ToF    OLED   IMU   Camera Camera
  USB-C UART   5V    3.3V   3.3V  3.3V  (A)   (B)
```

---

## Motor Driver Wiring (DRV8833)

```
ESP32-S3 DevKitC-1          DRV8833                 JGA25-370 Motor
─────────────────          ──────                 ───────────────
GPIO 4  (LEFT_PWM)  ──────►  AIN1
GPIO 5  (LEFT_DIR1) ──────►  AIN2  ──────┐
GPIO 6  (LEFT_DIR2) ──────►  AIN3  ──────┤──►  MOTOR A (Left)
                                       │
GPIO 7  (LEFT_ENC_A) ◄─── Encoder A   │
GPIO 8  (LEFT_ENC_B) ◄─── Encoder B    │

GPIO 9  (RIGHT_PWM) ─────►  BIN1
GPIO 10 (RIGHT_DIR1) ─────►  BIN2  ─────┐
GPIO 11 (RIGHT_DIR2) ─────►  BIN3  ─────┤──►  MOTOR B (Right)
                                        │
GPIO 12 (RIGHT_ENC_A) ◄─── Encoder A   │
GPIO 13 (RIGHT_ENC_B) ◄─── Encoder B    │

         AOFT / VMOT ────────── Battery (+) direct
         PGND     ───────────── Battery (-) direct
```

---

## Sensor Pinouts

### YDLIDAR X4 / LD06 (UART)
| LiDAR Pin | Wire Color | ESP32 GPIO | Notes |
|-----------|------------|------------|-------|
| VCC (5V)  | Red        | —          | From 5V buck |
| GND       | Black      | —          | Common GND |
| TX        | Green      | GPIO 44   | LiDAR → ESP |
| RX        | Blue       | GPIO 43   | ESP → LiDAR |

### VL53L5CX ToF Array (I2C)
| ToF Pin | ESP32 GPIO | Notes |
|---------|------------|-------|
| SDA     | GPIO 1     | I2C data |
| SCL     | GPIO 2     | I2C clock |
| VCC     | 3.3V LDO   | |
| GND     | GND        | |

### Pi Camera Module 3 Wide ×2 (USB-C)
| Camera | Connection | Notes |
|--------|------------|-------|
| Horizon (forward) | USB-A port on Pi 5 | `/dev/video0` |
| Floor (downward)  | USB-A port on Pi 5 | `/dev/video1` |

### BNO055 IMU (I2C)
| IMU Pin | ESP32 GPIO | Notes |
|---------|------------|-------|
| SDA     | GPIO 1     | Shared I2C bus |
| SCL     | GPIO 2     | Shared I2C bus |
| VCC     | 3.3V       | |
| GND     | GND        | |

### SSD1306 OLED 128×64 (I2C)
| OLED Pin | ESP32 GPIO | Notes |
|----------|------------|-------|
| SDA      | GPIO 1     | Shared I2C bus |
| SCL      | GPIO 2     | Shared I2C bus |
| VCC      | 3.3V LDO   | |
| GND      | GND        | |

---

## Safety Circuit

```
                    E-STOP BUTTON (NC)
                         ┌──┐
    Battery(+) ──────────┤  ├───┬─────────────────┐
                          │  │ │                 │
    Battery(-) ───────────┴──┴─┴─┤                 │
                                  │                 │
                      Motor power cuts here when  │
                      E-Stop is pressed (NC relay) │
                                              │    │
                                              ▼    ▼
                                    ┌──────────────┐
                                    │  Motor Driver│
                                    │   Enable     │
                                    └──────────────┘
```

### E-Stop Logic
- E-Stop button = Latching NC (16mm panel mount)
- Connected to ESP32 GPIO 14 (with 10k pull-up)
- Active LOW: pressing button pulls GPIO 14 LOW
- ISR on ESP32 cuts motor PWM immediately (< 1ms)
- ISR also sets motor driver ENABLE low

---

## Wiring Checklist

| Wire | Gauge | Color | From | To |
|------|-------|-------|------|----|
| Battery + | 16 AWG | Red | Battery XT60 | BMS VMOT |
| Battery - | 16 AWG | Black | Battery XT60 | BMS GND |
| Motor A+ | 18 AWG | Red | DRV8833 OUTA | Left Motor |
| Motor A- | 18 AWG | Black | DRV8833 OUTA | Left Motor |
| Motor B+ | 18 AWG | Red | DRV8833 OUTB | Right Motor |
| Motor B- | 18 AWG | Black | DRV8833 OUTB | Right Motor |
| 5V Bus | 20 AWG | Red | 5V Buck | Pi5, LiDAR |
| 3.3V Bus | 22 AWG | Red | 3.3V LDO | ToF, IMU, OLED |
| GND Bus | 20 AWG | Black | Buck GND | All devices |
| UART TX | 26 AWG | Green | LiDAR TX | ESP32 GPIO 44 |
| UART RX | 26 AWG | Blue | ESP32 GPIO 43 | LiDAR RX |
| I2C SDA | 26 AWG | White | Shared SDA | ToF, IMU, OLED |
| I2C SCL | 26 AWG | Yellow | Shared SCL | ToF, IMU, OLED |
| USB-C | Shielded | — | Pi 5 | ESP32 (UART debug) |

---

## Cable Routing

```
TOP VIEW OF CHASSIS (base plate)
─────────────────────────────────────────────────────
  FRONT                                                  REAR
  ┌──────────────────────────────────────────────────┐
  │  [LiDAR Tower]     ┌──────────┐                 │
  │      │              │ ESP32    │                 │
  │      │              │ (front)  │                 │
  │      │              └──────────┘                 │
  │      │                                            │
  │      │         ┌────────────┐                     │
  │      │         │  Raspberry │                     │
  │      │         │    Pi 5    │                     │
  │      │         │  (center)  │                     │
  │      │         └────────────┘                     │
  │      │                                            │
  │      │  [Motor L]              [Motor R]          │
  │      │     ●                         ●             │
  │      │                                          │
  │      └───── Cable channel (base plate) ──────────

  LEFT WHEEL                            RIGHT WHEEL

  ToF sensor bar: routed along front edge
  Camera FPC: routed through mid frame slots
  IMU: located center of base plate
```

---

## Connectors

| Connector | Type | Location | Purpose |
|-----------|------|----------|---------|
| Battery XT60 | XT60 male | Base plate rear | Main power input |
| BMS balance | JST-XH 4-pin | Base plate | Battery cell balancing |
| Motor L | JST-PH 4-pin | Base plate | Left motor + encoder |
| Motor R | JST-PH 4-pin | Base plate | Right motor + encoder |
| LiDAR | JST-SR 4-pin | Mid frame top | LD06 UART + power |
| ToF bar | JST-XH 6-pin | Front bumper | I2C sensor array |
| E-Stop | 2-pin terminal | Top cover rear | Emergency stop |
| USB-C (Pi) | USB-C | Side of chassis | Programming + charging |
| FPC (cam) | 15-pin FPC | Mid frame | Camera modules |
| OLED | 4-pin JST | Top cover front | Display panel |

---

## I2C Device Addresses

| Device | Address |
|--------|---------|
| VL53L5CX (ToF L) | 0x29 |
| VL53L5CX (ToF R) | 0x29 |
| BNO055 (IMU) | 0x28 |
| SSD1306 (OLED) | 0x3C |
| BMS (Smart) | 0x0B |

---

## Voltage Rails

| Rail | Voltage | Source | Loads |
|------|---------|--------|-------|
| VBAT | 11.1–12.6V | Battery | BMS, DRV8833 |
| V5V | 5.0V ± 5% | Buck Converter | LiDAR, Pi 5, USB hubs |
| V3V3 | 3.3V ± 5% | LDO | ToF, IMU, OLED, ESP32 |

---

## Estimated Current Draw

| Component | Current (A) | Voltage |
|-----------|------------|---------|
| Raspberry Pi 5 (peak) | 1.5 | 5V |
| ESP32-S3 (peak) | 0.5 | 5V / 3.3V |
| LiDAR X4 | 0.4 | 5V |
| 2× VL53L5CX | 0.05 | 3.3V |
| 2× Pi Camera | 0.5 | 5V (USB) |
| Motors (stall) | 4.0 | VBAT |
| OLED + IMU | 0.02 | 3.3V |
| **Total peak** | **~7A** | |
| **Normal operation** | **~1.5A** | |

Battery runtime estimate: 5200mAh / 1500mA ≈ **3.5 hours** typical