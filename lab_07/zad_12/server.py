import socket

messages = [
    {"id": 1, "size": 256, "content": "Treść pierwszej wiadomości - TEST."},
    {"id": 2, "size": 512, "content": "Treść drugiej wiadomości - TEST."},
    {"id": 3, "size": 128, "content": "Treść trzeciej wiadomości - TEST."}
]

def handle_client_connection(client_socket):
    # Powitanie serwera POP3
    client_socket.send(b"+OK POP3 server ready\r\n")

    while True:
        request = client_socket.recv(1024).decode('utf-8').strip()
        print(f"Komenda od klienta: {request}")

        if request.startswith("USER"):
            client_socket.send(b"+OK User accepted\r\n")

        elif request.startswith("PASS"):
            client_socket.send(b"+OK Pass accepted\r\n")

        elif request.startswith("STAT"):
            num_messages = len(messages)
            total_size = sum(msg['size'] for msg in messages)
            client_socket.send(f"+OK {num_messages} {total_size}\r\n".encode('utf-8'))

        elif request.startswith("LIST"):
            client_socket.send(b"+OK List of messages follows\r\n")
            for msg in messages:
                client_socket.send(f"{msg['id']} {msg['size']}\r\n".encode('utf-8'))
            client_socket.send(b".\r\n")

        elif request.startswith("RETR"):
            try:
                msg_id = int(request.split()[1])
                message = next(msg for msg in messages if msg['id'] == msg_id)
                client_socket.send(f"+OK {message['size']} octets\r\n".encode('utf-8'))
                client_socket.send(f"{message['content']}\r\n".encode('utf-8'))
                client_socket.send(b".\r\n")
            except (ValueError, StopIteration):
                client_socket.send(b"-ERR Message not found\r\n")

        elif request.startswith("QUIT"):
            client_socket.send(b"+OK Bye\r\n")
            client_socket.close()
            break

        else:
            client_socket.send(b"-ERR Unknown command\r\n")


def run_pop3_server(host="127.0.0.1", port=110):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Serwer POP3 działa na {host}:{port}...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Połączono z {client_address}")

        handle_client_connection(client_socket)

if __name__ == "__main__":
    run_pop3_server()
