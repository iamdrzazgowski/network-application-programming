import socket
import ssl

SERVER = '212.182.24.27'
PORT = 29443
CA_CERT_FILE = 'server_root_ca.pem'  # podaj poprawną ścieżkę do certyfikatu

def main():
    context = ssl.create_default_context(cafile=CA_CERT_FILE)
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    with socket.create_connection((SERVER, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=SERVER) as ssock:
            print("Połączono z serwerem i zweryfikowano certyfikat.")

            while True:
                msg = input("Wpisz tekst do wysłania (lub 'exit' aby zakończyć): ")
                if msg.lower() == 'exit':
                    break
                ssock.sendall(msg.encode() + b'\n')
                response = ssock.recv(4096)
                print("Odpowiedź serwera:", response.decode(errors='ignore'))

if __name__ == "__main__":
    main()
