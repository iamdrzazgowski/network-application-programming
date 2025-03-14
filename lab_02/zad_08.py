import socket


def scan_ports(host):
    print(f"Scanning ports on {host}...")

    for port in range(75, 86):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((host, port))

        if result == 0:
            try:
                service = socket.getservbyport(port, "tcp")
            except OSError:
                service = "Nieznana usługa"

            print(f"Port {port} jest OTWARTY - Usługa: {service}")
        else:
            print(f"Port {port} jest ZAMKNIĘTY")

        sock.close()


target_host = input("Enter the host IP address: ")
scan_ports(target_host)