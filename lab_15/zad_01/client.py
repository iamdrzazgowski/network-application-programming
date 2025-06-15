import socket

HOST = '127.0.0.1'
PORT = 12345

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print(f"Połączono z serwerem {HOST}:{PORT}")

        while True:
            msg = input("Wpisz wiadomość (lub 'exit' aby zakończyć): ")
            if msg.lower() == 'exit':
                break
            sock.sendall(msg.encode())
            data = sock.recv(4096)
            print(f"Odebrano echo: {data.decode()}")

if __name__ == "__main__":
    main()
