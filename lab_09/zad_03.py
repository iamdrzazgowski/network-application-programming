import socket

# NA POTRZEBY TEGO ZADANIA UZYŁEM httpbin.org ORAZ PORTU 80 !!!

def get_image_part(host, port, path, byte_range):
    headers = {
        "Host": host,
        "User-Agent": "Mozilla/5.0",
        "Accept": "image/jpeg",
        "Range": f"bytes={byte_range}",
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
    body = response[header_end + 4:]

    return body

host = "httpbin.org"
port = 80
path = "/image/jpeg"

part1 = get_image_part(host, port, path, "0-10239")
part2 = get_image_part(host, port, path, "10240-20479")
part3 = get_image_part(host, port, path, "20480-")  # do końca

with open("obrazek.jpg", "wb") as f:
    f.write(part1 + part2 + part3)

print("Obrazek został zapisany jako 'obrazek.jpg'.")
