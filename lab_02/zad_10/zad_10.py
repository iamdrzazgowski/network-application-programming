import socket

HOST = '127.0.0.1'
# HOST = "212.182.24.27"
PORT = 2907

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

hostname = input("Podaj nazwę hosta: ")

try:
    print(f"Wysyłanie hosta: {hostname} do serwera {HOST}:{PORT}")
    client_socket.sendto(hostname.encode(), (HOST, PORT))

    response, server_address = client_socket.recvfrom(1024)
    ip_address = response.decode()

    print(f"Otrzymany adres IP: {ip_address}")

except socket.error as e:
    print(f"Błąd komunikacji: {e}")

finally:
    client_socket.close()