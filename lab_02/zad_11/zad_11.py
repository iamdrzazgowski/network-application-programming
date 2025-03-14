import socket

HOST = '127.0.0.1'
# HOST = '212.182.24.27'
PORT = 2908

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        message = input("Podaj wiadomość: ")

        if len(message) < 20:
            message = message.ljust(20)
        elif len(message) > 20:
            message = message[:20]

        s.sendall(message.encode('utf-8'))

        response = s.recv(1024)
        print("Odpowiedź z serwera:", response.decode('utf-8').strip())

except Exception as e:
    print(f'Błąd: {e}')
