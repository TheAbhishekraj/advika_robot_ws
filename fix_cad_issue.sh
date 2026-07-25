#!/bin/bash
echo "Installing CadQuery (Python fallback for CAD generation)..."
pip3 install cadquery --break-system-packages

echo "Running CAD generation script..."
bash ~/advika_robot_ws/src/advika_cad/scripts/generate_all.sh
