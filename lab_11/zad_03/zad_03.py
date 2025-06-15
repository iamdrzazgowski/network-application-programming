import socket
import threading
import random

def handle_client(client_socket, client_address):
    number_to_guess = random.randint(1, 100)
    print(f"Klient {client_address} - wylosowana liczba: {number_to_guess}")
    client_socket.sendall("Witaj! Odgadnij liczbę od 1 do 100.\n".encode('utf-8'))

    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f"Klient {client_address} rozłączył się.")
                break

            message = data.decode().strip()
            print(f"Otrzymano od {client_address}: {message}")

            if not message.isdigit():
                response = "Błąd: proszę podać liczbę.\n"
                client_socket.sendall(response.encode('utf-8'))
                continue

            guess = int(message)

            if guess < number_to_guess:
                response = "Twoja liczba jest za mała.\n"
            elif guess > number_to_guess:
                response = "Twoja liczba jest za duża.\n"
            else:
                response = "Gratulacje! Odgadłeś liczbę!\n"
                client_socket.sendall(response.encode('utf-8'))
                print(f"Klient {client_address} odgadł liczbę i zakończył działanie.")
                break

            client_socket.sendall(response.encode('utf-8'))
    except ConnectionResetError:
        print(f"Klient {client_address} niespodziewanie rozłączył się.")
    finally:
        client_socket.close()


def start_server(host="127.0.0.1", port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Serwer działa na {host}:{port} i czeka na połączenia...")

    try:
        while True:
            client_socket, client_address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
    except KeyboardInterrupt:
        print("Zamykanie serwera...")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
