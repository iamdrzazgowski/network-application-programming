import socket

HOST = "127.0.0.1"
PORT = 2090

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    message = input("Podaj operację (np. 5 + 3): ")
    client_socket.sendto(message.encode(), (HOST, PORT))
    data, addr = client_socket.recvfrom(1024)
    print(f"Wynik: {data.decode()}")

client_socket.close()
