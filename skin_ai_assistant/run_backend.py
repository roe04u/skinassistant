import os
from utils.port_utils import get_free_port, is_port_free
import uvicorn


def main():
    port_env = os.getenv("BACKEND_PORT")
    if port_env:
        port = int(port_env)
        # Verify the specified port is actually free
        if not is_port_free(port):
            print(f"[Backend] WARNING: Specified port {port} is in use, finding alternative...")
            port = get_free_port(8000, 9000)
            os.environ["BACKEND_PORT"] = str(port)
    else:
        # Dynamically find any free port in wide range
        port = get_free_port(8000, 9000)
        os.environ["BACKEND_PORT"] = str(port)

    print(f"[Backend] Starting FastAPI on port {port}")
    print(f"[Backend] Scanning for free port from entire range 8000-9000")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)


if __name__ == "__main__":
    main()
