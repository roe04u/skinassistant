import os
import sys
from pathlib import Path
from utils.port_utils import get_free_port, is_port_free
import subprocess


def main():
    admin_port_env = os.getenv("ADMIN_PORT")
    if admin_port_env:
        admin_port = int(admin_port_env)
        # Verify the specified port is actually free
        if not is_port_free(admin_port):
            print(f"[Admin] WARNING: Specified port {admin_port} is in use, finding alternative...")
            admin_port = get_free_port(8000, 9000)
            os.environ["ADMIN_PORT"] = str(admin_port)
    else:
        # Dynamically find any free port in wide range
        admin_port = get_free_port(8000, 9000)
        os.environ["ADMIN_PORT"] = str(admin_port)

    # Set backend URL if provided
    backend_port = os.getenv("BACKEND_PORT", "8000")
    os.environ["SKINAI_API_URL"] = f"http://127.0.0.1:{backend_port}"

    admin_app_path = Path(__file__).parent / "ui" / "admin_app.py"

    print(f"[Admin] Starting Admin Dashboard on port {admin_port} (dynamically allocated)")
    print(f"[Admin] Connecting to backend at {os.environ['SKINAI_API_URL']}")

    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        str(admin_app_path),
        "--server.port", str(admin_port),
        "--server.address", "localhost"
    ])


if __name__ == "__main__":
    main()
