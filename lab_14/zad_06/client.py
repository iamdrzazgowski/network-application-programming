import socket
import ssl

HOST = '127.0.0.1'
PORT = 12345

CERTFILE = 'client.pem'
KEYFILE = 'client.key'
CA_CERT = 'ca.pem'

def main():
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=CA_CERT)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname='localhost') as ssock:
            print(f"Połączono z serwerem TLS: {ssock.getpeercert()}")

            while True:
                msg = input("Wpisz wiadomość (lub 'exit' aby zakończyć): ")
                if msg.lower() == 'exit':
                    break
                ssock.sendall(msg.encode())
                data = ssock.recv(4096)
                print(f"Odebrano echo: {data.decode()}")

if __name__ == "__main__":
    main()
