# coding: utf-8
"""
Advika 3.0 Robot Model Generator
Fusion 360 API Script

INSTALLATION:
1. Copy this file to: %APPDATA%\Autodesk\Autodesk Fusion 360\API\Scripts\Advika3_0\
2. In Fusion 360: Press Shift+S → Scripts → Run → Select advika_3_0_generator

VERIFICATION AFTER RUN:
- Check Browser tree for all component names
- Verify dimensions in Properties panel
- Export STL manually via File → Export
"""

import adsk
import adsk.core as core
import adsk.fusion as fusion
import math

# Global variables
app = core.Application.get()
design = fusion.FusionDocument.cast(app.activeProduct)
if not design:
    app.userSettings.warningDialog('No active Fusion 360 design. Please create a new design first.')
    raise RuntimeError('No active design')

rootComp = design.rootComponent
unitsMgr = app.preferences.unitPreferences

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def create_circle(sketch, center, radius):
    """Create a circle in a sketch"""
    centerPt = sketch.modelToSketchSpace(center)
    return sketch.sketchCurves.sketchCircles.addByCenterRadius(centerPt, radius)

def create_rectangle(sketch, cx, cy, width, height):
    """Create a center rectangle in a sketch"""
    w2, h2 = width / 2, height / 2
    p1 = sketch.modelToSketchSpace(core.Point3D.create(cx - w2, cy - h2, 0))
    p2 = sketch.modelToSketchSpace(core.Point3D.create(cx + w2, cy - h2, 0))
    p3 = sketch.modelToSketchSpace(core.Point3D.create(cx + w2, cy + h2, 0))
    p4 = sketch.modelToSketchSpace(core.Point3D.create(cx - w2, cy + h2, 0))
    sketch.sketchCurves.sketchLines.addByTwoPoints(p1, p2)
    sketch.sketchCurves.sketchLines.addByTwoPoints(p2, p3)
    sketch.sketchCurves.sketchLines.addByTwoPoints(p3, p4)
    sketch.sketchCurves.sketchLines.addByTwoPoints(p4, p1)
    return sketch

# ============================================================
# STEP 2.2: CHASSIS BASE
# ============================================================

def create_chassis_base():
    """Create Chassis Base: 300x240x5 mm plate with fillets and mounting holes"""
    comp = rootComp
    sketches = comp.sketches
    xyPlane = comp.xYConstructionPlane

    # Create main plate sketch
    sketch = sketches.add(xyPlane)
    sketch.name = 'Chassis Base Sketch'

    # Create center rectangle 300x240 mm
    create_rectangle(sketch, 0, 0, 300.0, 240.0)

    # Extrude 5 mm
    profiles = sketch.profiles
    mainProfile = profiles.item(0)
    extrudes = comp.features.extrudeFeatures
    extInput = extrudes.createInput(mainProfile, fusion.FeatureOperations.NewBodyFeatureOperation)
    extInput.setDistanceExtent(False, core.ValueInput.createByReal(5.0))
    extInput.isSolid = True
    chassisBody = extrudes.add(extInput)

    # Add fillet corners (5 mm radius) - get vertical edges
    filletFeatures = comp.features.filletFeatures
    filletInput = filletFeatures.createInput()
    filletInput.radius = core.ValueInput.createByReal(5.0)
    # Add all edges from the 4 vertical faces
    for faceIdx in range(4):
        face = chassisBody.faces.item(faceIdx)
        for edgeIdx in range(face.edges.count):
            edge = face.edges.item(edgeIdx)
            # Check if edge is vertical (compare Z coordinates)
            if edge.startPoint.z != edge.endPoint.z:
                filletInput.edges.add(edge)
    filletFeatures.add(filletInput)

    # Add 4 mounting holes (3 mm diameter) at 15 mm from corners
    holePositions = [
        core.Point3D.create(-135, -105, 0),  # -150+15, -120+15
        core.Point3D.create(135, -105, 0),   # 150-15, -120+15
        core.Point3D.create(135, 105, 0),     # 150-15, 120-15
        core.Point3D.create(-135, 105, 0)     # -150+15, 120-15
    ]

    for pos in holePositions:
        holeSketch = sketches.add(xyPlane)
        create_circle(holeSketch, pos, 1.5)  # 3mm diameter = 1.5mm radius
        holeProfiles = holeSketch.profiles
        holeProfile = holeProfiles.item(0)
        holeExtInput = extrudes.createInput(holeProfile, fusion.FeatureOperations.CutFeatureOperation)
        holeExtInput.setDistanceExtent(False, core.ValueInput.createByReal(20.0))  # Through all
        extrudes.add(holeExtInput)
        sketches.remove(holeSketch)

    sketches.remove(sketch)
    app.log('Chassis Base created: 300x240x5 mm with 4 mounting holes')
    return comp

