import socket

HOST = '127.0.0.1'
PORT = 2908
MAX_PACKET_LENGTH = 20

def sendall(sock, data):
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError("Połączenie zostało zamknięte")
        total_sent += sent

def recvall(sock, msgLen):
    chunks = []
    bytes_received = 0
    while bytes_received < msgLen:
        chunk = sock.recv(msgLen - bytes_received)
        if chunk == b'':
            raise RuntimeError("Połączenie zostało zamknięte")
        chunks.append(chunk)
        bytes_received += len(chunk)
    return b''.join(chunks)

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        message = input("Podaj wiadomość: ")

        if len(message) < MAX_PACKET_LENGTH:
            message = message.ljust(MAX_PACKET_LENGTH)
        elif len(message) > MAX_PACKET_LENGTH:
            message = message[:MAX_PACKET_LENGTH]

        sendall(s, message.encode('utf-8'))

        response = recvall(s, MAX_PACKET_LENGTH)
        print("Odpowiedź z serwera:", response.decode('utf-8').strip())

except Exception as e:
    print(f'Błąd: {e}')
