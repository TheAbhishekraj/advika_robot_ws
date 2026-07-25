# ADVIKA 3.0 — MESH EXPORT GUIDE (STL → DAE → URDF)

**Version:** 1.0 | **Date:** 2026-07-25

---

## 📋 Overview

This guide covers converting FreeCAD/CadQuery STL meshes to Gazebo-compatible DAE (Collada) format and integrating them into the Advika URDF robot description.

```
FreeCAD (.FCStd)  →  STL (.stl)  →  DAE (.dae)  →  URDF <mesh>
     ↓                  ↓              ↓
  Parametric         3D Print      Gazebo Sim
```

---

## Step 1: Generate STL Files

```bash
# Run the generation script
bash ~/advika_robot_ws/src/advika_cad/scripts/generate_all.sh

# Output: src/advika_cad/meshes/advika30_*.stl
```

---

## Step 2: Convert STL → DAE (Collada)

### Option A: Using Blender (Recommended)

```bash
# Install Blender
sudo apt install blender

# Batch convert all STL to DAE
cd ~/advika_robot_ws/src/advika_cad/meshes

for stl in advika30_*.stl; do
    dae="${stl%.stl}.dae"
    blender --background --python-expr "
import bpy
bpy.ops.wm.read_homefile(use_empty=True)
bpy.ops.import_mesh.stl(filepath='$(pwd)/$stl')
bpy.ops.wm.collada_export(filepath='$(pwd)/$dae')
" 2>/dev/null
    echo "✅ $stl → $dae"
done
```

### Option B: Using MeshLab

```bash
# Install MeshLab
sudo apt install meshlab

# Convert single file
meshlabserver -i input.stl -o output.dae
```

### Option C: Using ctmconv (lightweight)

```bash
pip install trimesh
python3 -c "
import trimesh, glob, os
for stl in glob.glob('*.stl'):
    mesh = trimesh.load(stl)
    dae = stl.replace('.stl', '.dae')
    mesh.export(dae, file_type='collada')
    print(f'✅ {stl} → {dae}')
"
```

---

## Step 3: Organize Mesh Files

```bash
# Create meshes directory in advika_description
mkdir -p ~/advika_robot_ws/src/advika_description/meshes/visual
mkdir -p ~/advika_robot_ws/src/advika_description/meshes/collision

# Copy visual meshes (DAE — textured, detailed)
cp ~/advika_robot_ws/src/advika_cad/meshes/*.dae \
   ~/advika_robot_ws/src/advika_description/meshes/visual/

# Copy collision meshes (STL — simplified, faster physics)
cp ~/advika_robot_ws/src/advika_cad/meshes/*.stl \
   ~/advika_robot_ws/src/advika_description/meshes/collision/
```

---

## Step 4: Update URDF with Mesh References

Replace primitive geometry `<box>` / `<cylinder>` with `<mesh>` tags:

### Before (primitive geometry):
```xml
<link name="base_link">
  <visual>
    <geometry>
      <box size="0.300 0.240 0.005"/>
    </geometry>
    <material name="blue">
      <color rgba="0.1 0.3 0.8 1.0"/>
    </material>
  </visual>
  <collision>
    <geometry>
      <box size="0.300 0.240 0.005"/>
    </geometry>
  </collision>
</link>
```

### After (mesh geometry):
```xml
<link name="base_link">
  <visual>
    <geometry>
      <mesh filename="package://advika_description/meshes/visual/advika30_base_plate.dae"
            scale="0.001 0.001 0.001"/>
    </geometry>
  </visual>
  <collision>
    <geometry>
      <mesh filename="package://advika_description/meshes/collision/advika30_base_plate.stl"
            scale="0.001 0.001 0.001"/>
    </geometry>
  </collision>
</link>
```

> **Important:** STL/DAE files are in **millimeters**. URDF expects **meters**.
> Use `scale="0.001 0.001 0.001"` to convert mm → m.

---

## Step 5: Mesh-to-Link Mapping

| URDF Link | Visual Mesh (DAE) | Collision Mesh (STL) |
|-----------|-------------------|----------------------|
| `base_link` | `advika30_base_plate.dae` | `advika30_base_plate.stl` |
| `mid_frame_link` | `advika30_mid_frame.dae` | `advika30_mid_frame.stl` |
| `top_cover_link` | `advika30_top_cover.dae` | `advika30_top_cover.stl` |
| `left_wheel_link` | `advika30_wheel_hub_L.dae` | `advika30_wheel_hub_L.stl` |
| `right_wheel_link` | `advika30_wheel_hub_R.dae` | `advika30_wheel_hub_R.stl` |
| `lidar_link` | (sensor only — no CAD mesh) | — |
| `horizon_camera_link` | `advika30_camera_mount_front.dae` | `advika30_camera_mount_front.stl` |
| `floor_camera_link` | `advika30_camera_mount_floor.dae` | `advika30_camera_mount_floor.stl` |
| `bumper_front_link` | `advika30_bumper_front.dae` | `advika30_bumper_front.stl` |
| `bumper_rear_link` | `advika30_bumper_rear.dae` | `advika30_bumper_rear.stl` |

---

## Step 6: Verify in Gazebo

```bash
# Rebuild workspace
cd ~/advika_robot_ws
colcon build --packages-select advika_description advika_sim
source install/setup.bash

# Launch simulation
ros2 launch advika_sim sim_bringup.launch.py

# Verify: robot model uses CAD meshes (not primitive boxes)
```

---

## ⚠️ Common Issues

| Problem | Solution |
|---------|----------|
| Mesh not visible in Gazebo | Check `package://` path and `scale` attribute |
| Mesh upside down | Adjust URDF `<origin rpy=.../>` inside `<visual>` |
| Mesh offset from joint | Adjust `<origin xyz=.../>` inside `<visual>` |
| Collision too detailed (slow) | Use simplified STL for `<collision>`, detailed DAE for `<visual>` |
| Model explodes in simulation | Ensure inertial properties match new geometry |