# 3BHK FURNITURE SPECIFICATION

**Purpose:** Custom furniture design for Advika 3.0 indoor simulation
**World File:** `src/advika_sim/worlds/3bhk_house.world`
**Date:** 2026-07-25

---

## 1. HOUSE LAYOUT OVERVIEW

### 1.1 Room Dimensions

```
+------------------+------------------+------------------+
|                  |                  |                  |
|   BEDROOM 3      |   BEDROOM 2      |    KITCHEN       |
|   3.6m × 3.0m    |   3.6m × 3.0m    |    3.6m × 3.0m   |
|                  |                  |                  |
|                  |                  |                  |
+--------+---------+--------+---------+--------+---------+
         |        HALLWAY   |        |
         |       0.6m wide  |        |
+--------+---------+--------+---------+--------+---------+
|                  |                  |                  |
|   MASTER BEDROOM |   LIVING ROOM    |                  |
|   4.5m × 3.6m   |   6.0m × 4.5m   |                  |
|                  |                  |                  |
|                  |                  +--------+---------+
|                  |                           BATH 2
+--------+---------+--------+        (2.4m × 1.8m)
         |        BATH 1      |
         |    (2.4m × 1.8m)  |
+--------+---------+---------+

Total House: ~12m × 10m
Ceiling Height: 2.5m
```

### 1.2 Coordinate System (Gazebo)

```
Origin: (0, 0, 0) at ground center
X-axis: Positive = East
Y-axis: Positive = North
Z-axis: Positive = Up
```

---

## 2. LIVING ROOM FURNITURE

### 2.1 Sofa (3-Seater + 2-Seater)

```
Dimensions:
  - Length: 2200mm
  - Width: 900mm
  - Height: 800mm (back), 450mm (seat)
  - Seat height: 450mm

Material:
  - Frame: Plywood 15mm
  - Cushions: Foam 50mm
  - Fabric: Dark blue (0.2 0.2 0.8 1.0)

Placement: pose="-1.5 1.5 0 0 0 0"

Features:
  - 3 seater main section
  - 2 seater chaise on one end
  - Angled backrest
```

### 2.2 Coffee Table

```
Dimensions:
  - Length: 1200mm
  - Width: 600mm
  - Height: 400mm
  - Table top: 20mm glass
  - Frame: Metal tubes 25mm diameter

Material:
  - Top: Glass (transparent)
  - Frame: Black metal (0.1 0.1 0.1 1.0)

Placement: pose="-1.5 2.3 0 0 0 0"

Features:
  - Tempered glass top
  - 4 metal legs
  - Central shelf
```

### 2.3 TV Unit

```
Dimensions:
  - Length: 1800mm
  - Width: 450mm
  - Height: 1200mm
  - Shelf height: 300mm intervals

Material:
  - Body: White laminate (0.9 0.9 0.9 1.0)
  - Accent: Dark grey (0.2 0.2 0.2 1.0)

Placement: pose="-2.6 2.3 0 0 0 0"

Features:
  - 4 open shelves
  - 2 cabinets
  - Cable management holes
  - TV mount on top section
```

### 2.4 Floor Lamp

```
Dimensions:
  - Pole height: 1600mm
  - Base diameter: 300mm
  - Shade diameter: 400mm

Material:
  - Pole: Brushed nickel (0.7 0.7 0.65 1.0)
  - Shade: Fabric white (0.95 0.95 0.9 1.0)

Placement: pose="1.8 2.3 0 0 0 0"

Features:
  - Adjustable neck
  - LED bulb compatible
  - Weighted base
```

---

## 3. KITCHEN FURNITURE

### 3.1 Kitchen Counter (L-Shaped)

```
Dimensions:
  - Main section: 2400mm × 600mm × 900mm
  - Side section: 1200mm × 600mm × 900mm
  - Counter depth: 600mm
  - Counter height: 900mm

Material:
  - Cabinet: White MDF (0.9 0.9 0.9 1.0)
  - Countertop: Grey granite (0.5 0.5 0.5 1.0)

Placement: pose="2.5 -2.5 0 0 0 0"

Features:
  - 6 cabinet doors
  - 2 drawers
  - Under-mount sink (not modeled)
  - Backsplash area
```

### 3.2 Dining Table

