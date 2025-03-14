import socket

HOST = '127.0.0.1'
# HOST = "212.182.24.27"
PORT = 2906

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_ip = socket.gethostbyname(socket.gethostname())

try:
    print(f"Wysyłanie IP: {client_ip} do serwera {HOST}:{PORT}")
    client_socket.sendto(client_ip.encode(), (HOST, PORT))

    response, server_address = client_socket.recvfrom(1024)
    hostname = response.decode()

    print(f"Otrzymana nazwa hosta: {hostname}")

except socket.error as e:
    print(f"Błąd komunikacji: {e}")

finally:
    client_socket.close()