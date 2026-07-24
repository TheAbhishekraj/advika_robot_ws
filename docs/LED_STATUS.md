# LED Status Patterns — Advika 3.0

> **Hardware:** WS2812B LED rings on bumpers, controlled via ESP32  
> **Status LED:** GPIO 2 onboard ESP32 (single colour)

---

## Startup Sequence (Power-On)

| Step | Pattern | Meaning |
|------|---------|---------|
| Boot | 🔵 Blue — 3 quick blinks | ESP32 firmware loaded |
| Init | 🌈 Rainbow swirl (2s) | System initialising |
| Ready | ⚪ Solid white | All systems nominal — robot ready |

---

## Operational Patterns (WS2812B Rings)

| Pattern | Colour | State | Description |
|---------|--------|-------|-------------|
| Solid | ⚪ White | `READY` | Idle, all systems normal |
| Slow pulse | 🔵 Blue | `PERCEIVING` | Scanning sensors, capturing frame |
| Solid | 🟡 Yellow | `PLANNING` | Computing navigation route |
| chase | 🔵 Blue | `NAVIGATING` | Autonomous navigation active |
| Solid | 🔴 Red | `OBSTACLE_ALERT` | ToF/LiDAR triggered — halted |
| Fast flash | 🔴 Red | `EMERGENCY` | E-Stop pressed |
| Solid | 🟢 Green | `TASK_COMPLETE` | Goal reached successfully |
| Slow flash | 🟡 Yellow | `LOW_BATTERY` | Battery < 11.1V — return to charge |
| Solid | 🟠 Orange | `MOTOR_ERROR` | Motor stall or driver fault |
| Off | ⚫ Dark | `SHUTDOWN` | Graceful shutdown in progress |

---

## Status LED (ESP32 Onboard GPIO 2)

| Pattern | Meaning |
|---------|---------|
| 3 blinks on boot | Firmware boot OK |
| Solid ON | UART active, Pi connected |
| Rapid flash (5Hz) | Receiving drive commands |
| OFF | No UART activity (Pi not connected) |

---

## Child-Friendly Explanation (`manuals/i_am_5/`)

| Colour | Meaning (child language) |
|--------|-------------------------|
| ⚪ White | "I'm awake and happy!" |
| 🔵 Blue | "I'm thinking..." |
| 🟢 Green | "I did it! Goal reached!" |
| 🟡 Yellow | "I'm planning my trip..." |
| 🔴 Red | "Stop! Something is in my way." |
| ⚫ Off | "I'm going to sleep." |

---

*Last Updated: 2026-07-24 | Version: 0.1.0*
