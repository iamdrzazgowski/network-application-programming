import socket

HOST = str(input("Podaj hosta: "))
PORT = int(input("Podaj port: "))

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        s.connect((HOST, PORT))
        print(f"Port {PORT} na hoście {HOST} jest OTWARTY.")

        service = socket.getservbyport(PORT, "tcp") if PORT else "Nieznana usługa"
        print(f"Usługa na porcie {PORT}: {service}")
except socket.error:
    print(f"Port {PORT} na hoście {HOST} jest ZAMKNIĘTY lub niedostępny.")
except OSError:
    print("Nie można znaleźć informacji o usłudze dla tego portu.")
