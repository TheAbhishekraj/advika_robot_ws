import os
import shutil
import re

WS = "/home/abhishek/advika_robot_ws"
URDF_PATH = f"{WS}/src/advika_description/urdf/advika.urdf"

# 1. Update URDF
with open(URDF_PATH, "r") as f:
    urdf = f.read()

# Replace Base Link MESH setup
urdf = re.sub(
    r'<mesh filename="[^"]+" scale="[^"]+"/>',
    r'<mesh filename="package://advika_cad/meshes/advika30_base_plate.stl"/>',
    urdf
)
# Strip out the base_link collision box
urdf = re.sub(
    r'<box size="0.30 0.24 0.15"/>',
    r'<mesh filename="package://advika_cad/meshes/advika30_base_plate.stl"/>',
    urdf
)

# Left wheel (In CAD, extruded along Z, needs rotate in URDF like we did in assembly)
urdf = re.sub(
    r'link name="left_wheel".*?<geometry>\s*<cylinder radius="0.0325" length="0.03"/>\s*</geometry>',
    r'link name="left_wheel">\n    <visual><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_wheel_hub_L.stl"/></geometry><material name="black"/></visual>\n    <collision><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_wheel_hub_L.stl"/></geometry>',
    urdf, flags=re.DOTALL
)

urdf = re.sub(
    r'link name="right_wheel".*?<geometry>\s*<cylinder radius="0.0325" length="0.03"/>\s*</geometry>',
    r'link name="right_wheel">\n    <visual><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_wheel_hub_R.stl"/></geometry><material name="black"/></visual>\n    <collision><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_wheel_hub_R.stl"/></geometry>',
    urdf, flags=re.DOTALL
)

# Casters
urdf = re.sub(
    r'link name="caster_wheel".*?<geometry>\s*<sphere radius="0.015"/>\s*</geometry>',
    r'link name="caster_wheel">\n    <visual><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_caster_housing_F.stl"/></geometry><material name="grey"/></visual>\n    <collision><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_caster_housing_F.stl"/></geometry>',
    urdf, flags=re.DOTALL
)
urdf = re.sub(
    r'link name="caster_wheel_rear".*?<geometry>\s*<sphere radius="0.015"/>\s*</geometry>',
    r'link name="caster_wheel_rear">\n    <visual><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_caster_housing_R.stl"/></geometry><material name="grey"/></visual>\n    <collision><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_caster_housing_R.stl"/></geometry>',
    urdf, flags=re.DOTALL
)

# Lidar Tower 
urdf = re.sub(
    r'link name="lidar_tower".*?<geometry>\s*<cylinder radius="0.035" length="0.08"/>\s*</geometry>',
    r'link name="lidar_tower">\n    <visual><origin xyz="0 0 -0.15" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_top_cover.stl"/></geometry><material name="white"/></visual>\n    <collision><origin xyz="0 0 -0.15" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_top_cover.stl"/></geometry>',
    urdf, flags=re.DOTALL
)

# Cameras
urdf = re.sub(
    r'link name="horizon_camera_link".*?<geometry>\s*<box size="0.02 0.04 0.02"/>\s*</geometry>',
    r'link name="horizon_camera_link">\n    <visual><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_camera_mount_front.stl"/></geometry><material name="black"/></visual>\n    <collision><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_camera_mount_front.stl"/></geometry>',
    urdf, flags=re.DOTALL
)
urdf = re.sub(
    r'link name="floor_camera_link".*?<geometry>\s*<box size="0.02 0.04 0.02"/>\s*</geometry>',
    r'link name="floor_camera_link">\n    <visual><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_camera_mount_floor.stl"/></geometry><material name="black"/></visual>\n    <collision><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_camera_mount_floor.stl"/></geometry>',
    urdf, flags=re.DOTALL
)

# Insert the missing links (Mid frame, Bumpers) directly inside base_link visual so we don't break plugins
additional_meshes = """
    <visual><origin xyz="0 0 0" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_mid_frame.stl"/></geometry><material name="blue"/></visual>
    <visual><origin xyz="0.130 0 0.03" rpy="0 0 0"/><geometry><mesh filename="package://advika_cad/meshes/advika30_bumper_front.stl"/></geometry><material name="red"/></visual>
    <visual><origin xyz="-0.130 0 0.03" rpy="0 0 3.14159"/><geometry><mesh filename="package://advika_cad/meshes/advika30_bumper_rear.stl"/></geometry><material name="red"/></visual>
"""
urdf = urdf.replace('</link>', f'{additional_meshes}\n  </link>', 1)

with open(URDF_PATH, "w") as f:
    f.write(urdf)
print("Updated URDF successfully.")
