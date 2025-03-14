import socket

HOST = '127.0.0.1'
PORT = 2902

num1 = input("Podaj pierwszą liczbę: ")
operator = str(input("Podaj operator (+, -, *, /): "))
num2 = input("Podaj drugą liczbę: ")

try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(num1.encode('utf-8'), (HOST, PORT))
        s.sendto(operator.encode('utf-8'), (HOST, PORT))
        s.sendto(num2.encode('utf-8'), (HOST, PORT))
        response, server = s.recvfrom(4096)
        print(f"Odpowiedź z serwera: {response.decode('utf-8').strip()}")
except Exception as e:
    print(f'Błąd: {e}')