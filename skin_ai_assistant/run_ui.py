import os
import sys
from pathlib import Path
from utils.port_utils import get_free_port, is_port_free
import subprocess


def main():
    ui_port_env = os.getenv("UI_PORT")
    if ui_port_env:
        ui_port = int(ui_port_env)
        # Verify the specified port is actually free
        if not is_port_free(ui_port):
            print(f"[UI] WARNING: Specified port {ui_port} is in use, finding alternative...")
            ui_port = get_free_port(8000, 9000)
            os.environ["UI_PORT"] = str(ui_port)
    else:
        # Dynamically find any free port in wide range
        ui_port = get_free_port(8000, 9000)
        os.environ["UI_PORT"] = str(ui_port)

    # Set backend URL if provided
    backend_port = os.getenv("BACKEND_PORT", "8000")
    os.environ["SKINAI_API_URL"] = f"http://127.0.0.1:{backend_port}"

    ui_app_path = Path(__file__).parent / "ui" / "streamlit_app.py"

    print(f"[UI] Starting Streamlit on port {ui_port} (dynamically allocated)")
    print(f"[UI] Connecting to backend at {os.environ['SKINAI_API_URL']}")

    subprocess.run([
        sys.executable, "-m", "streamlit", "run",
        str(ui_app_path),
        "--server.port", str(ui_port),
        "--server.address", "localhost"
    ])


if __name__ == "__main__":
    main()
