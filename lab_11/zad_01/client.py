import socket


def start_client(host="127.0.0.1", port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print(f"Połączono z serwerem {host}:{port}")

        try:
            while True:
                message = input("Wpisz wiadomość (lub 'exit' aby zakończyć): ")
                if message.lower() == 'exit':
                    print("Zamykanie klienta.")
                    break

                sock.sendall(message.encode())
                data = sock.recv(1024)
                print(f"Otrzymano echo: {data.decode()}")
        except ConnectionResetError:
            print("Połączenie z serwerem zostało przerwane.")


if __name__ == "__main__":
    start_client()
