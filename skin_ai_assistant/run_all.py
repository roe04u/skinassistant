#!/usr/bin/env python3
"""
Unified launcher for all Skin AI Assistant services with dynamic port mapping.
Launches backend, UI, and admin dashboard in separate processes.
All ports are dynamically allocated from any available free ports.
"""
import os
import sys
import subprocess
import time
from pathlib import Path
from utils.port_utils import get_multiple_free_ports, get_free_port


def main():
    # Find 3 free ports for all services dynamically from wide range
    print(">> Scanning for available free ports...")
    try:
        # Try to get 3 free ports from entire range 8000-9000
        ports = get_multiple_free_ports(count=3, start_port=8000, max_port=9000)
        backend_port, ui_port, admin_port = ports[0], ports[1], ports[2]
        print(f"   Found 3 free ports: {backend_port}, {ui_port}, {admin_port}")
    except RuntimeError as e:
        print(f"   [WARNING] {e}")
        print("   Falling back to range-based allocation...")
        # Fallback to range-based allocation
        backend_port = get_free_port(8000, 8100)
        ui_port = get_free_port(8501, 8600)
        admin_port = get_free_port(8601, 8700)
        print(f"   Allocated ports: {backend_port}, {ui_port}, {admin_port}")

    # Set environment variables
    os.environ["BACKEND_PORT"] = str(backend_port)
    os.environ["UI_PORT"] = str(ui_port)
    os.environ["ADMIN_PORT"] = str(admin_port)
    os.environ["SKINAI_API_URL"] = f"http://127.0.0.1:{backend_port}"

    print("=" * 70)
    print(">> Skin AI Assistant - Starting All Services")
    print("=" * 70)
    print(f"Backend API:       http://127.0.0.1:{backend_port}")
    print(f"User UI:           http://localhost:{ui_port}")
    print(f"Admin Dashboard:   http://localhost:{admin_port}")
    print("=" * 70)
    print()

    # Get script directory
    script_dir = Path(__file__).parent

    processes = []

    try:
        # Start backend
        print(f"[1/3] Starting Backend API on port {backend_port}...")
        backend_proc = subprocess.Popen(
            [sys.executable, str(script_dir / "run_backend.py")],
            env=os.environ.copy()
        )
        processes.append(("Backend", backend_proc))
        print("   Waiting for backend to initialize...")
        time.sleep(5)  # Give backend more time to start and load model

        # Start UI
        print(f"[2/3] Starting User UI on port {ui_port}...")
        ui_proc = subprocess.Popen(
            [sys.executable, str(script_dir / "run_ui.py")],
            env=os.environ.copy()
        )
        processes.append(("UI", ui_proc))
        time.sleep(3)  # Give UI time to start

        # Start Admin
        print(f"[3/3] Starting Admin Dashboard on port {admin_port}...")
        admin_proc = subprocess.Popen(
            [sys.executable, str(script_dir / "run_admin.py")],
            env=os.environ.copy()
        )
        processes.append(("Admin", admin_proc))
        time.sleep(2)  # Give admin time to start

        print()
        print("[OK] All services started successfully!")
        print("=" * 70)
        print()
        print("Access URLs:")
        print(f"   - API Documentation: http://127.0.0.1:{backend_port}/docs")
        print(f"   - User Interface:    http://localhost:{ui_port}")
        print(f"   - Admin Dashboard:   http://localhost:{admin_port}")
        print()
        print("Press Ctrl+C to stop all services")
        print("=" * 70)

        # Wait for all processes
        for name, proc in processes:
            proc.wait()

    except KeyboardInterrupt:
        print("\n\n[STOP] Shutting down all services...")
        for name, proc in processes:
            print(f"   Stopping {name}...")
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
        print("[OK] All services stopped.")

    except Exception as e:
        print(f"\n[ERROR] {e}")
        for name, proc in processes:
            proc.terminate()
        sys.exit(1)


if __name__ == "__main__":
    main()