# ============================================================
# STEP 2.3: MOTOR MOUNTS
# ============================================================

def create_motor_mount(x, y, name):
    """Create Motor Mount with 6mm shaft hole and 4x M3 mounting holes"""
    occurrences = rootComp.occurrences
    newOcc = occurrences.addNewComponent(core.Matrix3D.create())
    motorComp = newOcc.component
    motorComp.name = name

    sketches = motorComp.sketches
    xyPlane = motorComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Motor Mount Sketch'

    # Draw motor shaft hole (6 mm diameter = 3mm radius)
    create_circle(sketch, core.Point3D.create(0, 0, 0), 3.0)

    # 4 mounting holes (3 mm diameter = 1.5mm radius) at 15mm radius
    mountRadius = 15.0
    for i in range(4):
        angle = math.radians(45 + i * 90)
        hx = mountRadius * math.cos(angle)
        hy = mountRadius * math.sin(angle)
        create_circle(sketch, core.Point3D.create(hx, hy, 0), 1.5)

    profiles = sketch.profiles
    mainProfile = profiles.item(0)

    # Extrude and cut through
    extrudes = motorComp.features.extrudeFeatures
    extInput = extrudes.createInput(mainProfile, fusion.FeatureOperations.CutFeatureOperation)
    extInput.setDistanceExtent(False, core.ValueInput.createByReal(20.0))
    extrudes.add(extInput)

    # Position occurrence
    transform = core.Matrix3D.create()
    transform.translation = core.Vector3D.create(x, y, -10)
    newOcc.transform = transform

    sketches.remove(sketch)
    app.log(f'{name} created at ({x}, {y})')
    return motorComp

# ============================================================
# STEP 2.4: WHEEL HUBS
# ============================================================

def create_wheel_hub(x, y, name):
    """Create Wheel Hub: 65mm diameter, 20mm thick, D-shaft hole"""
    occurrences = rootComp.occurrences
    newOcc = occurrences.addNewComponent(core.Matrix3D.create())
    hubComp = newOcc.component
    hubComp.name = name

    sketches = hubComp.sketches
    xyPlane = hubComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Wheel Hub Sketch'

    # Main circle 65 mm diameter (32.5mm radius)
    create_circle(sketch, core.Point3D.create(0, 0, 0), 32.5)

    profiles = sketch.profiles
    mainProfile = profiles.item(0)

    extrudes = hubComp.features.extrudeFeatures
    extInput = extrudes.createInput(mainProfile, fusion.FeatureOperations.NewBodyFeatureOperation)
    extInput.setDistanceExtent(False, core.ValueInput.createByReal(20.0))
    extInput.isSolid = True
    extrudes.add(extInput)

    # Create shaft hole sketch on front face
    frontFace = hubComp.bRepBodies.item(0).faces.item(1)  # Front face
    shaftSketch = sketches.add(frontFace)

    # D-shaft hole with flat (6mm diameter with 5.5mm flat)
    create_circle(shaftSketch, core.Point3D.create(0, 0, 0), 3.0)  # 6mm diameter

    # Add flat side using tangent lines
    # Create line across circle to make D-shape
    p1 = shaftSketch.modelToSketchSpace(core.Point3D.create(-3.0, 2.75, 0))
    p2 = shaftSketch.modelToSketchSpace(core.Point3D.create(3.0, 2.75, 0))
    shaftSketch.sketchCurves.sketchLines.addByTwoPoints(p1, p2)

    shaftProfiles = shaftSketch.profiles
    shaftProfile = shaftProfiles.item(0)
    shaftInput = extrudes.createInput(shaftProfile, fusion.FeatureOperations.CutFeatureOperation)
    shaftInput.setDistanceExtent(False, core.ValueInput.createByReal(25.0))
    extrudes.add(shaftInput)

    # 4 mounting holes at 45 degree intervals on 25 mm radius
    mountRadius = 25.0
    for i in range(4):
        angle = math.radians(i * 90)
        hx = mountRadius * math.cos(angle)
        hy = mountRadius * math.sin(angle)
        create_circle(shaftSketch, core.Point3D.create(hx, hy, 0), 1.5)  # 3mm diameter

    # Position
    transform = core.Matrix3D.create()
    transform.translation = core.Vector3D.create(x, y, -15)
    newOcc.transform = transform

    sketches.remove(sketch)
    sketches.remove(shaftSketch)
    app.log(f'{name} created: 65mm diameter, 20mm thick')
    return hubComp

