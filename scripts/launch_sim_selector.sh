#!/bin/bash
# Advika 3.0 — Simulation Selector Launcher

echo "=============================================="
echo "ADVIKA 3.0 — SIMULATION SELECTOR"
echo "=============================================="

cd ~/advika_robot_ws
source install/setup.bash

# Generate alternative models if they don't exist
ALT_DIR="src/advika_description/urdf/alternative"
if [ ! -f $ALT_DIR/advika_heavy.urdf ]; then
    echo "🔧 Generating Advika Heavy and Light URDF variations..."
    mkdir -p $ALT_DIR
    sed 's/<mass value="2.0"\/>/<mass value="3.0"\/>/g' src/advika_description/urdf/advika.urdf > $ALT_DIR/advika_heavy.urdf
    sed 's/<mass value="2.0"\/>/<mass value="1.0"\/>/g' src/advika_description/urdf/advika.urdf > $ALT_DIR/advika_light.urdf
fi

# Reorganize world files into expected subsystem directories if needed
if [ -f src/advika_sim/worlds/3bhk_house.world ]; then
    echo "Reorganizing 3BHK world into its subfolder..."
    mkdir -p src/advika_sim/worlds/3bhk_house
    mv src/advika_sim/worlds/3bhk_house.world src/advika_sim/worlds/3bhk_house/
fi

# Check if selector config exists
if [ ! -f ~/.advika_config/selector_config.yaml ]; then
    echo "⚠️  First time running. Creating default config..."
    mkdir -p ~/.advika_config
    echo "last_world: 3bhk_house" > ~/.advika_config/selector_config.yaml
    echo "last_model: advika" >> ~/.advika_config/selector_config.yaml
fi

# Launch selector
ros2 launch advika_sim simulator_selector.launch.py

echo "=============================================="
echo "Simulation ended."
echo "=============================================="
