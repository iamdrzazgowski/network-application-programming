import socket
import select
import json

HOST = '127.0.0.1'
PORT = 12345
API_KEY = 'd4af3e33095b8c43f1a6815954face64'
CITY = 'Lublin'

def get_weather():
    request = (
        f"GET /data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric HTTP/1.1\r\n"
        "Host: api.openweathermap.org\r\n"
        "Connection: close\r\n"
        "\r\n"
    )
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('api.openweathermap.org', 80))
        sock.sendall(request.encode())

        response = b""
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            response += chunk

    try:
        header_data, body = response.split(b"\r\n\r\n", 1)
    except ValueError:
        return "Błąd pobierania danych pogodowych"

    try:
        data = json.loads(body.decode('utf-8'))
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        weather_str = f"Pogoda w {CITY}: {temp}°C, {desc}"
        return weather_str
    except Exception:
        return "Błąd parsowania danych pogodowych"

def handle_client(sock, inputs):
    try:
        data = sock.recv(1024)
        if not data:
            inputs.remove(sock)
            sock.close()
            return

        command = data.decode('utf-8').strip()
        if command == "GET_WEATHER":
            weather_info = get_weather()
            message = weather_info + "\r\n.\r\n"
            sock.sendall(message.encode())
        else:
            sock.sendall(b"ERROR: Nieznana komenda\r\n.\r\n")
    except ConnectionResetError:
        inputs.remove(sock)
        sock.close()

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.listen()
    print(f"Serwer działa na {HOST}:{PORT}")

    inputs = [server_sock]

    while True:
        readable, _, _ = select.select(inputs, [], [])
        for s in readable:
            if s is server_sock:
                client_sock, addr = server_sock.accept()
                print(f"Połączono z {addr}")
                inputs.append(client_sock)
            else:
                handle_client(s, inputs)

if __name__ == "__main__":
    main()
