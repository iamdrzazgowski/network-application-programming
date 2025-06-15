import socket
import ssl

HOST = "httpbin.org"
PORT = 443
REQUEST = (
    "GET /html HTTP/1.1\r\n"
    f"Host: {HOST}\r\n"
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) "
    "AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A\r\n"
    "Connection: close\r\n"
    "\r\n"
)

def main():
    context = ssl.create_default_context()  # Weryfikacja certyfikatu

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname=HOST) as ssock:
            ssock.sendall(REQUEST.encode("utf-8"))
            response = b""
            while True:
                data = ssock.recv(4096)
                if not data:
                    break
                response += data

    header, _, body = response.partition(b"\r\n\r\n")

    with open("strona_z_weryfikacja.html", "wb") as f:
        f.write(body)

    print("✅ Zapisano stronę jako 'strona_z_weryfikacja.html'")

if __name__ == "__main__":
    main()
