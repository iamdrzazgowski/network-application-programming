import socket

host = "httpbin.org"
port = 80
path = "/image/png"

headers = {
    "Host": host,
    "User-Agent": "Mozilla/5.0",
    "Accept": "image/png",
    "Connection": "close"
}

request_lines = [f"GET {path} HTTP/1.1"]
request_lines += [f"{key}: {value}" for key, value in headers.items()]
request = "\r\n".join(request_lines) + "\r\n\r\n"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(request.encode())

    response = b""
    while True:
        data = s.recv(4096)
        if not data:
            break
        response += data

header_end = response.find(b"\r\n\r\n")
image_data = response[header_end + 4:]

with open("obrazek.png", "wb") as f:
    f.write(image_data)

print("Obrazek został zapisany jako 'obrazek.png'.")
