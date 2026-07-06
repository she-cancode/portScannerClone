import socket
import json
from concurrent.futures import ThreadPoolExecutor

TARGET_IP = "8.8.8.8"
open_ports = []

# A simple dictionary mapping common ports to their expected services
COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    853: "DNS over TLS"
}


def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        result = s.connect_ex((TARGET_IP, port))

        if result == 0:
            open_ports.append(port)

        s.close()
    except Exception:
        pass


def run_scanner():
    print(f"Starting aggressive scan on {TARGET_IP}...")
    ports_to_scan = range(1, 1025)

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan_port, ports_to_scan)

    # Build a structured dictionary from our results
    scan_results = {
        "target_ip": TARGET_IP,
        "total_open": len(open_ports),
        "details": []
    }

    # Sort the ports numerically before processing
    for port in sorted(open_ports):
        service_name = COMMON_SERVICES.get(port, "Unknown Service")
        scan_results["details"].append({
            "port": port,
            "expected_service": service_name
        })

    # Print the final data structure
    print("\n--- Structured Scan Results ---")
    print(json.dumps(scan_results, indent=4))


if __name__ == "__main__":
    run_scanner()