# ============================================================
# STEP 2.5: LIDAR TOWER
# ============================================================

def create_lidar_tower():
    """Create LiDAR Tower: 70mm base, 150mm height, 2 degree draft, hollow"""
    occurrences = rootComp.occurrences
    newOcc = occurrences.addNewComponent(core.Matrix3D.create())
    lidarComp = newOcc.component
    lidarComp.name = 'LiDAR Tower'

    sketches = lidarComp.sketches
    xyPlane = lidarComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'LiDAR Tower Base'

    # Base circle 70 mm diameter (35mm radius)
    create_circle(sketch, core.Point3D.create(0, 0, 0), 35.0)

    profiles = sketch.profiles
    mainProfile = profiles.item(0)

    extrudes = lidarComp.features.extrudeFeatures
    extInput = extrudes.createInput(mainProfile, fusion.FeatureOperations.NewBodyFeatureOperation)
    extInput.setDistanceExtent(False, core.ValueInput.createByReal(150.0))
    extInput.isSolid = True
    # Set taper/draft angle (2 degrees = 0.0349 radians)
    extInput.taperAngle = core.ValueInput.createByReal(math.radians(2))
    extrudes.add(extInput)

    # Apply shell (hollow)
    shellInput = lidarComp.features.shellFeatures.createInput(
        lidarComp.bRepBodies.item(0), core.ValueInput.createByReal(2.0)
    )
    shellInput.isOuterShell = True
    lidarComp.features.shellFeatures.add(shellInput)

    # Top platform (80 mm diameter, 5 mm thick)
    # Get top face of tower
    topFace = lidarComp.bRepBodies.item(0).faces.item(1)
    topSketch = sketches.add(topFace)
    topSketch.name = 'LiDAR Top Platform'
    create_circle(topSketch, core.Point3D.create(0, 0, 0), 40.0)  # 80mm diameter

    topProfiles = topSketch.profiles
    topProfile = topProfiles.item(0)
    topExtInput = extrudes.createInput(topProfile, fusion.FeatureOperations.NewBodyFeatureOperation)
    topExtInput.setDistanceExtent(False, core.ValueInput.createByReal(5.0))
    topExtInput.isSolid = True
    extrudes.add(topExtInput)

    # 4 mounting holes for LiDAR at 25mm radius
    for i in range(4):
        angle = math.radians(i * 90 + 45)
        hx = 25 * math.cos(angle)
        hy = 25 * math.sin(angle)
        create_circle(topSketch, core.Point3D.create(hx, hy, 0), 1.5)  # 3mm diameter

        # Cut holes through
        holeProfile = topSketch.profiles.item(topSketch.profiles.count - 1)
        holeInput = extrudes.createInput(holeProfile, fusion.FeatureOperations.CutFeatureOperation)
        holeInput.setDistanceExtent(False, core.ValueInput.createByReal(10.0))
        extrudes.add(holeInput)

    # Position
    transform = core.Matrix3D.create()
    transform.translation = core.Vector3D.create(0, 0, 75)
    newOcc.transform = transform

    sketches.remove(sketch)
    sketches.remove(topSketch)
    app.log('LiDAR Tower created: 70mm base, 150mm height, hollow')
    return lidarComp

