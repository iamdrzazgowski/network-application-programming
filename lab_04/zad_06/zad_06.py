import socket

HOST = "127.0.0.1"
PORT = 2090
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"Serwer działa na {HOST}:{PORT}")

while True:
    data, addr = sock.recvfrom(1024)

    print(f"Otrzymano dane od {addr}: {data.decode()}")
    hostname = data.decode()

    try:
        ip_address = socket.gethostbyname(hostname)
        response = f"Adres IP dla {hostname} to {ip_address}"
    except socket.gaierror:
        response = f"Nie znaleziono adresu IP dla hosta: {hostname}"

    sock.sendto(response.encode(), addr)
