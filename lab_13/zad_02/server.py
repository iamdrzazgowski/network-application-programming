import socket
import threading
import os

HOST = '127.0.0.1'
PORT = 2904
FILES_DIR = "obrazy"  # folder z plikami do pobrania

def send_line(sock, line: str):
    sock.sendall((line.strip() + "\r\n").encode('utf-8'))

def handle_get_image(client_socket):
    image_path = os.path.join(FILES_DIR, "samoyed.jpg")
    if not os.path.isfile(image_path):
        send_line(client_socket, "ERROR Nie znaleziono pliku.")
        return

    filesize = os.path.getsize(image_path)
    filename = os.path.basename(image_path)

    send_line(client_socket, f"SIZE {filesize} NAME {filename}")

    with open(image_path, "rb") as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            client_socket.sendall(data)

def handle_list_files(client_socket):
    if not os.path.isdir(FILES_DIR):
        send_line(client_socket, "ERROR Folder z plikami nie istnieje.")
        return
    files = os.listdir(FILES_DIR)
    files = [f for f in files if os.path.isfile(os.path.join(FILES_DIR, f))]
    if not files:
        send_line(client_socket, "ERROR Brak plików.")
    else:
        send_line(client_socket, "FILES " + " ".join(files))

def handle_help(client_socket):
    help_text = "Dostępne komendy:\n" \
                "GET_IMAGE – pobiera obrazek samoyed.jpg\n" \
                "LIST_FILES – wypisuje pliki w folderze\n" \
                "HELP – wyświetla pomoc"
    for line in help_text.splitlines():
        send_line(client_socket, line)

def handle_client(client_socket, client_address):
    print(f"Połączono z {client_address}")
    try:
        command = b""
        while not command.endswith(b"\r\n"):
            chunk = client_socket.recv(1)
            if not chunk:
                print(f"Klient {client_address} rozłączył się przed wysłaniem komendy.")
                return
            command += chunk

        command_str = command.decode('utf-8').strip()
        print(f"Otrzymano komendę: {command_str}")

        if command_str == "GET_IMAGE":
            handle_get_image(client_socket)
        elif command_str == "LIST_FILES":
            handle_list_files(client_socket)
        elif command_str == "HELP":
            handle_help(client_socket)
        else:
            send_line(client_socket, "ERROR Nieznana komenda.")

    except Exception as e:
        print(f"Błąd obsługi klienta {client_address}: {e}")
    finally:
        client_socket.close()

def start_server():
    os.makedirs(FILES_DIR, exist_ok=True)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Serwer działa na {HOST}:{PORT}")

    try:
        while True:
            client_socket, client_address = server.accept()
            threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True).start()
    except KeyboardInterrupt:
        print("Zamykanie serwera...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
