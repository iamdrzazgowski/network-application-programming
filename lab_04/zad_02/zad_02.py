import socket

HOST = '127.0.0.1'
PORT = 2090

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Serwer nasłuchuje na {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Połączono z {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Otrzymano: {data.decode()}")
            conn.sendall(data)
            print("Odesłano wiadomość")
