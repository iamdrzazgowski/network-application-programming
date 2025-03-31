import socket

HOST = "127.0.0.1"
PORT = 2090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((HOST, PORT))

print(f"Serwer nasłuchuje na {HOST}:{PORT}")

while True:
    data, addr = server_socket.recvfrom(1024)
    message = data.decode().strip()
    print(f"Otrzymano od {addr}: {message}")

    parts = message.split()
    if len(parts) == 3:
        try:
            num1 = float(parts[0])
            operator = parts[1]
            num2 = float(parts[2])

            if operator == "+":
                result = num1 + num2
            elif operator == "-":
                result = num1 - num2
            elif operator == "*":
                result = num1 * num2
            elif operator == "/":
                if num2 != 0:
                    result = num1 / num2
                else:
                    result = "Błąd: dzielenie przez zero"
            else:
                result = "Błąd: nieznany operator"
        except ValueError:
            result = "Błąd: nieprawidłowe dane"
    else:
        result = "Błąd: niepoprawny format"

    server_socket.sendto(str(result).encode(), addr)
