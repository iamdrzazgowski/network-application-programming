import socket
import ssl
import threading

HOST = '127.0.0.1'
PORT = 80
CERT_FILE = 'cert.pem'
KEY_FILE = 'key.pem'

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
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
        sock.bind((HOST, PORT))
        sock.listen(5)
        print(f"Serwer działa na {HOST}:{PORT} z TLS")

        while True:
            newsock, addr = sock.accept()
            try:
                connstream = context.wrap_socket(newsock, server_side=True)
                threading.Thread(target=handle_client, args=(connstream, addr), daemon=True).start()
            except ssl.SSLError as e:
                print(f"SSL error przy połączeniu z {addr}: {e}")

if __name__ == "__main__":
    main()
