import socket

host = '127.0.0.1'
port = 2090

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((host, port))
    message = input("Podaj wiadomość: ")
    client_socket.sendall(message.encode('utf-8'))
    data = client_socket.recv(1024)
    print(f"Otrzymano od serwera: {data.decode('utf-8')}")
