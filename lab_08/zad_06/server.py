import socket

def handle_client(client_socket):

    client_socket.send(b"* OK IMAP4rev1 Service Ready\r\n")

    while True:

        request = client_socket.recv(1024).decode('utf-8').strip()

        if not request:
            break

        print(f"Otrzymano komendę: {request}")

        parts = request.split(" ", 1)
        command = parts[0].upper()

        if command == "LOGIN":
            if len(parts) > 1:
                client_socket.send(b"1 OK LOGIN completed\r\n")
            else:
                client_socket.send(b"1 NO LOGIN failed\r\n")

        elif command == "SELECT":
            client_socket.send(b"1 OK [READ-WRITE] SELECT completed\r\n")

        elif command == "LIST":
            client_socket.send(b"* LIST (\\Noselect) \"/\" \"INBOX\"\r\n")
            client_socket.send(b"1 OK LIST completed\r\n")

        elif command == "FETCH":
            client_socket.send(
                b"* 1 FETCH (FLAGS (\\Seen) INTERNALDATE \"04-Apr-2025 12:34:56 +0000\" RFC822.SIZE 512)\r\n")
            client_socket.send(b"1 OK FETCH completed\r\n")

        else:
            client_socket.send(b"BAD Command unrecognized\r\n")

    client_socket.close()

def start_server(host='127.0.0.1', port=143):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Serwer IMAP nasłuchuje na {host}:{port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Połączenie od {addr}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