# ============================================================
# STEP 2.6: TOP DOME
# ============================================================

def create_top_dome():
    """Create Top Dome: half-circle profile, 115mm radius, 80mm height"""
    occurrences = rootComp.occurrences
    newOcc = occurrences.addNewComponent(core.Matrix3D.create())
    domeComp = newOcc.component
    domeComp.name = 'Top Dome'

    sketches = domeComp.sketches
    xzPlane = domeComp.xZConstructionPlane
    sketch = sketches.add(xzPlane)
    sketch.name = 'Dome Profile'

    # Create closed half-circle profile
    # Arc from left to right via bottom point
    p1 = sketch.modelToSketchSpace(core.Point3D.create(-115, 0, 0))
    p2 = sketch.modelToSketchSpace(core.Point3D.create(0, -80, 0))  # Bottom point (negative Y in sketch)
    p3 = sketch.modelToSketchSpace(core.Point3D.create(115, 0, 0))

    # Add arc (counterclockwise from p1 to p3 through p2)
    sketch.sketchCurves.sketchArcs.addByThreePoints(p1, p2, p3)

    # Close the profile with line at top
    sketch.sketchCurves.sketchLines.addByTwoPoints(p1, p3)

    # Create center line for revolve axis
    centerLine = sketch.modelToSketchSpace(core.Point3D.create(0, 0, 0))
    axisLine = sketch.sketchCurves.sketchLines.addByTwoPoints(
        sketch.modelToSketchSpace(core.Point3D.create(0, -100, 0)),
        sketch.modelToSketchSpace(core.Point3D.create(0, 100, 0))
    )

    profiles = sketch.profiles
    revProfile = profiles.item(0)

    # Revolve to create dome
    revolves = domeComp.features.revolveFeatures
    revInput = revolves.createInput(revProfile, axisLine, fusion.FeatureOperations.NewBodyFeatureOperation)
    revInput.setAngleExtent(False, core.ValueInput.createByReal(math.pi * 2))
    revolves.add(revInput)

    # Position
    transform = core.Matrix3D.create()
    transform.translation = core.Vector3D.create(0, 0, 155)
    newOcc.transform = transform

    sketches.remove(sketch)
    app.log('Top Dome created: 115mm radius, 80mm height')
    return domeComp

# ============================================================
# STEP 2.7: CAMERA MOUNTS
# ============================================================

def create_camera_mount(size_x, size_y, x, y, z, angle, name):
    """Create Camera Mount: 25x24mm, 8mm thick, with tilt and screw holes"""
    occurrences = rootComp.occurrences
    newOcc = occurrences.addNewComponent(core.Matrix3D.create())
    camComp = newOcc.component
    camComp.name = name

    sketches = camComp.sketches
    xyPlane = camComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Camera Mount Sketch'

    # Rectangle
    create_rectangle(sketch, 0, 0, size_x, size_y)

    profiles = sketch.profiles
    mainProfile = profiles.item(0)

    extrudes = camComp.features.extrudeFeatures
    extInput = extrudes.createInput(mainProfile, fusion.FeatureOperations.NewBodyFeatureOperation)
    extInput.setDistanceExtent(False, core.ValueInput.createByReal(8.0))
    extInput.isSolid = True
    extrudes.add(extInput)

    # 2.5 mm screw holes (2 places)
    create_circle(sketch, core.Point3D.create(-5, 0, 0), 1.25)  # 2.5mm diameter
    create_circle(sketch, core.Point3D.create(5, 0, 0), 1.25)

    # Position and apply rotation
    transform = core.Matrix3D.create()
    transform.translation = core.Vector3D.create(x, y, z)

    # Apply rotation around Y axis for tilt
    rotMatrix = core.Matrix3D.create()
    rotMatrix.setRotationWithAxis(
        core.Vector3D.create(0, 1, 0),
        math.radians(angle),
        core.Point3D.create(0, 0, 0)
    )
    combined = core.Matrix3D.multiply(rotMatrix, transform)
    newOcc.transform = combined

    sketches.remove(sketch)
    app.log(f'{name} created: {size_x}x{size_y}mm, {angle}deg tilt')
    return camComp

