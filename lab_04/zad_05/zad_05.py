import socket

HOST = "127.0.0.1"
PORT = 2090
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"Serwer działa na {HOST}:{PORT}")

while True:
    data, addr = sock.recvfrom(1024)

    print(f"Otrzymano dane od {addr}: {data.decode()}")
    ip_address = data.decode()

    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        response = f"Hostname dla {ip_address} to {hostname}"
    except socket.herror:
        response = f"Nie znaleziono hosta dla adresu IP: {ip_address}"

    sock.sendto(response.encode(), addr)
