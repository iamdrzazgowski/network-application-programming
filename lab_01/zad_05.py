import socket

hostname = str(input("Podaj hostname: "))
print(socket.gethostbyname(hostname))