# ============================================================
# STEP 2.8: IMU MOUNT
# ============================================================

def create_imu_mount():
    """Create IMU Mount: 20x20mm, 5mm thick, with center locating hole"""
    occurrences = rootComp.occurrences
    newOcc = occurrences.addNewComponent(core.Matrix3D.create())
    imuComp = newOcc.component
    imuComp.name = 'IMU Mount'

    sketches = imuComp.sketches
    xyPlane = imuComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'IMU Mount Sketch'

    # 20x20 mm square
    create_rectangle(sketch, 0, 0, 20.0, 20.0)

    profiles = sketch.profiles
    mainProfile = profiles.item(0)

    extrudes = imuComp.features.extrudeFeatures
    extInput = extrudes.createInput(mainProfile, fusion.FeatureOperations.NewBodyFeatureOperation)
    extInput.setDistanceExtent(False, core.ValueInput.createByReal(5.0))
    extInput.isSolid = True
    extrudes.add(extInput)

    # Center locating hole (3 mm diameter)
    create_circle(sketch, core.Point3D.create(0, 0, 0), 1.5)

    # Position
    transform = core.Matrix3D.create()
    transform.translation = core.Vector3D.create(0, 0, 5)
    newOcc.transform = transform

    sketches.remove(sketch)
    app.log('IMU Mount created: 20x20x5mm with 3mm center hole')
    return imuComp

# ============================================================
# STEP 2.9: BATTERY TRAY
# ============================================================

def create_battery_tray():
    """Create Battery Tray: 80x70x25mm, 2mm shell, XT60 and JST cutouts"""
    occurrences = rootComp.occurrences
    newOcc = occurrences.addNewComponent(core.Matrix3D.create())
    battComp = newOcc.component
    battComp.name = 'Battery Tray'

    sketches = battComp.sketches
    xyPlane = battComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Battery Tray Sketch'

    # 80x70 mm rectangle
    create_rectangle(sketch, 0, 0, 80.0, 70.0)

    profiles = sketch.profiles
    mainProfile = profiles.item(0)

    extrudes = battComp.features.extrudeFeatures
    extInput = extrudes.createInput(mainProfile, fusion.FeatureOperations.NewBodyFeatureOperation)
    extInput.setDistanceExtent(False, core.ValueInput.createByReal(25.0))
    extInput.isSolid = True
    extrudes.add(extInput)

    # Shell with 2 mm wall (hollow)
    shellInput = battComp.features.shellFeatures.createInput(
        battComp.bRepBodies.item(0), core.ValueInput.createByReal(2.0)
    )
    shellInput.isOuterShell = True
    battComp.features.shellFeatures.add(shellInput)

    # XT60 connector hole (15x10 mm) on front face
    frontFace = battComp.bRepBodies.item(0).faces.item(3)
    frontSketch = sketches.add(frontFace)
    frontSketch.name = 'XT60 Cutout'
    create_rectangle(frontSketch, 0, 0, 15.0, 10.0)

    frontProfiles = frontSketch.profiles
    frontProfile = frontProfiles.item(0)
    frontInput = extrudes.createInput(frontProfile, fusion.FeatureOperations.CutFeatureOperation)
    frontInput.setDistanceExtent(False, core.ValueInput.createByReal(10.0))
    extrudes.add(frontInput)

    # JST-XH cutout on side face
    # Get side face (assuming face 5)
    sideFace = battComp.bRepBodies.item(0).faces.item(4)
    sideSketch = sketches.add(sideFace)
    sideSketch.name = 'JST Cutout'
    create_rectangle(sideSketch, 0, 0, 8.0, 4.0)

    sideProfiles = sideSketch.profiles
    if sideProfiles.count > 0:
        sideProfile = sideProfiles.item(0)
        sideInput = extrudes.createInput(sideProfile, fusion.FeatureOperations.CutFeatureOperation)
        sideInput.setDistanceExtent(False, core.ValueInput.createByReal(5.0))
        extrudes.add(sideInput)

    # Position
    transform = core.Matrix3D.create()
    transform.translation = core.Vector3D.create(0, -20, -5)
    newOcc.transform = transform

    sketches.remove(sketch)
    sketches.remove(frontSketch)
    if sideProfiles.count > 0:
        sketches.remove(sideSketch)
    app.log('Battery Tray created: 80x70x25mm, hollow with cutouts')
    return battComp

