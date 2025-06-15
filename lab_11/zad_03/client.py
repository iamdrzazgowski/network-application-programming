import socket

def start_client(host="127.0.0.1", port=12345):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        welcome = sock.recv(1024).decode()
        print(welcome.strip())

        while True:
            message = input("Podaj liczbę: ").strip()
            if not message:
                continue
            sock.sendall(message.encode())

            response = sock.recv(1024).decode()
            print("Serwer:", response.strip())

            if "Gratulacje" in response:
                print("Zakończono grę.")
                break

if __name__ == "__main__":
    start_client()
