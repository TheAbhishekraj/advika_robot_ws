# Wiring Diagram

## Advika 3.0 Electrical Schematic

This directory contains the complete electrical wiring documentation.

### Files
- `Wiring_Diagram.pdf` -- Full electrical schematic (PDF)
- `Wiring_Diagram.svg` -- Vector version for editing
- `pinout_reference.md` -- Quick pin reference table
- `cable_routing.md` -- Cable management guide

### Power Distribution
```
3S LiPo Battery (11.1V, 5000mAh)
    |
    +---> BMS (I2C 0x0B) --+--> Main Power Switch
    |                        |
    |                        +--> 5V Buck Converter --+--> Raspberry Pi 5 (USB-C)
    |                        |                        +--> ESP32-S3 (USB/VIN)
    |                        |                        +--> Cameras (USB)
    |                        |                        +--> LiDAR (5V)
    |                        |                        +--> ToF Array (3.3V LDO)
    |                        |                        +--> Display (3.3V)
    |                        |
    +---> Motor Driver (DRV8833) --+--> Left JGA25-370
                                   +--> Right JGA25-370
```

### Pin Assignments (ESP32-S3)
| Pin | Function | Connected To |
|-----|----------|-------------|
| GPIO 4 | LEFT_PWM | Motor Driver A IN1 |
| GPIO 5 | LEFT_DIR1 | Motor Driver A IN2 |
| GPIO 6 | LEFT_DIR2 | Motor Driver A IN3 |
| GPIO 7 | LEFT_ENC_A | Left Encoder Channel A |
| GPIO 8 | LEFT_ENC_B | Left Encoder Channel B |
| GPIO 9 | RIGHT_PWM | Motor Driver B IN1 |
| GPIO 10 | RIGHT_DIR1 | Motor Driver B IN2 |
| GPIO 11 | RIGHT_DIR2 | Motor Driver B IN3 |
| GPIO 12 | RIGHT_ENC_A | Right Encoder Channel A |
| GPIO 13 | RIGHT_ENC_B | Right Encoder Channel B |
| GPIO 14 | E-STOP | E-Stop Button (active LOW) |
| GPIO 15 | BUZZER | Piezo Buzzer |
| GPIO 2 | STATUS_LED | Onboard LED |
| UART0 | USB | Raspberry Pi USB connection |
| I2C SDA | GPIO 8 | ToF Array, BMS, Display |
| I2C SCL | GPIO 9 | ToF Array, BMS, Display |

### Serial Connections
| Device | Port | Baud Rate | Protocol |
|--------|------|-----------|----------|
| ESP32-S3 | /dev/ttyUSB0 | 115200 | JSON-RPC 2.0 |
| LD06 LiDAR | /dev/ttyUSB1 | 230400 | LD Protocol |

### Safety Wiring
- E-Stop button wired to GPIO 14 with internal pull-up
- Hardware watchdog on ESP32 timer group 0
- Motor driver enable pin tied to ESP32 safety ISR output
- Battery low-voltage cutoff at 9.0V (BMS controlled)
