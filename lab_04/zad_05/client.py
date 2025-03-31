import socket

HOST = "127.0.0.1"
PORT = 2090
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    ip_address = input("Wprowadź adres IP: ")
    sock.sendto(ip_address.encode(), (HOST, PORT))
    data, server = sock.recvfrom(1024)
    print(f"Odpowiedź od serwera: {data.decode()}")
sock.close()
