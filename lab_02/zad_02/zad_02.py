import socket

# HOST = '212.182.24.27'
HOST = '127.0.0.1'
PORT = 2900

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = str(input("Podaj wiadomość: "))
        s.sendall(message.encode('utf-8'))
        response = s.recv(1024)
        print(response.decode('utf-8').strip())
except Exception as e:
    print(f'Błąd: {e}')