```
Dimensions:
  - Length: 1500mm
  - Width: 900mm
  - Height: 750mm
  - Table thickness: 50mm

Material:
  - Top: Oak wood (0.6 0.4 0.2 1.0)
  - Legs: Black metal (0.15 0.15 0.15 1.0)

Placement: pose="3.0 -1.5 0 0 0 0"

Features:
  - Seats 6
  - Central leg pedestal
  - Oak wood grain texture
```

### 3.3 Dining Chairs ×4

```
Dimensions:
  - Seat height: 450mm
  - Seat: 400mm × 400mm
  - Back height: 450mm
  - Leg span: 400mm × 400mm

Material:
  - Seat: Oak wood (0.6 0.4 0.2 1.0)
  - Frame: Black metal (0.15 0.15 0.15 1.0)

Placement:
  - Chair 1: pose="3.0 -0.7 0 0 0 -1.57"
  - Chair 2: pose="3.8 -1.5 0 0 0 3.14"
  - Chair 3: pose="3.0 -2.3 0 0 0 1.57"
  - Chair 4: pose="2.2 -1.5 0 0 0 0"
```

### 3.4 Refrigerator

```
Dimensions:
  - Width: 700mm
  - Depth: 700mm
  - Height: 1800mm

Material:
  - Body: Stainless steel (0.75 0.75 0.75 1.0)
  - Handle: Chrome (0.8 0.8 0.8 1.0)

Placement: pose="3.0 -3.5 0 0 0 0"

Features:
  - French door (top freezer)
  - Water dispenser area
  - Ice maker recess
```

---

## 4. MASTER BEDROOM FURNITURE

### 4.1 Double Bed

```
Dimensions:
  - Mattress: 2000mm × 1800mm
  - Overall: 2200mm × 2000mm × 500mm (headboard 1000mm)
  - Headboard: 200mm wide × 1000mm high

Material:
  - Frame: Dark wood (0.25 0.15 0.1 1.0)
  - Mattress: White (0.95 0.95 0.95 1.0)
  - Headboard: Fabric (0.3 0.2 0.4 1.0)

Placement: pose="-2.0 3.5 0 0 0 0"

Features:
  - 2× pillows (600mm × 400mm)
  - Headboard with padding
  - 2 nightstands flanking
```

### 4.2 Nightstands ×2

```
Dimensions:
  - Width: 500mm
  - Depth: 400mm
  - Height: 600mm
  - Drawer height: 200mm

Material:
  - Body: Dark wood (0.25 0.15 0.1 1.0)
  - Top: Marble look (0.85 0.85 0.8 1.0)

Placement:
  - Left: pose="-2.9 3.5 0 0 0 0"
  - Right: pose="-1.1 3.5 0 0 0 0"

Features:
  - 2 drawers each
  - Lamp surface on top
  - Soft-close hinges
```

### 4.3 Wardrobe

```
Dimensions:
  - Width: 1800mm
  - Depth: 600mm
  - Height: 2200mm

Material:
  - Body: White laminate (0.9 0.9 0.9 1.0)
  - Handles: Gold/brass (0.7 0.6 0.2 1.0)

Placement: pose="-2.0 4.5 0 0 0 0"

Features:
  - 3 doors
  - Hanging rod
  - 3 shelves inside
  - Full height
```

---

## 5. BEDROOM 2 FURNITURE

### 5.1 Single Bed

```
Dimensions:
  - Mattress: 1900mm × 900mm
  - Overall: 2000mm × 1000mm × 400mm
  - Headboard: 150mm wide × 800mm high

Material:
  - Frame: Light oak (0.5 0.35 0.2 1.0)
  - Mattress: White (0.95 0.95 0.95 1.0)

Placement: pose="-2.0 1.2 0 0 0 0"

Features:
  - Single pillow
  - Compact headboard
```

### 5.2 Study Table

```
Dimensions:
  - Width: 1200mm
  - Depth: 600mm
  - Height: 750mm

Material:
  - Top: White laminate (0.9 0.9 0.9 1.0)
  - Legs: Metal (0.2 0.2 0.2 1.0)

Placement: pose="-1.0 0.3 0 0 0 0"

Features:
  - 2 drawers
  - CPU stand area
  - Cable hole
```

### 5.3 Bookshelf

```
Dimensions:
  - Width: 800mm
  - Depth: 300mm
  - Height: 1800mm

Material:
  - Body: Light oak (0.5 0.35 0.2 1.0)

Placement: pose="-2.8 0.0 0 0 0 1.57"

Features:
  - 5 shelves
  - Adjustable shelf heights
  - Books decoration
```

