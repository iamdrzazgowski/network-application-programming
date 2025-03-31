import socket

HOST = "127.0.0.1"
PORT = 2090

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    message = input("Podaj wiadomość (lub 'exit' aby zakończyć): ")
    if message.lower() == "exit":
        break
    client_socket.sendto(message.encode(), (HOST, PORT))

    data, _ = client_socket.recvfrom(1024)
    print(f"Odpowiedź serwera: {data.decode()}")

client_socket.close()
