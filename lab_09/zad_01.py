import socket

host = "httpbin.org"
port = 80
path = "/html"

headers = {
    "Host": host,
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 "
                  "(KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "Accept": "text/html",
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

response_text = response.decode("utf-8", errors="ignore")
header_end = response_text.find("\r\n\r\n")
html_content = response_text[header_end + 4:]

with open("strona.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Strona została zapisana jako 'strona.html'.")
