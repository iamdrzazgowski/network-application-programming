import socket
import select

HOST = '127.0.0.1'
PORT = 12345

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"Serwer działa na {HOST}:{PORT}")

    inputs = [server_sock]

    while True:
        readable, _, exceptional = select.select(inputs, [], inputs)
        for s in readable:
            if s is server_sock:
                client_sock, addr = server_sock.accept()
                print(f"Połączono z {addr}")
                inputs.append(client_sock)
            else:
                try:
                    data = s.recv(4096)
                    if data:
                        s.sendall(data)
                    else:
                        print(f"Połączenie zamknięte: {s.getpeername()}")
                        inputs.remove(s)
                        s.close()
                except ConnectionResetError:
                    print(f"Połączenie zerwane: {s.getpeername()}")
                    inputs.remove(s)
                    s.close()

        for s in exceptional:
            print(f"Wyjątek na gnieździe: {s.getpeername()}")
            inputs.remove(s)
            s.close()

if __name__ == "__main__":
    main()