# ============================================================
# STEP 2.10: BUMPERS
# ============================================================

def create_bumper(x, name):
    """Create Bumper: 280x30x20mm, rounded, hollow, with microswitch holes"""
    occurrences = rootComp.occurrences
    newOcc = occurrences.addNewComponent(core.Matrix3D.create())
    bumpComp = newOcc.component
    bumpComp.name = name

    sketches = bumpComp.sketches
    xyPlane = bumpComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'Bumper Sketch'

    # Rounded rectangle 280x30 mm with 10mm corner radius
    w, h = 280.0, 30.0
    r = 10.0
    w2, h2 = w/2, h/2

    # Create rounded rectangle using arcs and lines
    # Bottom edge
    p1 = sketch.modelToSketchSpace(core.Point3D.create(-w2 + r, -h2, 0))
    p2 = sketch.modelToSketchSpace(core.Point3D.create(w2 - r, -h2, 0))
    sketch.sketchCurves.sketchLines.addByTwoPoints(p1, p2)

    # Right bottom arc
    arc1 = sketch.sketchCurves.sketchArcs.addByThreePoints(
        sketch.modelToSketchSpace(core.Point3D.create(w2 - r, -h2, 0)),
        sketch.modelToSketchSpace(core.Point3D.create(w2, -h2 + r, 0)),
        sketch.modelToSketchSpace(core.Point3D.create(w2, h2 - r, 0))
    )

    # Right edge
    p3 = sketch.modelToSketchSpace(core.Point3D.create(w2, -h2 + r, 0))
    p4 = sketch.modelToSketchSpace(core.Point3D.create(w2, h2 - r, 0))

    # Top edge
    p5 = sketch.modelToSketchSpace(core.Point3D.create(w2 - r, h2, 0))
    p6 = sketch.modelToSketchSpace(core.Point3D.create(-w2 + r, h2, 0))
    sketch.sketchCurves.sketchLines.addByTwoPoints(p4, p5)

    # Top right arc
    sketch.sketchCurves.sketchArcs.addByThreePoints(
        sketch.modelToSketchSpace(core.Point3D.create(w2, h2 - r, 0)),
        sketch.modelToSketchSpace(core.Point3D.create(w2 - r, h2, 0)),
        sketch.modelToSketchSpace(core.Point3D.create(-w2 + r, h2, 0))
    )

    # Top edge line
    sketch.sketchCurves.sketchLines.addByTwoPoints(p5, p6)

    # Top left arc
    sketch.sketchCurves.sketchArcs.addByThreePoints(
        sketch.modelToSketchSpace(core.Point3D.create(-w2 + r, h2, 0)),
        sketch.modelToSketchSpace(core.Point3D.create(-w2, h2 - r, 0)),
        sketch.modelToSketchSpace(core.Point3D.create(-w2, -h2 + r, 0))
    )

    # Left edge
    sketch.sketchCurves.sketchLines.addByTwoPoints(
        sketch.modelToSketchSpace(core.Point3D.create(-w2, h2 - r, 0)),
        sketch.modelToSketchSpace(core.Point3D.create(-w2, -h2 + r, 0))
    )

    # Bottom left arc
    sketch.sketchCurves.sketchArcs.addByThreePoints(
        sketch.modelToSketchSpace(core.Point3D.create(-w2, -h2 + r, 0)),
        sketch.modelToSketchSpace(core.Point3D.create(-w2 + r, -h2, 0)),
        sketch.modelToSketchSpace(core.Point3D.create(w2 - r, -h2, 0))
    )

    # Extrude
    profiles = sketch.profiles
    if profiles.count > 0:
        mainProfile = profiles.item(0)
        extrudes = bumpComp.features.extrudeFeatures
        extInput = extrudes.createInput(mainProfile, fusion.FeatureOperations.NewBodyFeatureOperation)
        extInput.setDistanceExtent(False, core.ValueInput.createByReal(20.0))
        extInput.isSolid = True
        extrudes.add(extInput)

        # Shell with 2 mm wall
        shellInput = bumpComp.features.shellFeatures.createInput(
            bumpComp.bRepBodies.item(0), core.ValueInput.createByReal(2.0)
        )
        shellInput.isOuterShell = True
        bumpComp.features.shellFeatures.add(shellInput)

        # 2 microswitch mounting holes (3 mm) at 50mm from ends
        for hx in [-100, 100]:
            create_circle(sketch, core.Point3D.create(hx, 0, 0), 1.5)

    # Position
    transform = core.Matrix3D.create()
    transform.translation = core.Vector3D.create(x, 0, 5)
    newOcc.transform = transform

    sketches.remove(sketch)
    app.log(f'{name} created: 280x30x20mm, rounded, hollow')
    return bumpComp

