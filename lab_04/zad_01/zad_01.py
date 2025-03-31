import socket
import datetime

host = '127.0.0.1'
port = 2090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()
print(f"Serwer nasłuchuje na {host}:{port}")

while True:
    client_socket, client_address = server_socket.accept()
    with client_socket:
        print(f"Połączono z {client_address}")
        data = client_socket.recv(1024)
        if data:
            received_message = data.decode('utf-8')
            print(f"Odebrano wiadomość: {received_message}")
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            client_socket.sendall(current_time.encode('utf-8'))
        print(f"Zamknięcie połączenia z {client_address}")
