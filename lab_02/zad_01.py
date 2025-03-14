import socket

HOST = 'ntp.task.gda.pl'
PORT = 13

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data = s.recv(1024)

    print(data.decode('utf-8').strip())
except Exception as e:
    print(f'Błąd: {e}')