import socket
import time

def send_command(command):

    server_ip = "127.0.0.1"
    server_port = 143

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))

    print(f"Wysyłam komendę: {command}")
    client_socket.send(f"{command}\r\n".encode('utf-8'))

    time.sleep(1)

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Odpowiedź serwera: {response}")

    client_socket.close()

def login(username, password):
    command = f"LOGIN {username} {password}"
    send_command(command)

def select_folder(folder):
    command = f"SELECT {folder}"
    send_command(command)

def list_folders():
    command = "LIST"
    send_command(command)

def fetch_message(message_id):
    command = f"FETCH {message_id}"
    send_command(command)

def logout():
    command = "LOGOUT"
    send_command(command)

if __name__ == "__main__":
    # Testowanie komend
    login("user", "password")
    select_folder("INBOX")
    list_folders()
    fetch_message(1)
    logout()
