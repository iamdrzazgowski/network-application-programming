import poplib

host = "poczta.interia.pl"
port = 995
user = "pas2025inf@interia.pl"
password = "dq4cCRSta4VM&qqN9vesJcVeW*"

server = poplib.POP3_SSL(host, port)

server.user(user)
server.pass_(password)

messages = server.list()[1]

total_size = 0
for message in messages:
    size = int(message.split()[1])
    total_size += size

print(f"Łączny rozmiar wiadomości: {total_size} bajtów")

server.quit()