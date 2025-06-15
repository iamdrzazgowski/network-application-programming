import socket
import os

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 2904
SAVE_DIR = "pobrane_zdjecia"

def receive_line(sock):
    line = b""
    while not line.endswith(b"\r\n"):
        chunk = sock.recv(1)
        if not chunk:
            break
        line += chunk
    return line.decode('utf-8').strip()

def request_file_list():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.sendall(b"LIST_FILES\r\n")
        response = receive_line(sock)
        if response.startswith("FILES"):
            files = response[6:].split()
            if files:
                print("Dostępne pliki:")
                for f in files:
                    print(" -", f)
            else:
                print("Brak dostępnych plików.")
        else:
            print("Błąd serwera:", response)

def request_file(filename):
    os.makedirs(SAVE_DIR, exist_ok=True)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER_HOST, SERVER_PORT))
        sock.sendall(f"GET_FILE {filename}\r\n".encode('utf-8'))

        response = receive_line(sock)
        if response.startswith("ERROR"):
            print("Błąd serwera:", response)
            return

        parts = response.split()
        if len(parts) != 4 or parts[0] != "SIZE" or parts[2] != "NAME":
            print("Niepoprawna odpowiedź serwera:", response)
            return

        try:
            filesize = int(parts[1])
        except ValueError:
            print("Nieprawidłowy rozmiar pliku.")
            return

        save_path = os.path.join(SAVE_DIR, parts[3])
        print(f"Pobieranie pliku '{parts[3]}' ({filesize} bajtów)...")

        with open(save_path, "wb") as f:
            received = 0
            while received < filesize:
                chunk = sock.recv(min(4096, filesize - received))
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)
                print(f"Odebrano {received} / {filesize} bajtów", end='\r')

        print(f"\nZapisano plik do: {save_path}")

def main():
    print("1. Wyświetl listę plików")
    print("2. Pobierz plik")
    choice = input("Wybierz opcję (1/2): ").strip()

    if choice == "1":
        request_file_list()
    elif choice == "2":
        filename = input("Podaj nazwę pliku do pobrania: ").strip()
        request_file(filename)
    else:
        print("Nieznana opcja.")

if __name__ == "__main__":
    main()
