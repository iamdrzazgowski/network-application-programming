import poplib


host = "poczta.interia.pl"
port = 995
user = "pas2025inf@interia.pl"
password = "dq4cCRSta4VM&qqN9vesJcVeW*"

server = poplib.POP3_SSL(host, port)

server.user(user)
server.pass_(password)

messages = server.list()[1]

max_size = 0
max_msg_num = 0

for message in messages:
    parts = message.decode('utf-8').split()
    if len(parts) == 2:
        try:
            message_number = parts[0]
            message_size = int(parts[1])
            if message_size > max_size:
                max_size = message_size
                max_msg_num = message_number
        except ValueError:
            continue

if max_msg_num:
    print(f"Treść wiadomości o numerze {max_msg_num} (rozmiar: {max_size} bajtów):\n")
    response = server.retr(max_msg_num)

    message_content = b"\n".join(response[1]).decode('utf-8')
    print(message_content)
else:
    print("Nie znaleziono wiadomości.")

server.quit()
