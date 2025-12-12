#!/usr/bin/env python3
"""
Verify that all required backend files are in place
"""

import os
from pathlib import Path

print("")
print("=" * 50)
print("VERIFYING PROJECT SETUP")
print("=" * 50)
print("")

project_root = Path.cwd()
print(f"Project root: {project_root}")
print("")

# Files that must exist
required_files = [
    "backend/main.py",
    "backend/requirements.txt",
    "backend/db_helper.py",
    "backend/app/__init__.py",
    "backend/app/models.py",
    "backend/app/routes/__init__.py",
    "backend/app/routes/clients.py",
    "backend/app/routes/timesheet.py",
    "backend/app/routes/invoices.py"
]

print("Checking required files...")
print("")

all_good = True
for file_path in required_files:
    full_path = project_root / file_path
    if full_path.exists():
        print(f"  ✓ {file_path}")
    else:
        print(f"  ✗ MISSING: {file_path}")
        all_good = False

print("")
if all_good:
    print("=" * 50)
    print("✓ ALL FILES PRESENT!")
    print("=" * 50)
    print("")
    print("Next steps:")
    print("1. cd backend")
    print("2. pip install -r requirements.txt")
    print("3. python main.py")
    print("")
else:
    print("=" * 50)
    print("✗ SOME FILES MISSING")
    print("=" * 50)
    print("")
    print("Download missing files from outputs and place them")
    print("in the correct directories as shown above.")
    print("")
