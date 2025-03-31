import socket

HOST = "127.0.0.1"
PORT = 2090

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

hostname = input("Podaj nazwę hosta: ")
sock.sendto(hostname.encode(), (HOST, PORT))

response, _ = sock.recvfrom(1024)
print("Odpowiedź serwera:", response.decode())

sock.close()