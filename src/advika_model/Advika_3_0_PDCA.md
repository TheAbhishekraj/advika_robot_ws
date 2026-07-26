# ADVIKA 3.0 PDCA — PLAN DO CHECK ACT
## Fusion 360 Robot Model Generation

---

## P — PLAN

### 1. Objective
Generate a complete 3D CAD model of the Advika 3.0 robot using Fusion 360, including all 12 components with proper materials and STL export.

### 2. Success Criteria
- [ ] All 12 components created successfully
- [ ] Assembly positions match specification
- [ ] Materials applied correctly
- [ ] STL files exported for 3D printing
- [ ] No modeling errors

### 3. Resources Required
- Fusion 360 (latest version)
- Fusion 360 API Python environment
- MCP Server connection (or manual script execution)
- ~2-4 hours for full execution

### 4. Timeline
| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Connection Setup | 30 min | MCP working or script ready |
| Component Creation | 2-3 hours | All 12 parts modeled |
| Assembly & Export | 30 min | STL files ready |

### 5. Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| MCP connection fails | Medium | Medium | Manual script execution fallback |
| Complex geometry fails | Low | High | Simplify features |
| Material not found | Low | Low | Create custom material |
| Performance issues | Medium | Low | Use lightweight preview mode |

---

## D — DO

### Phase 1: Connection Setup

**Option A — MCP Server:**
1. Open Fusion 360 → Preferences → General → API
2. Enable "Fusion MCP Server" (port 27182)
3. In Claude Desktop: Settings → Connectors → Install Autodesk Fusion
4. Verify hammer icon appears

**Option B — Direct Script (Fallback):**
1. Copy `advika_3_0_generator.py` to Fusion 360 scripts folder
2. In Fusion 360: Shift+S → Scripts → Run → Select file
3. Monitor console for progress

### Phase 2: Execute Generation

Execute the following in order:

```bash
# If using MCP
[Execute via Claude Desktop with Fusion 360 connection]

# If using manual script
[Run advika_3_0_generator.py from Fusion 360]
```

### Phase 3: Verify Components

Check each component after generation:
1. Chassis Base — 300×240×5 mm plate with fillets
2. Motor Mounts — 6mm shaft hole, 4×M3 holes
3. Wheel Hubs — 65mm diameter, D-shaft, 4×M3 holes
4. LiDAR Tower — 150mm height, 2° draft, hollow
5. Top Dome — 115mm radius, translucent
6. Camera Mounts — 25×24mm, tilted correctly
7. IMU Mount — 20×20×5mm with center hole
8. Battery Tray — Shell with XT60/JST cuts
9. Bumpers — TPU style, hollow with microswitch holes
10. ESP32 Enclosure — Shell with USB-C cutout

---

## C — CHECK

### Verification Checklist

**Model Structure:**
- [ ] Document has 12 components
- [ ] Each component named correctly
- [ ] No duplicate bodies

**Geometry:**
- [ ] Chassis dimensions: 300×240×5 mm ±0.5mm
- [ ] Wheel hubs: 65mm diameter × 20mm thick
- [ ] LiDAR tower: 150mm height, hollow
- [ ] All fillets present (5mm on chassis)
- [ ] All holes through extruded

**Assembly Positions (verify against spec):**
| Component | X | Y | Z |
|-----------|---|---|---|
| Chassis Base | 0 | 0 | 0 |
| Left Motor | -90 | 70 | -10 |
| Right Motor | 90 | -70 | -10 |
| Left Wheel | -90 | 70 | -15 |
| Right Wheel | 90 | -70 | -15 |
| LiDAR Tower | 0 | 0 | 75 |
| Top Dome | 0 | 0 | 155 |
| Horizon Camera | 140 | 0 | 75 |
| Floor Camera | 120 | 0 | 25 |
| IMU | 0 | 0 | 5 |
| Battery Tray | 0 | -20 | -5 |
| Front Bumper | 150 | 0 | 5 |
| Rear Bumper | -150 | 0 | 5 |
| ESP32 | 0 | 20 | 5 |

**Materials:**
- [ ] Chassis: Dark Blue (43, 91, 132)
- [ ] Wheels: Black (26, 26, 26)
- [ ] LiDAR Tower: White (240, 240, 240)
- [ ] Top Dome: 60% transparency
- [ ] Bumpers: Red (230, 57, 70)
- [ ] Battery Tray: Orange (255, 140, 0)

**STL Export:**
- [ ] All 12 components exported
- [ ] High quality setting
- [ ] Files named correctly (advika_*.stl)
- [ ] Files open in slicer without errors

---

## A — ACT

### If All Checks Pass:
1. Model is ready for 3D printing
2. Export Bill of Materials (BOM)
3. Proceed to hardware assembly
4. Document any lessons learned

### If Issues Found:

**Component Missing:**
- Re-run specific generation function
- Check for sketch errors

**Wrong Dimensions:**
- Verify input parameters
- Check Fusion units setting

**Material Not Applied:**
- Manually assign from Appearance library
- Create custom appearance if needed

**STL Export Failed:**
- Check disk space
- Simplify complex geometry
- Try lower quality setting

### Continuous Improvement:

For next iteration of Advika 3.1:
1. Add mounting brackets for easier assembly
2. Consider snap-fit connections
3. Add cable routing channels
4. Optimize for material usage

---

## EXECUTION SUMMARY

| Item | Status |
|------|--------|
| Script Created | ✅ |
| PDCA Document | ✅ |
| Connection Setup | ⏳ User action required |
| Model Generation | ⏳ User action required |
| STL Export | ⏳ User action required |

**Next Steps:**
1. Set up Fusion 360 connection (MCP or manual)
2. Execute the Python script
3. Verify components against CHECK list
4. Export STL files
5. Ready for 3D printing