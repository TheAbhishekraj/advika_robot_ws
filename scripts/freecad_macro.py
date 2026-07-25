import FreeCAD as App
import FreeCADGui as Gui
import Part
import Mesh
import os

# Create or get active document
doc = App.ActiveDocument
if not doc:
    doc = App.newDocument("Advika30_Render")

print("Importing STLs and applying showroom colors...")
colors = {
    "advika30_base_plate": (0.10, 0.23, 0.36),
    "advika30_mid_frame": (0.17, 0.36, 0.52),
    "advika30_top_cover": (0.94, 0.94, 0.94),
    "advika30_motor_mount_L": (0.50, 0.50, 0.50),
    "advika30_motor_mount_R": (0.50, 0.50, 0.50),
    "advika30_wheel_hub_L": (0.10, 0.10, 0.10),
    "advika30_wheel_hub_R": (0.10, 0.10, 0.10),
    "advika30_caster_housing_F": (0.75, 0.75, 0.75),
    "advika30_caster_housing_R": (0.75, 0.75, 0.75),
    "advika30_bumper_front": (0.90, 0.22, 0.27),
    "advika30_bumper_rear": (0.90, 0.22, 0.27),
    "advika30_camera_mount_front": (0.10, 0.10, 0.10),
    "advika30_camera_mount_floor": (0.10, 0.10, 0.10),
    "advika30_battery_retainer": (1.0, 0.55, 0.0),
    "advika30_gasket_top": (0.25, 0.25, 0.25),
    "advika30_gasket_pi": (0.25, 0.25, 0.25),
    "advika30_gasket_motor": (0.25, 0.25, 0.25),
}

mesh_dir = "/home/abhishek/advika_robot_ws/src/advika_cad/meshes"

for obj_name, rgb in colors.items():
    stl_path = os.path.join(mesh_dir, f"{obj_name}.stl")
    if os.path.exists(stl_path):
        # Insert STL into FreeCAD
        Mesh.insert(stl_path, doc.Name)
        
        # FreeCAD names the object exactly as the STL filename without extension
        obj = doc.getObject(obj_name)
        if obj:
            obj.ViewObject.ShapeColor = rgb
            if obj_name == "advika30_top_cover":
                obj.ViewObject.Transparency = 60
    else:
        print(f"Warning: {stl_path} not found.")

# PART 2: ADD ELECTRONICS (Pi & ESP)
print("Adding electronics modules...")
try:
    pi = doc.addObject("Part::Box", "raspberry_pi")
    pi.Length, pi.Width, pi.Height = 85, 56, 20
    # Pi goes mounted over the base plate, shifted slightly
    pi.Placement = App.Placement(App.Vector(-42.5, -28, 5), App.Rotation())
    pi.ViewObject.ShapeColor = (0.0, 0.5, 0.0)

    esp32 = doc.addObject("Part::Box", "esp32_s3")
    esp32.Length, esp32.Width, esp32.Height = 55, 30, 15
    # ESP32 positioned behind Pi
    esp32.Placement = App.Placement(App.Vector(-27.5, 35, 5), App.Rotation())
    esp32.ViewObject.ShapeColor = (0.0, 0.2, 0.8)
except Exception as e:
    print(f"Could not add electronics: {e}")

# RECOMPUTE AND FIT
doc.recompute()
Gui.SendMsgToActiveView("ViewFit")

print("=====================================")
print("✅ NATIVE STL ASSEMBLY PERFECTED!")
print(f"Total components loaded: {len(doc.Objects)}")
print("=====================================")
