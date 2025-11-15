#!/usr/bin/env python3
"""
Root-level test runner for Skin AI Assistant.
Delegates to the actual run_tests.py in the skin_ai_assistant subdirectory.
"""
import os
import sys
from pathlib import Path

# Add the skin_ai_assistant directory to the path
project_root = Path(__file__).parent
skin_ai_dir = project_root / "skin_ai_assistant"
sys.path.insert(0, str(skin_ai_dir))

# Change to the skin_ai_assistant directory
os.chdir(skin_ai_dir)

# Import and run the test runner
import subprocess

result = subprocess.run([sys.executable, "run_tests.py"])
sys.exit(result.returncode)
