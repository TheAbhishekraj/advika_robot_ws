#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# ADVIKA 3.0 — INSTALL CADQUERY + GENERATE ALL CAD FILES
# ═══════════════════════════════════════════════════════════════════
# One-command script: installs CadQuery if missing, then generates
# all 20 STL + STEP CAD files.
#
# Usage:
#   bash ~/advika_robot_ws/src/advika_cad/scripts/install_and_generate.sh

set -e

echo "=============================================="
echo "ADVIKA 3.0 — CAD SETUP & GENERATION"
echo "=============================================="
echo ""

# Step 1: Check if CadQuery is already installed
if python3 -c "import cadquery" &>/dev/null; then
    echo "✅ CadQuery already installed"
else
    echo "📦 Installing CadQuery..."
    echo ""

    # Try conda first (user has conda base active)
    if command -v conda &>/dev/null; then
        echo "  Using conda..."
        conda install -y -c conda-forge -c cadquery cadquery 2>/dev/null && echo "  ✅ Installed via conda" || {
            echo "  ⚠️  conda install failed, trying pip..."
            pip install cadquery 2>/dev/null || pip install cadquery --break-system-packages 2>/dev/null
        }
    else
        echo "  Using pip..."
        pip install cadquery 2>/dev/null || pip install cadquery --break-system-packages 2>/dev/null
    fi

    # Verify
    if python3 -c "import cadquery" &>/dev/null; then
        echo "  ✅ CadQuery installed successfully!"
    else
        echo "  ❌ CadQuery installation failed."
        echo ""
        echo "  Try manually:"
        echo "    conda install -c conda-forge -c cadquery cadquery"
        echo "    OR: pip install cadquery"
        exit 1
    fi
fi

echo ""

# Step 2: Run the generation script
echo "🔧 Generating CAD models..."
bash "$(dirname "$0")/generate_all.sh"
