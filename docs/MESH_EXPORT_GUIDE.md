# MESH EXPORT GUIDE

**Purpose:** Export STL/DAE meshes from Fusion 360 and integrate into URDF
**Platform:** Windows with Fusion 360
**Date:** 2026-07-25

---

## 1. STL EXPORT FROM FUSION 360

### 1.1 Single Part Export

```
1. Open component in Fusion 360
2. Right-click body in browser → "Save as STL"
3. Or: File → Export → STL

STL Settings:
├── Units: Millimeters
├── Resolution: High (0.01mm)
└── Output: Binary STL

Save location:
src/advika_cad/meshes/{Component}_v{n}_{date}.stl
```

### 1.2 Full Assembly Export

```
1. Open assembly
2. Activate top-level assembly
3. File → Export → STL
4. Select "All components as single file"
5. Or "Each component as separate file"

For single file:
└── advika_full_robot_v1_20260725.stl

For multiple files:
├── Chassis_Base_v3.stl
├── Wheel_Hub_Left_v1.stl
├── Wheel_Hub_Right_v1.stl
├── LiDAR_Tower_v2.stl
└── ...
```

### 1.3 STL Quality Settings

```
High Quality (Recommended for 3D Printing):
├── Surface Deviation: 0.01 mm
├── Normal Deviation: 0.05 deg
└── Maximum Aspect Ratio: 100:1

Standard Quality (for URDF visualization):
├── Surface Deviation: 0.05 mm
├── Normal Deviation: 0.1 deg
└── Maximum Aspect Ratio: 50:1

Fast Preview (for testing):
├── Surface Deviation: 0.1 mm
├── Normal Deviation: 0.5 deg
└── Maximum Aspect Ratio: 20:1
```

---

## 2. STEP FILE EXPORT

### 2.1 Single Part STEP

```
1. Open component
2. File → Export → STEP
3. Settings:
   ├── Format: STEP
   ├── Units: Millimeters
   ├── Scheme: AP214 (automotive)
   └── Include: Active component only
```

### 2.2 Assembly STEP

```
1. Open assembly
2. File → Export → STEP
3. Settings:
   ├── Format: STEP
   ├── Units: Millimeters
   ├── Scheme: AP214
   └── Include: All components as:
       - Single compound (for vendor)
       - Multiple files (for collaboration)

Output naming:
├── Advika_Chassis_Assembly_v3.step
├── Advika_Sensor_Module_v2.step
└── Advika_Full_Robot_v1.step
```

---

## 3. CONVERT STL TO DAE FOR GAZEBO

### 3.1 Using Blender (Recommended)

Blender has better material support for Gazebo.

```
1. Open Blender
2. File → Import → STL
3. Select your STL file
4. Fix normals: Select mesh → Mesh → Normals → Recalculate Outside
5. File → Export → Collada DAE
6. Settings:
   ├── Include: Selected Objects
   ├── Transformation: Apply Transform
   └── Apply Scale: FBX All
7. Save as {component}.dae
```

### 3.2 Using MeshLab

```
1. Open MeshLab
2. File → Import Mesh
3. Filters → Normals, Curvatures and Orientation → Compute normals
4. File → Export Mesh As → DAE
```

### 3.3 Using CloudCompare

```
1. Open CloudCompare
2. File → Open → Select STL
3. Edit → Merge
4. File → Export → Collada (DAE)
```

---

## 4. URDF MESH INTEGRATION

### 4.1 Directory Structure

```
src/advika_cad/
├── meshes/
│   ├── base_link.stl
│   ├── chassis_v3.stl
│   ├── wheel_hub_left.stl
│   └── ...
├── step/
│   └── assembly.step
└── advika_cad/
    └── __init__.py

simulation/urdf/
├── advika.urdf
└── meshes/
    └── base_link.stl  (copy of advika_cad/meshes/)
```

### 4.2 Package.xml Configuration

Add to `src/advika_cad/package.xml`:

```xml
<export>
  <build_type>ament_python</build_type>
  <exec_depend>rviz_common</exec_depend>
  <exec_depend>robot_state_publisher</exec_depend>
</export>
```

### 4.3 Update URDF Visual

```xml
<!-- Before (primitive geometry) -->
<link name="base_link">
  <visual>
    <origin xyz="0 0 0.075" rpy="0 0 0"/>
    <geometry>
      <box size="0.30 0.24 0.15"/>
    </geometry>
    <material name="blue"/>
  </visual>
</link>

<!-- After (mesh geometry) -->
<link name="base_link">
  <visual>
    <origin xyz="0 0 0.075" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://advika_cad/meshes/chassis_v3.stl"/>
    </geometry>
    <material name="blue"/>
  </visual>
</link>
```

### 4.4 Update URDF Collision

```xml
<link name="base_link">
  <collision>
    <origin xyz="0 0 0.075" rpy="0 0 0"/>
    <geometry>
      <mesh filename="package://advika_cad/meshes/chassis_v3.stl"/>
    </geometry>
  </collision>
</link>
```

### 4.5 Launch File Configuration

Ensure the URDF package is properly sourced in your launch file:

