import socket
import ssl
import base64

def send_email_via_telnet():
    port = 587
    smtp_server = "poczta.interia.pl"
    sender_email = "pas2025inf2@interia.pl"
    password = "V*ij8Hk%xqLq&Q5MaW3Bh3v%4X"

    receiver_emails = [
        "pas2025inf@interia.pl",
        "pas2025inf3@interia.pl",
    ]

    client_socket = socket.create_connection((smtp_server, port))
    recv = client_socket.recv(1024).decode()
    print(recv)

    client_socket.send(b"EHLO interia.pl\r\n")
    recv = client_socket.recv(1024).decode()
    print(recv)

    client_socket.send(b"STARTTLS\r\n")
    recv = client_socket.recv(1024).decode()
    print(recv)

    context = ssl.create_default_context()
    secure_socket = context.wrap_socket(client_socket, server_hostname=smtp_server)

    secure_socket.send(b"EHLO interia.pl\r\n")
    recv = secure_socket.recv(1024).decode()
    print(recv)

    login_b64 = base64.b64encode(sender_email.encode()).decode()
    password_b64 = base64.b64encode(password.encode()).decode()

    secure_socket.send(b"AUTH LOGIN\r\n")
    recv = secure_socket.recv(1024).decode()
    print(recv)

    secure_socket.send((login_b64 + "\r\n").encode())
    recv = secure_socket.recv(1024).decode()
    print(recv)

    secure_socket.send((password_b64 + "\r\n").encode())
    recv = secure_socket.recv(1024).decode()
    print(recv)

    secure_socket.send(f"MAIL FROM:<{sender_email}>\r\n".encode())
    recv = secure_socket.recv(1024).decode()
    print(recv)

    for receiver_email in receiver_emails:
        secure_socket.send(f"RCPT TO:<{receiver_email}>\r\n".encode())
        recv = secure_socket.recv(1024).decode()
        print(recv)

    secure_socket.send(b"DATA\r\n")
    recv = secure_socket.recv(1024).decode()

    print(recv)
    message = f"""\
From: {sender_email}
To: {', '.join(receiver_emails)}
Subject: Test ESMTP przez Telnet

To jest testowa wiadomość wysłana przez ESMTP na serwerze Interia.
.
"""
    secure_socket.send(message.encode())
    secure_socket.send(b"\r\n.\r\n")
    recv = secure_socket.recv(1024).decode()
    print(recv)
    secure_socket.send(b"QUIT\r\n")
    recv = secure_socket.recv(1024).decode()
    print(recv)

    secure_socket.close()

send_email_via_telnet()
