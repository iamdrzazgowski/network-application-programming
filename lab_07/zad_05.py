import poplib

host = "poczta.interia.pl"
port = 995
user = "pas2025inf@interia.pl"
password = "dq4cCRSta4VM&qqN9vesJcVeW*"

server = poplib.POP3_SSL(host, port)

server.user(user)
server.pass_(password)

messages = server.list()[1]

min_size = float('inf')
min_msg_num = None

for message in messages:
    parts = message.decode('utf-8').split()
    if len(parts) == 2:
        try:
            message_number = parts[0]
            message_size = int(parts[1])
            if message_size < min_size:
                min_size = message_size
                min_msg_num = message_number
        except ValueError:
            continue

if min_msg_num:
    print(f"Usuwam wiadomość o numerze {min_msg_num} (rozmiar: {min_size} bajtów)")
    server.dele(min_msg_num)
else:
    print("Nie znaleziono wiadomości do usunięcia.")

server.quit()
