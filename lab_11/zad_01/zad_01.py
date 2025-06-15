import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Połączono z {client_address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Klient {client_address} rozłączył się.")
                break
            print(f"Otrzymano od {client_address}: {data.decode()}")
            client_socket.sendall(data)  # Echo - odsyłamy tę samą wiadomość
    except ConnectionResetError:
        print(f"Klient {client_address} niespodziewanie rozłączył się.")
    finally:
        client_socket.close()

def start_server(host="127.0.0.1", port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Serwer działa na {host}:{port} i czeka na połączenia...")

    while True:
        client_socket, client_address = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_server()