---

## 6. BEDROOM 3 FURNITURE

### 6.1 Single Bed

```
Dimensions:
  - Same as Bedroom 2

Material:
  - Same as Bedroom 2

Placement: pose="-2.0 -0.6 0 0 0 0"
```

### 6.2 Desk

```
Dimensions:
  - Width: 1400mm
  - Depth: 700mm
  - Height: 750mm

Material:
  - Top: Dark walnut (0.3 0.2 0.15 1.0)
  - Frame: Black metal (0.15 0.15 0.15 1.0)

Placement: pose="-1.0 -1.5 0 0 0 0"

Features:
  - Monitor shelf
  - Keyboard tray
  - 3 drawers
```

### 6.3 Chair

```
Dimensions:
  - Office chair style
  - Seat height: 450-550mm (adjustable)
  - 5-star base

Material:
  - Seat: Black mesh (0.1 0.1 0.1 1.0)
  - Frame: Chrome (0.8 0.8 0.8 1.0)

Placement: pose="-1.0 -2.0 0 0 0 0"
```

---

## 7. BATHROOM FIXTURES

### 7.1 Commode

```
Dimensions:
  - Toilet: 400mm × 700mm × 800mm
  - Tank: 400mm × 150mm × 400mm
  - Seat height: 400mm

Material:
  - Body: White ceramic (0.95 0.95 0.95 1.0)
  - Seat: White plastic (0.9 0.9 0.9 1.0)

Placement:
  - Bathroom 1: pose="-2.0 -1.8 0 0 0 0"
  - Bathroom 2: pose="1.5 -4.2 0 0 0 0"
```

### 7.2 Sink

```
Dimensions:
  - Basin: 550mm × 450mm
  - Depth: 200mm
  - Pedestal height: 850mm

Material:
  - Basin: White ceramic (0.95 0.95 0.95 1.0)
  - Pedestal: White ceramic

Placement:
  - Bathroom 1: pose="-2.0 -1.8 0 0 0 0"
  - Bathroom 2: pose="1.5 -4.2 0 0 0 0"
```

### 7.3 Shower Area

```
Dimensions:
  - 900mm × 900mm
  - Height: 2100mm
  - Glass walls: 6mm

Material:
  - Glass: Transparent (0.9 0.9 0.9 0.3)
  - Frame: Chrome (0.8 0.8 0.8 1.0)
  - Tray: White (0.95 0.95 0.95 1.0)

Placement:
  - Bathroom 1: pose="-1.0 -2.5 0 0 0 0"
  - Bathroom 2: pose="2.0 -4.5 0 0 0 0"
```

---

## 8. EXPORT SPECIFICATIONS

### 8.1 STL Export Settings

```
Format: Binary STL
Units: Millimeters
Mesh Deviation: 0.05mm
Normal Deviation: 0.1 deg
Aspect Ratio: Max 100:1
```

### 8.2 Gazebo Model Structure

```
model_name/
├── model.sdf          # SDF description
├── model.config       # Model metadata
├── meshes/           # STL files
│   ├── sofa.stl
│   ├── table.stl
│   └── ...
└── materials/        # Textures (optional)
    └── scripts/
    └── textures/
```

### 8.3 SDF Model Template

```xml
<?xml version="1.0"?>
<sdf version="1.6">
  <model name="sofa">
    <static>true</static>
    <pose>-1.5 1.5 0 0 0 0</pose>
    <link name="link">
      <collision name="collision">
        <geometry>
          <mesh>
            <uri>model://sofa/meshes/sofa.stl</uri>
            <scale>0.001 0.001 0.001</scale>
          </mesh>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://sofa/meshes/sofa.stl</uri>
            <scale>0.001 0.001 0.001</scale>
          </mesh>
        </geometry>
        <material>
          <ambient>0.2 0.2 0.8 1.0</ambient>
        </material>
      </visual>
    </link>
  </model>
</sdf>
```

---

## 9. PRIORITY LIST FOR CUSTOM FURNITURE

| Priority | Furniture | Reason |
|----------|-----------|--------|
| 1 | Living Room Set | Most visible in demos |
| 2 | Kitchen/Dining | Navigation testing |
| 3 | Master Bedroom | Multi-room navigation |
| 4 | Bedroom 2 & 3 | Study areas |
| 5 | Bathrooms | Small space navigation |

---

*End of 3BHK Furniture Specification*