# ============================================================
# STEP 2.11: ESP32 ENCLOSURE
# ============================================================

def create_esp32_enclosure():
    """Create ESP32 Enclosure: 55x30x15mm, 1.5mm shell, USB-C cutout"""
    occurrences = rootComp.occurrences
    newOcc = occurrences.addNewComponent(core.Matrix3D.create())
    espComp = newOcc.component
    espComp.name = 'ESP32 Enclosure'

    sketches = espComp.sketches
    xyPlane = espComp.xYConstructionPlane
    sketch = sketches.add(xyPlane)
    sketch.name = 'ESP32 Enclosure Sketch'

    # 55x30 mm rectangle
    create_rectangle(sketch, 0, 0, 55.0, 30.0)

    profiles = sketch.profiles
    mainProfile = profiles.item(0)

    extrudes = espComp.features.extrudeFeatures
    extInput = extrudes.createInput(mainProfile, fusion.FeatureOperations.NewBodyFeatureOperation)
    extInput.setDistanceExtent(False, core.ValueInput.createByReal(15.0))
    extInput.isSolid = True
    extrudes.add(extInput)

    # Shell with 1.5 mm wall
    shellInput = espComp.features.shellFeatures.createInput(
        espComp.bRepBodies.item(0), core.ValueInput.createByReal(1.5)
    )
    shellInput.isOuterShell = True
    espComp.features.shellFeatures.add(shellInput)

    # USB-C hole (10x5 mm) on front face
    if espComp.bRepBodies.item(0).faces.count > 3:
        frontFace = espComp.bRepBodies.item(0).faces.item(3)
        frontSketch = sketches.add(frontFace)
        frontSketch.name = 'USB-C Cutout'
        create_rectangle(frontSketch, 0, 0, 10.0, 5.0)

        frontProfiles = frontSketch.profiles
        if frontProfiles.count > 0:
            frontProfile = frontProfiles.item(0)
            frontInput = extrudes.createInput(frontProfile, fusion.FeatureOperations.CutFeatureOperation)
            frontInput.setDistanceExtent(False, core.ValueInput.createByReal(10.0))
            extrudes.add(frontInput)

        # Add ventilation slots on top face
        topFace = espComp.bRepBodies.item(0).faces.item(1)
        ventSketch = sketches.add(topFace)
        ventSketch.name = 'Ventilation'
        for i in range(4):
            vx = -15 + i * 10
            create_rectangle(ventSketch, vx, 0, 5.0, 1.0)

            ventProfiles = ventSketch.profiles
            if ventProfiles.count > 0:
                ventProfile = ventProfiles.item(ventProfiles.count - 1)
                ventInput = extrudes.createInput(ventProfile, fusion.FeatureOperations.CutFeatureOperation)
                ventInput.setDistanceExtent(False, core.ValueInput.createByReal(5.0))
                extrudes.add(ventInput)

        sketches.remove(frontSketch)
        sketches.remove(ventSketch)

    # Position
    transform = core.Matrix3D.create()
    transform.translation = core.Vector3D.create(0, 20, 5)
    newOcc.transform = transform

    sketches.remove(sketch)
    app.log('ESP32 Enclosure created: 55x30x15mm, hollow with cutouts')
    return espComp

