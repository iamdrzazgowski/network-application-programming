import socket


def find_knocking_sequence(target_ip):
    knocking_ports = []
    for port in range(10666, 65666, 1000):  # Zakładamy, że końcówki 666 są w tym zakresie
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            udp_socket.settimeout(0.5)  # Krótkie timeouty dla szybszego skanowania
            udp_socket.sendto(b'PING', (target_ip, port))
            try:
                data, _ = udp_socket.recvfrom(1024)
                if data == b'PONG':
                    print(f"Found knocking port: {port}")
                    knocking_ports.append(port)
            except socket.timeout:
                continue
    return knocking_ports


def send_knocking_sequence(target_ip, knocking_ports):
    for port in knocking_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
            udp_socket.sendto(b'PING', (target_ip, port))


def connect_to_hidden_service(target_ip, target_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect((target_ip, target_port))
        response = tcp_socket.recv(1024)
        print("Response from hidden service:", response.decode())


def main():
    target_ip = "212.182.24.27"
    target_port = 2913

    print("Scanning for knocking sequence...")
    knocking_ports = find_knocking_sequence(target_ip)

    if knocking_ports:
        print("Sending knocking sequence...")
        send_knocking_sequence(target_ip, knocking_ports)
        print("Connecting to hidden service...")
        connect_to_hidden_service(target_ip, target_port)
    else:
        print("No valid knocking ports found!")


if __name__ == "__main__":
    main()
