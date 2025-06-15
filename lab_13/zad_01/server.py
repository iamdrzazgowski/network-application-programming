import socket
import threading
import os

def handle_client(client_socket, client_address):
    print(f"Połączono z {client_address}")

    try:
        command_line = b""
        while not command_line.endswith(b"\n"):
            chunk = client_socket.recv(1)
            if not chunk:
                print(f"Klient {client_address} rozłączył się przed wysłaniem komendy.")
                client_socket.close()
                return
            command_line += chunk

        command_line = command_line.decode('utf-8').strip()
        parts = command_line.split()
        if len(parts) != 3 or parts[0] != "UPLOAD":
            client_socket.sendall("ERROR Nieprawidłowa komenda. Użyj: UPLOAD <filename> <filesize>\n".encode('utf-8'))
            client_socket.close()
            return

        _, filename, filesize_str = parts

        if not filesize_str.isdigit():
            client_socket.sendall("ERROR Rozmiar pliku musi być liczbą.\n".encode('utf-8'))
            client_socket.close()
            return

        filesize = int(filesize_str)
        if filesize <= 0:
            client_socket.sendall("ERROR Rozmiar pliku musi być większy niż 0.\n".encode('utf-8'))
            client_socket.close()
            return

        client_socket.sendall("OK\n".encode('utf-8'))

        received_bytes = 0
        os.makedirs("uploads", exist_ok=True)
        with open(f"uploads/{filename}", "wb") as f:
            while received_bytes < filesize:
                chunk = client_socket.recv(min(4096, filesize - received_bytes))
                if not chunk:
                    print(f"Klient {client_address} rozłączył się w trakcie uploadu.")
                    break
                f.write(chunk)
                received_bytes += len(chunk)

        if received_bytes == filesize:
            print(f"Plik {filename} odebrany poprawnie od {client_address}.")
        else:
            print(f"Upload pliku {filename} od {client_address} niekompletny.")

    except Exception as e:
        print(f"Błąd obsługi klienta {client_address}: {e}")
    finally:
        client_socket.close()

def start_server(host="127.0.0.1", port=80):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Serwer uploadu działa na {host}:{port}")

    try:
        while True:
            client_socket, client_address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Zamykanie serwera...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
