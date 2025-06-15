import socket
import os

def get_saved_etag():
    if os.path.exists("etag.txt"):
        with open("etag.txt", "r") as f:
            return f.read().strip()
    return None

def save_etag(etag):
    with open("etag.txt", "w") as f:
        f.write(etag)

def send_head_request(host, port, path, etag=None):
    headers = {
        "Host": host,
        "User-Agent": "Mozilla/5.0",
        "Accept": "image/jpeg",
        "Connection": "close"
    }
    if etag:
        headers["If-None-Match"] = etag

    request_lines = [f"HEAD {path} HTTP/1.1"]
    request_lines += [f"{k}: {v}" for k, v in headers.items()]
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
    headers_raw = response[:header_end].decode()

    status_line = headers_raw.split("\r\n")[0]
    status_code = int(status_line.split()[1])
    print(f"HEAD request status: {status_code}")

    if status_code == 304:
        print("Plik nie został zmieniony od ostatniego pobrania.")
        return False

    for line in headers_raw.split("\r\n"):
        if line.lower().startswith("etag:"):
            etag_value = line.split(":", 1)[1].strip()
            save_etag(etag_value)
            print(f"Zapisano nowy ETag: {etag_value}")
    return True

def get_image_part(host, port, path, byte_range):
    headers = {
        "Host": host,
        "User-Agent": "Mozilla/5.0",
        "Accept": "image/jpeg",
        "Range": f"bytes={byte_range}",
        "Connection": "close"
    }

    request_lines = [f"GET {path} HTTP/1.1"]
    request_lines += [f"{k}: {v}" for k, v in headers.items()]
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

etag = get_saved_etag()

if not send_head_request(host, port, path, etag):
    exit()

part1 = get_image_part(host, port, path, "0-10239")
part2 = get_image_part(host, port, path, "10240-20479")
part3 = get_image_part(host, port, path, "20480-")

with open("obrazek.jpg", "wb") as f:
    f.write(part1 + part2 + part3)

print("Obrazek został zapisany jako 'obrazek.jpg'.")
