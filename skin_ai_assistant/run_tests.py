#!/usr/bin/env python3
"""
Cross-platform test runner for Skin AI Assistant.
Automatically sets up environment variables for dynamic port mapping.
"""
import os
import sys
import subprocess


def main():
    print("=" * 70)
    print("Running Skin AI Assistant Tests (pytest)")
    print("=" * 70)
    print()

    # Set up test environment with dynamic ports
    print("Setting up test environment with dynamic ports...")
    os.environ["BACKEND_PORT"] = os.getenv("BACKEND_PORT", "8000")
    os.environ["SKINAI_API_URL"] = f"http://127.0.0.1:{os.environ['BACKEND_PORT']}"

    print(f"Backend Port: {os.environ['BACKEND_PORT']}")
    print(f"API URL: {os.environ['SKINAI_API_URL']}")
    print()

    # Run pytest
    print("Running pytest...")
    print("-" * 70)
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests", "-vv", "--tb=short"],
        cwd=os.path.dirname(__file__)
    )

    print()
    if result.returncode == 0:
        print("[PASS] All tests passed!")
    else:
        print(f"[FAIL] Some tests failed. Exit code: {result.returncode}")

    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
