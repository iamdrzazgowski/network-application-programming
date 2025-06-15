import socket
import ssl
import threading

HOST = '127.0.0.1'
PORT = 12345

CERTFILE = 'server.pem'
KEYFILE = 'server.key'
CA_CERT = 'ca.pem'

def handle_client(connstream, addr):
    print(f"Połączono z {addr}")
    try:
        while True:
            data = connstream.recv(4096)
            if not data:
                print(f"Klient {addr} zakończył połączenie.")
                break
            print(f"Otrzymano od {addr}: {data.decode(errors='ignore')}")
            connstream.sendall(data)  # echo
    except Exception as e:
        print(f"Błąd w połączeniu z {addr}: {e}")
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
        print(f"Połączenie z {addr} zamknięte.")

def main():
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERTFILE, keyfile=KEYFILE)
    context.load_verify_locations(cafile=CA_CERT)
    context.verify_mode = ssl.CERT_REQUIRED  # wymusz wzajemna weryfikacje klienta

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"Serwer TLS działa na {HOST}:{PORT} (wzajemna weryfikacja certyfikatów)")

        while True:
            newsock, addr = sock.accept()
            try:
                connstream = context.wrap_socket(newsock, server_side=True)
                print(f"Zweryfikowano klienta: {connstream.getpeercert()}")
                threading.Thread(target=handle_client, args=(connstream, addr), daemon=True).start()
            except ssl.SSLError as e:
                print(f"SSL error przy połączeniu z {addr}: {e}")

if __name__ == "__main__":
    main()
