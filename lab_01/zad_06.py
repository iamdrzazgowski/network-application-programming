import socket

HOST = str(input("Podaj hosta: "))
PORT = int(input("Podaj port: "))

server_address = (HOST, int(PORT))

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("OK")
except socket.error as e:
    print("Bład")
