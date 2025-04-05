import poplib

host = "poczta.interia.pl"
port = 995
user = "pas2025inf@interia.pl"
password = "dq4cCRSta4VM&qqN9vesJcVeW*"

server = poplib.POP3_SSL(host, port)

server.user(user)
server.pass_(password)

num_messages = len(server.list()[1])

print(f"Liczba wiadomości w skrzynce: {num_messages}")

server.quit()


