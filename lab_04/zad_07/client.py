import socket

HOST = '127.0.0.1'
PORT = 2900

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

message = input("Wpisz wiadomość ('exit' aby zakończyć): ")
message = message[:20]
client_socket.send(message.encode())
response = client_socket.recv(20)  # Serwer ogranicza odbieraną odpowiedź do 20 znaków
print("Odpowiedź serwera:", response.decode())

client_socket.close()
