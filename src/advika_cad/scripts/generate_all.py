#!/usr/bin/env python3
"""
══════════════════════════════════════════════════════════════════════════════
ADVIKA 3.0 — UNIFIED CAD GENERATOR SELECTOR
══════════════════════════════════════════════════════════════════════════════

Choose your CAD backend:
  [1] CadQuery    — Python-based, pip install, works on any OS (Linux/Mac/Windows)
  [2] FreeCAD     — Native FreeCAD API, generates via FreeCADCmd.exe (Windows)
  [3] BOTH        — Run CadQuery first, then FreeCAD (highest quality + backup)

Usage (Windows):
  python scripts/generate_all.py           # Interactive menu
  python scripts/generate_all.py --cadquery # CadQuery only
  python scripts/generate_all.py --freecad  # FreeCAD only
  python scripts/generate_all.py --both     # Both backends

On Windows with FreeCAD installed:
  "C:\Users\HP\AppData\Local\Programs\FreeCAD 0.21\bin\FreeCADCmd.exe" ^
    scripts/generate_all_freecad.py

══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import subprocess
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAD_ROOT   = os.path.dirname(SCRIPT_DIR)   # src/advika_cad
MESHEE_DIR  = os.path.join(CAD_ROOT, "meshes")
MESHFC_DIR  = os.path.join(CAD_ROOT, "meshes_freecad")
STEP_DIR    = os.path.join(CAD_ROOT, "step")
STEPFC_DIR  = os.path.join(CAD_ROOT, "step_freecad")

FREECAD_CMD = r"C:\Users\HP\AppData\Local\Programs\FreeCAD 0.21\bin\FreeCADCmd.exe"
FREECAD_SCRIPT = os.path.join(SCRIPT_DIR, "generate_all_freecad.py")
CADQUERY_SCRIPT = os.path.join(SCRIPT_DIR, "generate_all.py")


def check_freecad():
    """Check if FreeCADCmd.exe exists."""
    return os.path.exists(FREECAD_CMD)

def check_cadquery():
    """Check if CadQuery is importable."""
    try:
        import cadquery
        return True
    except ImportError:
        return False

def run_cadquery():
    """Run CadQuery generator (works on any OS with pip)."""
    print("\n" + "="*60)
    print("Running CadQuery backend...")
    print("="*60)

    os.makedirs(MESHEE_DIR, exist_ok=True)
    os.makedirs(STEP_DIR, exist_ok=True)

    result = subprocess.run(
        [sys.executable, CADQUERY_SCRIPT],
        cwd=CAD_ROOT,
        capture_output=False
    )
    return result.returncode == 0

def run_freecad():
    """Run FreeCAD headless generator (Windows only)."""
    print("\n" + "="*60)
    print("Running FreeCAD backend...")
    print("="*60)

    if not os.path.exists(FREECAD_CMD):
        print(f"ERROR: FreeCADCmd.exe not found at:\n  {FREECAD_CMD}")
        print("\nInstall FreeCAD from: https://freecad.org/download.php")
        return False

    os.makedirs(MESHFC_DIR, exist_ok=True)
    os.makedirs(STEPFC_DIR, exist_ok=True)

    result = subprocess.run(
        [FREECAD_CMD, FREECAD_SCRIPT],
        cwd=CAD_ROOT,
        capture_output=False
    )
    return result.returncode == 0

def interactive_menu():
    """Show interactive selection menu."""
    freecad_ok = check_freecad()
    cq_ok      = check_cadquery()

    print("\n" + "═"*60)
    print(" ADVIKA 3.0 — CAD BACKEND SELECTOR")
    print("═"*60)
    print(f"  [1] CadQuery    — {'Available' if cq_ok else 'NOT installed (pip install cadquery)'}")
    print(f"  [2] FreeCAD     — {'Available' if freecad_ok else 'NOT installed (install FreeCAD 0.21)'}")
    print(f"  [3] BOTH        — Run CadQuery, then FreeCAD (recommended)")
    print(f"  [4] Show stats  — List existing STLs")
    print(f"  [5] Quit")
    print("─"*60)

    choice = input("Select backend [1-5]: ").strip()

    if choice == "1":
        if not cq_ok:
            print("CadQuery not found. Install: pip install cadquery")
            return False
        return run_cadquery()

    elif choice == "2":
        if not freecad_ok:
            print("FreeCAD not found. Install from: https://freecad.org")
            return False
        return run_freecad()

    elif choice == "3":
        ok1 = run_cadquery() if cq_ok else False
        ok2 = run_freecad() if freecad_ok else False
        if not cq_ok:   print("CadQuery skipped (not available)")
        if not freecad_ok: print("FreeCAD skipped (not available)")
        return ok1 or ok2

    elif choice == "4":
        show_stats()
        return False

    elif choice == "5":
        print("Exiting.")
        return False

    else:
        print("Invalid choice.")
        return False


def show_stats():
    """Show existing STL files in both directories."""
    print("\n── CadQuery meshes ──")
    if os.path.exists(MESHEE_DIR):
        files = [f for f in os.listdir(MESHEE_DIR) if f.endswith(".stl")]
        print(f"  {len(files)} files in {MESHEE_DIR}")
        for f in sorted(files):
            sz = os.path.getsize(os.path.join(MESHEE_DIR, f)) // 1024
            print(f"    {f}  ({sz} KB)")
    else:
        print("  Directory does not exist (run CadQuery first)")

    print("\n── FreeCAD meshes ──")
    if os.path.exists(MESHFC_DIR):
        files = [f for f in os.listdir(MESHFC_DIR) if f.endswith(".stl")]
        print(f"  {len(files)} files in {MESHFC_DIR}")
        for f in sorted(files):
            sz = os.path.getsize(os.path.join(MESHFC_DIR, f)) // 1024
            print(f"    {f}  ({sz} KB)")
    else:
        print("  Directory does not exist (run FreeCAD first)")

    print("\n── STEP files (CadQuery) ──")
    if os.path.exists(STEP_DIR):
        files = [f for f in os.listdir(STEP_DIR) if f.endswith(".step")]
        print(f"  {len(files)} files in {STEP_DIR}")
    else:
        print("  None")


def main():
    parser = argparse.ArgumentParser(description="Advika 3.0 CAD Generator Selector")
    parser.add_argument("--cadquery", action="store_true", help="Run CadQuery only")
    parser.add_argument("--freecad",  action="store_true", help="Run FreeCAD only")
    parser.add_argument("--both",     action="store_true", help="Run both backends")
    parser.add_argument("--stats",    action="store_true", help="Show existing STL stats")
    args = parser.parse_args()

    if args.stats:
        show_stats()
        return

    if args.cadquery:
        ok = check_cadquery()
        if not ok:
            print("CadQuery not installed. Run: pip install cadquery")
            sys.exit(1)
        success = run_cadquery()
    elif args.freecad:
        success = run_freecad()
    elif args.both:
        success = True
        if check_cadquery():
            success = run_cadquery() and success
        else:
            print("CadQuery not available, skipping.")
        if check_freecad():
            success = run_freecad() and success
        else:
            print("FreeCAD not available, skipping.")
    else:
        success = interactive_menu()

    if success:
        show_stats()
        print("\nCAD generation complete!")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()