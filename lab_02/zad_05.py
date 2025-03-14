import socket

HOST = '212.182.24.27'
PORT = 2901

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        while True:
            message = input("Wpisz wiadomość do wysłania (lub 'exit' aby zakończyć): ")
            if message.lower() == 'exit':
                break
            s.sendto(message.encode('utf-8'), (HOST, PORT))
            response, server = s.recvfrom(1024)
            print(f"Odpowiedź z serwera: {response.decode('utf-8').strip()}")
except Exception as e:
    print(f'Błąd: {e}')