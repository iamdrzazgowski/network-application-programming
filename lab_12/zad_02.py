import socket
import threading
from datetime import datetime

LOG_FILE = "server_log.txt"

def log_event(event):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {event}\n")

def handle_client(client_socket, client_address):
    log_event(f"Połączono z {client_address}")
    print(f"Połączono z {client_address}")
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                log_event(f"Klient {client_address} rozłączył się.")
                print(f"Klient {client_address} rozłączył się.")
                break
            message = data.decode(errors='replace')
            log_event(f"Otrzymano od {client_address}: {message}")
            print(f"Otrzymano od {client_address}: {message}")
            client_socket.sendall(data)  # Echo - odsyłamy tę samą wiadomość
    except ConnectionResetError:
        log_event(f"Klient {client_address} niespodziewanie rozłączył się.")
        print(f"Klient {client_address} niespodziewanie rozłączył się.")
    finally:
        client_socket.close()

def start_server(host="127.0.0.1", port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    log_event(f"Serwer wystartował na {host}:{port}")
    print(f"Serwer działa na {host}:{port} i czeka na połączenia...")

    try:
        while True:
            client_socket, client_address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Zamykanie serwera...")
        log_event("Serwer został zamknięty.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