# ============================================================
# STEP 2.13: APPLY MATERIALS
# ============================================================

def apply_appearance(body, r, g, b, alpha=255):
    """Apply a color appearance to a body"""
    try:
        # Create color
        color = core.Color.create(r, g, b, alpha)

        # Try to find existing appearance or create new one
        appearanceName = f'Advika_RGB_{r}_{g}_{b}'
        appearance = app.materials.itemByName(appearanceName)

        if not appearance:
            # Create new appearance
            appearances = app.materialLibraryPresets
            if appearances.count > 0:
                baseAppearance = appearances.item(0)
                appearance = app.materials.addCopy(baseAppearance, appearanceName)
                # Set color properties
                if appearance.properties.itemByName('Diffuse Color'):
                    appearance.properties.itemByName('Diffuse Color').value = color
                if appearance.properties.itemByName('General', 'Transparency'):
                    appearance.properties.itemByName('General', 'Transparency').value = 1 - (alpha / 255)

        if appearance:
            body.appearance = appearance
    except:
        app.log(f'Could not apply appearance to body')

# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    """Main entry point - creates all Advika 3.0 components"""
    app.log('=' * 60)
    app.log('Starting Advika 3.0 Robot Model Generation')
    app.log('=' * 60)

    try:
        # Create all components
        app.log('')
        app.log('--- Creating Chassis Base ---')
        create_chassis_base()

        app.log('')
        app.log('--- Creating Motor Mounts ---')
        create_motor_mount(-90, 70, 'Motor Mount Left')
        create_motor_mount(90, -70, 'Motor Mount Right')

        app.log('')
        app.log('--- Creating Wheel Hubs ---')
        create_wheel_hub(-90, 70, 'Wheel Hub Left')
        create_wheel_hub(90, -70, 'Wheel Hub Right')

        app.log('')
        app.log('--- Creating LiDAR Tower ---')
        create_lidar_tower()

        app.log('')
        app.log('--- Creating Top Dome ---')
        create_top_dome()

        app.log('')
        app.log('--- Creating Camera Mounts ---')
        create_camera_mount(25, 24, 140, 0, 75, 15, 'Horizon Camera Mount')
        create_camera_mount(25, 24, 120, 0, 25, -45, 'Floor Camera Mount')

        app.log('')
        app.log('--- Creating IMU Mount ---')
        create_imu_mount()

        app.log('')
        app.log('--- Creating Battery Tray ---')
        create_battery_tray()

        app.log('')
        app.log('--- Creating Bumpers ---')
        create_bumper(150, 'Front Bumper')
        create_bumper(-150, 'Rear Bumper')

        app.log('')
        app.log('--- Creating ESP32 Enclosure ---')
        create_esp32_enclosure()

        app.log('')
        app.log('=' * 60)
        app.log('Advika 3.0 Robot Model Generation Complete!')
        app.log('=' * 60)
        app.log('')
        app.log('VERIFICATION STEPS:')
        app.log('1. Check Browser tree for all component names')
        app.log('2. Verify dimensions in Properties panel (right-click → Properties)')
        app.log('3. Export STL: File → Export → select STL → High quality')
        app.log('4. See README for detailed verification checklist')

    except Exception as e:
        app.log(f'ERROR: {str(e)}')
        import traceback
        app.log(traceback.format_exc())

# Run
main()