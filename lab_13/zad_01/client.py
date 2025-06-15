import socket
import os

def upload_file(server_host, server_port, filepath):
    if not os.path.isfile(filepath):
        print(f"Plik '{filepath}' nie istnieje.")
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_host, server_port))
            command = f"UPLOAD {filename} {filesize}\n"
            sock.sendall(command.encode('utf-8'))

            response = b""
            while not response.endswith(b"\n"):
                chunk = sock.recv(1)
                if not chunk:
                    print("Serwer rozłączył się przed wysłaniem odpowiedzi.")
                    return
                response += chunk

            response_text = response.decode('utf-8').strip()
            if response_text != "OK":
                print(f"Serwer odpowiedział błędem: {response_text}")
                return

            with open(filepath, "rb") as f:
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    sock.sendall(data)

            print(f"Plik '{filename}' został wysłany poprawnie.")

    except Exception as e:
        print(f"Błąd połączenia lub wysyłania: {e}")

if __name__ == "__main__":
    host = input("Podaj adres serwera (np. 127.0.0.1): ").strip()
    port_str = input("Podaj port serwera (np. 80): ").strip()

    if not port_str.isdigit():
        print("Port musi być liczbą.")
        exit(1)
    port = int(port_str)

    filepath = input("Podaj ścieżkę do pliku do wysłania: ").strip()

    upload_file(host, port, filepath)
