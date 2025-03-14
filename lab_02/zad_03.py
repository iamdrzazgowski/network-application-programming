import socket

HOST = '212.182.24.27'
PORT = 2900

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            message = input("Wpisz wiadomość do wysłania (lub 'exit' aby zakończyć): ")
            if message.lower() == 'exit':
                break
            s.sendall(message.encode('utf-8'))
            response = s.recv(1024)
            print(f"Odpowiedź z serwera: {response.decode('utf-8').strip()}")
except Exception as e:
    print(f'Błąd: {e}')