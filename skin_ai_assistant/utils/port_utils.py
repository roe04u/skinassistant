import socket


def get_free_port(start_port: int = 8000, max_port: int = 9000) -> int:
    """
    Scan from start_port upwards and return the first free TCP port.
    """
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    raise RuntimeError(f"No free ports found in range {start_port}-{max_port}.")


def get_multiple_free_ports(count: int, start_port: int = 8000, max_port: int = 9000) -> list[int]:
    """
    Get multiple free TCP ports starting from start_port.

    Args:
        count: Number of free ports to find
        start_port: Port to start scanning from
        max_port: Maximum port to scan to

    Returns:
        List of free port numbers

    Raises:
        RuntimeError: If not enough free ports are found
    """
    free_ports = []
    current_port = start_port

    while len(free_ports) < count and current_port <= max_port:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", current_port))
                free_ports.append(current_port)
            except OSError:
                # Port is in use, continue to next
                pass
        current_port += 1

    if len(free_ports) < count:
        raise RuntimeError(f"Only found {len(free_ports)} free ports out of {count} requested in range {start_port}-{max_port}.")

    return free_ports


def is_port_free(port: int, host: str = "127.0.0.1") -> bool:
    """
    Check if a specific port is free.

    Args:
        port: Port number to check
        host: Host address to check (default: 127.0.0.1)

    Returns:
        True if port is free, False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return True
        except OSError:
            return False
