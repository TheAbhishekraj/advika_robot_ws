# ADVIKA 3.0 â 3D Print Guide

## Printer Settings
- Layer Height: 0.2mm | Nozzle: 0.4mm | Material: PLA
- Bed Temp: 60°C | Nozzle Temp: 210°C | Speed: 50mm/s

## Print Order & Settings

| Priority | File | Infill | Supports | Notes |
|----------|------|--------|----------|-------|
| 1 | advika_chassis.stl | 20% | No | Print flat, use brim |
| 2 | advika_wheel_hub_L.stl | 50% | No | Check 8mm bore fit |
| 3 | advika_wheel_hub_R.stl | 50% | No | Check 8mm bore fit |
| 4 | advika_motor_mount_L.stl | 40% | No | Critical alignment |
| 5 | advika_motor_mount_R.stl | 40% | No | Critical alignment |
| 6 | advika_lidar_tower.stl | 30% | No | Use brim (tall part) |
| 7 | advika_top_dome.stl | 15% | YES | Supports on underside |
| 8 | advika_battery_tray.stl | 30% | No | |
| 9 | advika_bumper_front.stl | 45% | No | Orient flat |
| 10 | advika_bumper_rear.stl | 45% | No | Orient flat |
| 11 | advika_esp32_enclosure.stl | 25% | No | |
| 12 | advika_esp32_lid.stl | 25% | No | NEW v2.0 |
| 13 | advika_camera_horizon.stl | 25% | No | |
| 14 | advika_camera_floor.stl | 25% | No | |
| 15 | advika_imu_mount.stl | 30% | No | |

## Post-Print Checks
- [ ] Test M3 threaded insert installation in chassis
- [ ] Verify 8mm axle slides through wheel hub bores
- [ ] Confirm D-flat aligns with motor shaft
- [ ] Check ESP32 lid fits snugly (clearance 0.2mm)
- [ ] Test motor mount M3 hole spacing

## Troubleshooting
| Issue | Fix |
|-------|-----|
| Bore too tight | Sand with 220 grit or drill 8.1mm |
| Warping on chassis | Add brim 8mm + increase bed temp 65°C |
| Dome stringing | Reduce temp by 5°C, increase travel speed |
| Tower wobble | Add 5mm brim, print slower 30mm/s |

*STL files location: `C:\Users\HP\Advika_3.0\STL\`*
