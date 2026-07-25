#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# ADVIKA 3.0 — CAD GENERATION RUNNER
# ═══════════════════════════════════════════════════════════════════
# Generates all 20 STL + STEP CAD files using CadQuery (Python).
#
# Usage:
#   bash src/advika_cad/scripts/generate_all.sh
#
# Prerequisites:
#   pip install cadquery   (or: conda install -c conda-forge cadquery)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CAD_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=============================================="
echo "ADVIKA 3.0 — CAD MODEL GENERATOR"
echo "=============================================="
echo ""
echo "📁 CAD Root:  $CAD_ROOT"
echo "📁 Meshes:    $CAD_ROOT/meshes/"
echo "📁 STEP:      $CAD_ROOT/step/"
echo ""

# Create output directories
mkdir -p "$CAD_ROOT/meshes" "$CAD_ROOT/step" "$CAD_ROOT/fcstd"

# Check if CadQuery is available
if python3 -c "import cadquery" &>/dev/null; then
    echo "🔧 Using CadQuery backend..."
    python3 "$SCRIPT_DIR/generate_all.py"
else
    echo "❌ CadQuery not found. Installing now..."
    echo ""
    # Try pip install (works in conda base env)
    pip install cadquery 2>/dev/null || pip install cadquery --break-system-packages 2>/dev/null
    
    if python3 -c "import cadquery" &>/dev/null; then
        echo "✅ CadQuery installed successfully!"
        python3 "$SCRIPT_DIR/generate_all.py"
    else
        echo "❌ CadQuery installation failed."
        echo ""
        echo "Please install manually:"
        echo "  conda install -c conda-forge cadquery"
        echo "  OR: pip install cadquery"
        exit 1
    fi
fi

echo ""
echo "=============================================="
STL_COUNT=$(find "$CAD_ROOT/meshes" -name "*.stl" 2>/dev/null | wc -l)
STEP_COUNT=$(find "$CAD_ROOT/step" -name "*.step" 2>/dev/null | wc -l)
echo "✅ Generated: $STL_COUNT STL files, $STEP_COUNT STEP files"
echo "📁 STL output:  $CAD_ROOT/meshes/"
echo "📁 STEP output: $CAD_ROOT/step/"
echo "=============================================="
