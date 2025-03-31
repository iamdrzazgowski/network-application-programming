import socket
import time

def udp_server(host='127.0.0.1', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print("UDP Server listening...")
    while True:
        # Oczekiwanie na wiadomość od klienta
        data, addr = server_socket.recvfrom(1024)
        print(f"Received message from {addr}: {data}")
        # Odpowiedź (echo) do klienta
        server_socket.sendto(data, addr)

def udp_client(host='127.0.0.1', port=12345, message=b'Hello, UDP!'):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    start_time = time.perf_counter()
    # Wysyłanie wiadomości do serwera
    client_socket.sendto(message, (host, port))
    # Oczekiwanie na odpowiedź
    data, addr = client_socket.recvfrom(1024)
    end_time = time.perf_counter()
    client_socket.close()
    print(f"Received response from {addr}: {data}")
    print(f"UDP Round Trip Time: {end_time - start_time:.6f} seconds")

if __name__ == "__main__":
    from multiprocessing import Process

    # Tworzenie i uruchomienie serwera UDP w osobnym procesie
    udp_server_process = Process(target=udp_server)

    udp_server_process.start()
    time.sleep(1)  # Czekanie na uruchomienie serwera

    # Uruchomienie klienta UDP
    udp_client()

    # Zakończenie serwera
    udp_server_process.terminate()
