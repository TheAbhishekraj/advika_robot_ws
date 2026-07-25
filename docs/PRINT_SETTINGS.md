# ADVIKA 3.0 — 3D PRINT SETTINGS

**Version:** 1.0 | **Date:** 2026-07-25

---

## 🖨️ PETG — Structural Parts

Use for: Base Plate, Mid Frame, Top Cover, Motor Mounts, Wheel Hubs, Caster Housings, Camera Mounts, Battery Retainer, ToF Mount, ESP32 Enclosure, IMU Mount.

### Printer Profile

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Nozzle** | 0.4mm | Standard |
| **Nozzle Temp** | 240°C | Lower by 5°C for stringing-prone machines |
| **Bed Temp** | 75–80°C | PEI sheet or glass with glue stick |
| **Layer Height** | 0.2mm | 0.16mm for fine detail parts (camera mounts) |
| **First Layer** | 0.28mm | Better adhesion |
| **Perimeters** | 3–4 | 4 for base plate & wheel hubs |
| **Top/Bottom Layers** | 4 | Minimum for water resistance |
| **Print Speed** | 50–60 mm/s | Slow for overhangs |
| **Travel Speed** | 150 mm/s | |
| **Retraction** | 1.5mm @ 30mm/s | Direct drive; 5mm @ 45mm/s for Bowden |
| **Cooling Fan** | 50–70% | Full off for first 2 layers |
| **Supports** | On overhangs > 45° | Tree supports preferred |
| **Brim** | 5mm | For base plate, mid frame |

### Per-Part Infill

| Part | Infill | Pattern | Reason |
|------|--------|---------|--------|
| Base Plate | 50% | Grid | Structural floor, motor loads |
| Mid Frame | 30% | Gyroid | Lightweight walls, good rigidity |
| Top Cover | 30% | Grid | Moderate loads |
| Wheel Hub | 50% | Grid | High rotational stress |
| Motor Mount | 30% | Grid | Moderate clamping loads |
| Camera Mount | 30% | Gyroid | Light part, vibration dampening |
| All other PETG | 30% | Gyroid | General use |

### PETG Tips
- Dry filament before printing (4h @ 65°C in food dehydrator)
- Use PEI build plate or apply glue stick to glass
- PETG sticks **too well** to bare PEI — use release agent if needed
- Reduce fan for better layer adhesion on thick walls
- Print enclosed if possible (reduces warping on >200mm parts)

---

## 🔵 TPU 95A — Flexible Parts

Use for: Front/Rear Bumpers, Top Gasket, Pi Vibration Pad, Motor Isolation Rings.

### Printer Profile

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Nozzle** | 0.4mm | Direct drive STRONGLY recommended |
| **Nozzle Temp** | 220–230°C | Higher = more flexible result |
| **Bed Temp** | 45–55°C | |
| **Layer Height** | 0.2mm | 0.24mm acceptable for bumpers |
| **Perimeters** | 2–3 | 2 for gaskets, 3 for bumpers |
| **Top/Bottom Layers** | 3 | |
| **Print Speed** | 20–30 mm/s | **DO NOT exceed 35mm/s** |
| **Travel Speed** | 100 mm/s | Minimize retractions |
| **Retraction** | 0.5–1.0mm @ 15mm/s | Test first; some setups need 0 retraction |
| **Cooling Fan** | 100% | Full cooling |
| **Supports** | None (design avoids overhangs) | |
| **Brim** | 8mm | TPU needs extra adhesion |

### Per-Part Infill

| Part | Infill | Pattern | Reason |
|------|--------|---------|--------|
| Bumper Front/Rear | 40% | Grid | Energy absorption, LED channel support |
| Gasket — Top | 0% | — | Vase mode or 2 perimeters only |
| Gasket — Pi Pad | 15% | Grid | Vibration isolation |
| Gasket — Motor | 15% | Grid | Vibration isolation |

### TPU Tips
- **Direct drive extruder is essential** — Bowden will jam TPU
- Disable retraction entirely if experiencing grinding
- Print one part at a time (no multi-part plates)
- Slow down ALL movements, including non-print moves
- No post-processing needed (TPU is flexible as-printed)

---

## 🔍 LiDAR Dome — Clear/Translucent PETG

| Parameter | Value |
|-----------|-------|
| **Material** | Clear / Natural PETG |
| **Layer Height** | 0.12mm |
| **Perimeters** | 2 |
| **Infill** | 0% (vase mode recommended) |
| **Speed** | 25–30 mm/s |
| **Fan** | 30% (optical clarity priority) |

---

## ⚠️ Common Mistakes

| Mistake | Fix |
|---------|-----|
| PETG stringing | Dry filament, increase retraction, lower temp by 5°C |
| Base plate warping | Use brim, enclose printer, check bed adhesion |
| TPU jamming | Use direct drive, reduce print speed to 15mm/s |
| Wheel hub not round | Calibrate XY steps, check belt tension |
| Dome not clear | Lower speed, lower fan, ensure filament is bone-dry |
| Parts don't fit | Verify printer calibration with 20×20×20mm test cube |

---

## 📏 Test Print Before Full Run

```
1. Print 20×20×20mm calibration cube (PETG)
   → Verify dimensions within ±0.2mm

2. Print M3 insert boss test block
   → Test heat-set insert fit (should press in at 250°C with soldering iron)

3. Print TPU flexibility test strip (80×10×2mm)
   → Should flex freely without cracking

PASS ALL 3 → Proceed with full part prints
```
