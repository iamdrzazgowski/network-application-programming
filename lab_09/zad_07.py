import socket
import os
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 8080

MIME_TYPES = {
    ".html": "text/html",
    ".htm": "text/html",
    ".txt": "text/plain",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".css": "text/css",
    ".js": "application/javascript"
}

BASE_DIR = "examples"  # folder z plikami

def get_content_type(file_path):
    ext = os.path.splitext(file_path)[1]
    return MIME_TYPES.get(ext, "application/octet-stream")

def handle_client(conn, addr):
    try:
        print(f"Połączono z {addr}")
        request = conn.recv(1024).decode('utf-8')
        if not request:
            conn.close()
            return

        first_line = request.splitlines()[0]
        parts = first_line.split()
        if len(parts) < 3:
            response = http_response(400, "Bad Request", "Niepoprawne żądanie.")
            conn.sendall(response)
            conn.close()
            return

        method, path, _ = parts
        print(f"Metoda: {method}, Ścieżka: {path}")

        if method != "GET":
            response = http_response(405, "Method Not Allowed", "Metoda nieobsługiwana.")
            conn.sendall(response)
            conn.close()
            return

        if path == "/":
            path = "/index.html"

        # Tworzymy pełną ścieżkę pliku
        file_path = os.path.join(BASE_DIR, path.lstrip("/"))

        if not os.path.isfile(file_path):
            # 404
            error_path = os.path.join(BASE_DIR, "404.html")
            if os.path.isfile(error_path):
                with open(error_path, "rb") as f:
                    content = f.read()
                response = http_response(404, "Not Found", content, is_binary=True)
            else:
                response = http_response(404, "Not Found", "<h1>404 Not Found</h1>".encode(), is_binary=True)
            conn.sendall(response)
            conn.close()
            return

        with open(file_path, "rb") as f:
            content = f.read()

        response = http_response(200, "OK", content, is_binary=True, content_type=get_content_type(file_path))
        conn.sendall(response)
    except Exception as e:
        print("Błąd podczas obsługi klienta:", e)
    finally:
        conn.close()

def http_response(status_code, reason_phrase, body, is_binary=False, content_type="text/html"):
    status_line = f"HTTP/1.1 {status_code} {reason_phrase}\r\n"
    headers = {
        "Date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "Server": "SimplePythonHTTPServer/1.0",
        "Content-Length": str(len(body)),
        "Connection": "close",
        "Content-Type": content_type
    }

    headers_raw = "".join(f"{key}: {value}\r\n" for key, value in headers.items())
    blank_line = "\r\n"

    if not is_binary:
        body = body.encode('utf-8')

    response = (status_line + headers_raw + blank_line).encode('utf-8') + body
    return response

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"Serwer HTTP działa na http://{HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    main()
