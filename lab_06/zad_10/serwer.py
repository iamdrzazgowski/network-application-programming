import socket

def handle_client(client_socket):
    client_socket.send(b"220 Welcome to Simple SMTP Server\r\n")

    while True:

        request = client_socket.recv(1024).decode('utf-8').strip()
        print(f"Received: {request}")

        if request.startswith('HELO'):
            client_socket.send(b"250 Hello, I am ready to receive your email\r\n")
        elif request.startswith('MAIL FROM'):
            client_socket.send(b"250 Sender OK\r\n")
        elif request.startswith('RCPT TO'):
            client_socket.send(b"250 Recipient OK\r\n")
        elif request.startswith('DATA'):
            client_socket.send(b"354 Start mail input; end with <CRLF>.<CRLF>\r\n")
            email_data = b""
            while True:
                line = client_socket.recv(1024)
                email_data += line
                if b"\r\n.\r\n" in email_data:
                    break
            client_socket.send(b"250 OK: Message accepted for delivery\r\n")
        elif request.startswith('QUIT'):
            client_socket.send(b"221 Bye\r\n")
            break
        else:
            client_socket.send(b"502 Command not implemented\r\n")

    client_socket.close()


def start_smtp_server(host='127.0.0.1', port=2525):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"SMTP server running on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        handle_client(client_socket)


if __name__ == "__main__":
    start_smtp_server(host='127.0.0.1', port=2525)
