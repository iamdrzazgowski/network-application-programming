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

def main():
    os.makedirs(SAVE_DIR, exist_ok=True)

    # Użytkownik wpisuje komendę
    user_command = input("Wpisz komendę do wysłania (np. GET_IMAGE): ").strip()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(10)
        print(f"Łączenie z {SERVER_HOST}:{SERVER_PORT}...")
        sock.connect((SERVER_HOST, SERVER_PORT))

        # Wysłanie komendy użytkownika z końcówką \r\n
        full_command = f"{user_command}\r\n".encode('utf-8')
        sock.sendall(full_command)

        response = receive_line(sock)
        if response.startswith("ERROR"):
            print("Serwer odpowiedział błędem:", response)
            return

        parts = response.split()
        if len(parts) != 4 or parts[0] != "SIZE" or parts[2] != "NAME":
            print("Niepoprawna odpowiedź serwera:", response)
            return

        try:
            filesize = int(parts[1])
        except ValueError:
            print("Błędny rozmiar pliku od serwera:", parts[1])
            return

        filename = parts[3]
        save_path = os.path.join(SAVE_DIR, filename)
        print(f"Odbieram plik '{filename}' ({filesize} bajtów)...")
        print(f"Zapis do: {save_path}")

        with open(save_path, "wb") as f:
            received = 0
            while received < filesize:
                to_read = min(65536, filesize - received)
                chunk = sock.recv(to_read)
                if not chunk:
                    print("\nPołączenie zostało przerwane przed odebraniem całego pliku.")
                    break
                f.write(chunk)
                received += len(chunk)
                print(f"Odebrano {received} / {filesize} bajtów", end='\r', flush=True)

        if received == filesize:
            print(f"\nPlik '{filename}' odebrany i zapisany poprawnie.")
        else:
            print(f"\nNie odebrano całego pliku, odebrano {received} z {filesize} bajtów.")

if __name__ == "__main__":
    main()
