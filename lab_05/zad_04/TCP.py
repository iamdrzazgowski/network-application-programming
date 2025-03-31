import socket
import time

def tcp_server(host='127.0.0.1', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("TCP Server listening...")
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

def tcp_client(host='127.0.0.1', port=12345, message=b'Hello, TCP!'):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    start_time = time.perf_counter()
    client_socket.sendall(message)
    data = client_socket.recv(1024)
    end_time = time.perf_counter()
    client_socket.close()
    print(f"TCP Round Trip Time: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    from multiprocessing import Process

    tcp_server_process = Process(target=tcp_server)

    tcp_server_process.start()
    time.sleep(1)  # Wait for server to start

    tcp_client()

    tcp_server_process.terminate()