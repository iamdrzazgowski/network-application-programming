import poplib

host = "poczta.interia.pl"
port = 995
user = "pas2025inf@interia.pl"
password = "dq4cCRSta4VM&qqN9vesJcVeW*"

server = poplib.POP3_SSL(host, port)

server.user(user)
server.pass_(password)

messages = server.list()[1]

for message in messages:
    size = int(message.split()[1])
    print(f"Wiadomość zajmuje {size} bajtów.")

server.quit()