```python
# In sim_bringup.launch.py
def generate_launch_description():
    # Use package share directory for mesh paths
    advika_cad_dir = get_package_share_directory('advika_cad')
    chassis_mesh = os.path.join(advika_cad_dir, 'meshes', 'chassis_v3.stl')

    # Or use 'package://' URI directly in URDF
    # package://advika_cad/meshes/chassis_v3.stl
```

---

## 5. GAZEBO VISUAL MATERIALS

### 5.1 Simple Color Material

```xml
<link name="base_link">
  <visual>
    <geometry>
      <mesh filename="package://advika_cad/meshes/chassis_v3.stl"/>
    </geometry>
    <material>
      <ambient>0.1 0.3 0.8 1.0</ambient>  <!-- RGB + Alpha -->
      <diffuse>0.1 0.3 0.8 1.0</diffuse>
      <specular>0.05 0.05 0.05 1.0</specular>
      <emissive>0 0 0 0</emissive>
    </material>
  </visual>
</link>
```

### 5.2 Gazebo Material Tag

```xml
<gazebo reference="base_link">
  <material>Gazebo/Blue</material>
  <!-- Or custom material from Gazebo library -->
  <mu1>0.5</mu1>
  <mu2>0.5</mu2>
</gazebo>
```

### 5.3 Transparent Material

```xml
<link name="top_dome">
  <visual>
    <geometry>
      <mesh filename="package://advika_cad/meshes/dome_v1.stl"/>
    </geometry>
    <material>
      <ambient>0.9 0.9 0.9 0.3</ambient>  <!-- Alpha = 0.3 -->
      <diffuse>0.9 0.9 0.9 0.3</diffuse>
    </material>
  </visual>
</link>
```

---

## 6. COMMON ISSUES & FIXES

### 6.1 Mesh Not Found

```
Error: "[Err] [MeshManager.cc:XXX] Unable to find file"

Solution:
1. Verify path: package://advika_cad/meshes/file.stl
2. Check file exists in src/advika_cad/meshes/
3. Rebuild package: colcon build --packages-select advika_cad
4. Source setup.bash: source install/setup.bash
```

### 6.2 Mesh Scale Issues

```
Error: Mesh appears tiny or huge in Gazebo

Solution:
1. Fusion 360 exports in mm by default
2. Gazebo URDF may need scale adjustment:
   <mesh filename="..." scale="0.001 0.001 0.001"/>
3. Or resize in Fusion 360 before export
```

### 6.3 Inverted Normals

```
Error: Mesh appears black/hole-filled in Gazebo

Solution:
1. Fix in Blender:
   - Import STL
   - Select mesh
   - Mesh → Normals → Recalculate Outside
   - Flip normals if needed
   - Export as DAE
```

### 6.4 Non-Manifold Mesh

```
Error: "Mesh is not valid for collision"

Solution:
1. Repair in MeshLab:
   - Filters → Remeshing → Quadratic Edge Collapse
   - Or: Filters → Mesh Layer → Remove Duplicate Faces
2. Repair in Blender:
   - Edit Mode → Select All
   - Mesh → Clean Up → Make Manifold
3. Use netfabb service (online repair)
```

---

## 7. BATCH CONVERSION SCRIPT

Create `scripts/convert_meshes.py`:

```python
#!/usr/bin/env python3
"""Convert STL to DAE for Gazebo integration."""

import os
import subprocess
import sys

def convert_stl_to_dae(stl_path, dae_path):
    """Convert STL to DAE using Blender headless."""
    blender_script = f"""
import bpy
bpy.ops.import_mesh.stl(filepath='{stl_path}')
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
bpy.ops.export_anim.dae(filepath='{dae_path}', export_eval={1})
"""
    subprocess.run([
        'blender',
        '--background',
        '--python-expr', blender_script
    ])

def main():
    meshes_dir = 'src/advika_cad/meshes'
    for stl_file in os.listdir(meshes_dir):
        if stl_file.endswith('.stl'):
            stl_path = os.path.join(meshes_dir, stl_file)
            dae_file = stl_file.replace('.stl', '.dae')
            dae_path = os.path.join(meshes_dir, dae_file)
            print(f"Converting {stl_file} -> {dae_file}")
            convert_stl_to_dae(stl_path, dae_path)

if __name__ == '__main__':
    main()
```

---

## 8. VERIFICATION CHECKLIST

- [ ] STL files export successfully from Fusion 360
- [ ] Mesh dimensions match original design (measure in mm)
- [ ] STL files copied to `src/advika_cad/meshes/`
- [ ] URDF updated with `package://` mesh paths
- [ ] Launch file sources `advika_cad` package
- [ ] Gazebo displays mesh correctly
- [ ] No console errors about missing meshes
- [ ] Collision geometry matches visual mesh
- [ ] Normals are correct (not inverted)

---

## 9. QUICK REFERENCE

| Task | Tool | Command/Steps |
|------|------|---------------|
| Export STL | Fusion 360 | File → Export → STL |
| Export STEP | Fusion 360 | File → Export → STEP |
| STL → DAE | Blender | Import STL, Export DAE |
| Verify mesh | MeshLab | File → Import → check errors |
| Test in URDF | Terminal | ros2 launch advika_sim sim_bringup.launch.py |
| Fix normals | Blender | Mesh → Normals → Recalculate Outside |

---

*End of Mesh Export Guide*