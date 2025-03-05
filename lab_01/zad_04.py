import socket

ip = str(input("Podaj adres IP: "))
print(socket.gethostbyaddr(ip))