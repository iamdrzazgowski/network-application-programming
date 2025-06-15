import socket

HOST = '127.0.0.1'
PORT = 12345

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        print(f"Połączono z serwerem {HOST}:{PORT}")

        while True:
            cmd = input("Wpisz komendę ('GET_WEATHER' lub 'exit'): ")
            if cmd.lower() == 'exit':
                break
            sock.sendall((cmd + "\r\n").encode())

            response = b""
            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                response += chunk
                if b"\r\n.\r\n" in response:
                    break

            response_text = response.decode('utf-8').replace("\r\n.\r\n", "")
            print("Odpowiedź serwera:")
            print(response_text)

if __name__ == "__main__":
    main()
