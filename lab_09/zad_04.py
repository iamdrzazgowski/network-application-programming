import socket
from urllib.parse import urlencode

imie = input("Podaj imię: ")
nazwisko = input("Podaj nazwisko: ")
email = input("Podaj email: ")

form_data = {
    "imie": imie,
    "nazwisko": nazwisko,
    "email": email
}
encoded_data = urlencode(form_data)
content_length = len(encoded_data)

host = "httpbin.org"
port = 80
path = "/post"

headers = {
    "Host": host,
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": str(content_length),
    "Connection": "close"
}

request_lines = [f"POST {path} HTTP/1.1"]
request_lines += [f"{key}: {value}" for key, value in headers.items()]
request = "\r\n".join(request_lines) + "\r\n\r\n" + encoded_data

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(request.encode())

    response = b""
    while True:
        data = s.recv(4096)
        if not data:
            break
        response += data

print("------ ODPOWIEDŹ SERWERA ------\n")
print(response.decode("utf-8", errors="ignore"))
