import socket


def scan_ports(host_port):
    print(f"Scanning ports on {host_port}...")

    for port in range(75, 85 + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((host_port, port))

        if result == 0:
            print(f"Port {port} is open")

        sock.close()


target_hosts = input("Enter the host IP address: ")

scan_ports(target_hosts) 